"""Loopback-only thesis demonstration API. GPU work runs in an isolated process."""
from __future__ import annotations
import asyncio
import hmac
import logging
import os
import secrets
import shutil
import signal
import subprocess
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlsplit
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from runtime import ROOT, load_config, read_json, readiness, write_json

CONFIG = load_config()
JOBS = ROOT / "runtime/jobs"
TOKEN = secrets.token_urlsafe(32)
LOCK = threading.Lock()
POOL = ThreadPoolExecutor(max_workers=1, thread_name_prefix="ka-inference")
ACTIVE = set()
ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}


def cleanup():
    JOBS.mkdir(parents=True, exist_ok=True)
    cutoff = time.time() - float(CONFIG["retention_hours"]) * 3600
    with LOCK:
        active = set(ACTIVE)
    for directory in JOBS.iterdir():
        if directory.is_dir() and not directory.is_symlink() and directory.name not in active:
            if directory.stat().st_mtime < cutoff:
                shutil.rmtree(directory)


@asynccontextmanager
async def lifespan(app):
    cleanup()
    yield
    POOL.shutdown(wait=True)


app = FastAPI(title="KA-GZSL Video Demo", version="0.1.0", lifespan=lifespan)


class UploadTooLarge(Exception):
    pass


class LocalOnlyAndSizeLimit:
    def __init__(self, application):
        self.application = application
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.application(scope, receive, send)
        headers = dict(scope.get("headers", []))
        hostname = urlsplit("http://" + headers.get(b"host", b"").decode("latin1")).hostname
        if hostname not in {"localhost", "127.0.0.1", "::1", "testserver"}:
            return await JSONResponse({"detail": "仅允许本机访问。"}, status_code=403)(scope, receive, send)
        limit = int(CONFIG["max_upload_mb"] * 1024 * 1024) + 65536
        try:
            declared = int(headers.get(b"content-length", b"0"))
        except ValueError:
            declared = limit + 1
        if declared > limit:
            return await JSONResponse({"detail": "上传超过大小限制。"}, status_code=413)(scope, receive, send)
        total = 0
        async def bounded_receive():
            nonlocal total
            message = await receive()
            if message["type"] == "http.request":
                total += len(message.get("body", b""))
                if total > limit:
                    raise UploadTooLarge()
            return message
        try:
            await self.application(scope, bounded_receive, send)
        except UploadTooLarge:
            await JSONResponse({"detail": "上传超过大小限制。"}, status_code=413)(scope, receive, send)


app.add_middleware(LocalOnlyAndSizeLimit)
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")


def authorize(request):
    supplied = request.headers.get("x-ka-demo-token", "")
    if not hmac.compare_digest(supplied, TOKEN):
        raise HTTPException(403, "请从本机展示页面发起操作。")


def job_path(job_id):
    try:
        normalized = uuid.UUID(job_id).hex
    except (ValueError, AttributeError):
        raise HTTPException(404, "任务不存在。")
    if job_id != normalized:
        raise HTTPException(404, "任务不存在。")
    path = JOBS / normalized
    if not path.is_dir():
        raise HTTPException(404, "任务不存在或已过期。")
    return path


def reserve_job():
    cleanup()
    with LOCK:
        if len(ACTIVE) >= 2:
            raise HTTPException(429, "已有推理任务正在运行或排队，请在当前任务完成后重试。")
        if len(list(JOBS.iterdir())) >= int(CONFIG["max_jobs"]):
            raise HTTPException(507, "本地任务存储已达到上限，请清理 runtime/jobs。")
        job_id = uuid.uuid4().hex
        ACTIVE.add(job_id)
    directory = JOBS / job_id
    directory.mkdir(parents=True)
    write_json(directory / "state.json", {"id": job_id, "status": "queued", "created_at": time.time()})
    return job_id, directory


