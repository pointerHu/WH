"""Upload actual video bytes through the same API used by the browser."""
import argparse
import json
import sys
import time
import uuid
import urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import ROOT, sha256, write_json


def get_json(url):
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.load(response)


def verify(video, mode, description, output, expected_error=None):
    base = 'http://127.0.0.1:8765'
    health = get_json(base + '/api/health')
    assert health['video_files_ready'], health['missing']
    boundary = uuid.uuid4().hex
    content = video.read_bytes()
    body = ('--%s\r\nContent-Disposition: form-data; name="mode"\r\n\r\n%s\r\n'
            '--%s\r\nContent-Disposition: form-data; name="file"; filename="test%s"\r\n'
            'Content-Type: application/octet-stream\r\n\r\n' %
            (boundary, mode, boundary, video.suffix)).encode() + content
    body += ('\r\n--%s--\r\n' % boundary).encode()
    request = urllib.request.Request(base + '/api/jobs', data=body, method='POST')
    request.add_header('Content-Type', 'multipart/form-data; boundary=' + boundary)
    request.add_header('X-KA-Demo-Token', health['server_token'])
    started = time.monotonic()
    with urllib.request.urlopen(request, timeout=30) as response:
        assert response.status == 202
        job = json.load(response)
    print('JOB', job['id'], flush=True)
    stages = []
    while time.monotonic() - started < 300:
        state = get_json(base + '/api/jobs/' + job['id'])
        stage = state.get('stage', state['status'])
        if stage not in stages:
            stages.append(stage)
            print('STAGE', stage, flush=True)
        if state['status'] in ('completed', 'failed'):
            break
        time.sleep(0.5)
    else:
        raise TimeoutError('Video HTTP verification timed out')
    report = dict(input_description=description, input_sha256=sha256(video),
                  input_bytes=len(content), mode=mode, job_id=job['id'],
                  observed_stages=stages, status=state['status'],
                  wall_seconds=time.monotonic()-started, accuracy_claim=False)
    if expected_error:
        assert state['status'] == 'failed' and expected_error in state.get('error', ''), state
        report.update(passed=True, rejected_as_expected=True, error=state['error'])
    else:
        assert state['status'] == 'completed', state
        result = state['result']
        assert result['input_kind'] == 'raw_video'
        assert result['feature_dimensions'] == dict(audio=1024, video=512, text=1536)
        assert len(result['metadata']['wavcaps_sha256']) == 64
        assert result['confidence_kind'] == 'relative_softmax_uncalibrated'
        total = sum(p['confidence'] for p in result['top5']) + result['remaining_probability']
        assert abs(total - 1) < 1e-5 and all(0 <= p['confidence'] <= 1 for p in result['top5'])
        assert result['prediction'] == result['top5'][0]
        assert get_json(base + '/api/jobs/' + job['id'] + '/result') == result
        with urllib.request.urlopen(base + '/api/jobs/' + job['id'] + '/preview', timeout=10) as response:
            assert response.headers.get_content_type() == 'image/jpeg'
        if mode == 'zsl':
            assert all(not p['seen'] for p in result['top5'])
            assert result['candidate_count'] == health['unseen_count']
        report.update(passed=True, result=result)
    write_json(output, report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video', type=Path)
    parser.add_argument('--mode', choices=['gzsl', 'zsl'], default='gzsl')
    parser.add_argument('--description', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--expected-error')
    args = parser.parse_args()
    verify(args.video, args.mode, args.description, args.output, args.expected_error)