def run_worker(job_id):
    directory = JOBS / job_id
    write_json(directory / "state.json", {"id": job_id, "status": "running"})
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONDONTWRITEBYTECODE="1",
               OMP_NUM_THREADS="4", MKL_NUM_THREADS="4")
    command = [CONFIG["model_python"], "-u", str(ROOT / "inference.py"), "--job-dir", str(directory)]
    try:
        with (directory / "worker.log").open("w", encoding="utf-8") as log:
            process = subprocess.Popen(command, cwd=str(ROOT), env=env, stdout=log,
                                       stderr=subprocess.STDOUT, start_new_session=True)
            try:
                code = process.wait(timeout=float(CONFIG["job_timeout_seconds"]))
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                raise TimeoutError("视频处理超过时限，请缩短视频后重试。")
        if code != 0 or not (directory / "result.json").is_file():
            error = read_json(directory / "error.json") if (directory / "error.json").exists() else {}
            raise RuntimeError(error.get("error", "推理失败，请查看本机 worker.log。"))
        write_json(directory / "state.json", {"id": job_id, "status": "completed"})
    except Exception as exc:
        logging.exception("Inference job failed: %s", job_id)
        write_json(directory / "state.json", {"id": job_id, "status": "failed", "error": str(exc)})
    finally:
        with LOCK:
            ACTIVE.discard(job_id)


@app.get("/")
def index():
    return FileResponse(ROOT / "static/index.html", media_type="text/html")


@app.get("/api/health")
def health():
    result = readiness(CONFIG)
    with LOCK:
        result["active_jobs"] = len(ACTIVE)
    result.update({"server_token": TOKEN, "max_upload_mb": CONFIG["max_upload_mb"],
                   "max_duration_seconds": CONFIG["max_duration_seconds"]})
    return result


@app.post("/api/jobs", status_code=202)
async def upload_video(request: Request, file: UploadFile = File(...), mode: str = Form("gzsl")):
    authorize(request)
    try:
        if mode not in ("gzsl", "zsl"):
            raise HTTPException(422, "分类模式无效。")
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            raise HTTPException(415, "请选择 MP4、AVI、MOV、MKV 或 WebM 视频。")
        state = readiness(CONFIG)
        if not state["video_files_ready"]:
            raise HTTPException(503, "视频链路尚缺：" + "、".join(state["missing"]))
        job_id, directory = reserve_job()
        try:
            size = 0
            with (directory / ("input" + suffix)).open("wb") as destination:
                while True:
                    chunk = await file.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > int(CONFIG["max_upload_mb"] * 1024 * 1024):
                        raise HTTPException(413, "视频超过大小限制。")
                    destination.write(chunk)
            if not size:
                raise HTTPException(400, "上传文件为空。")
            write_json(directory / "request.json", {"input_kind": "raw_video", "mode": mode,
                       "stored_filename": "input" + suffix, "bytes": size})
            POOL.submit(run_worker, job_id)
            return {"id": job_id, "status": "queued"}
        except BaseException:
            with LOCK:
                ACTIVE.discard(job_id)
            shutil.rmtree(directory)
            raise
    finally:
        await file.close()


@app.post("/api/sample", status_code=202)
def sample(request: Request):
    authorize(request)
    if not readiness(CONFIG)["sample_ready"]:
        raise HTTPException(503, "尚未导出模型与真实特征示例。")
    job_id, directory = reserve_job()
    write_json(directory / "request.json", {"input_kind": "cached_feature_validation", "mode": "gzsl"})
    POOL.submit(run_worker, job_id)
    return {"id": job_id, "status": "queued"}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    directory = job_path(job_id)
    result = read_json(directory / "state.json")
    if (directory / "progress.json").exists():
        result.update(read_json(directory / "progress.json"))
    if result["status"] == "completed":
        result["result"] = read_json(directory / "result.json")
    return result


@app.get("/api/jobs/{job_id}/result")
def download_result(job_id: str):
    path = job_path(job_id) / "result.json"
    if not path.is_file():
        raise HTTPException(404, "结果尚未生成。")
    return FileResponse(path, media_type="application/json", filename="ka-gzsl-result.json")


@app.get("/api/jobs/{job_id}/preview")
def preview(job_id: str):
    path = job_path(job_id) / "preview.jpg"
    if not path.is_file():
        raise HTTPException(404, "当前任务没有视频预览帧。")
    return FileResponse(path, media_type="image/jpeg")
