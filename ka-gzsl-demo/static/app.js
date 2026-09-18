'use strict';
const $ = (id) => document.getElementById(id);
let health = null, selectedFile = null, objectURL = null, busy = false;
const text = (id, value) => { $(id).textContent = value; };
const show = (id, visible) => { $(id).hidden = !visible; };
const percent = (value) => `${(value * 100).toFixed(2)}%`;

async function requestJSON(url, options = {}) {
  const response = await fetch(url, options);
  let body;
  try { body = await response.json(); } catch (_) { throw new Error('服务返回了无效响应。'); }
  if (!response.ok) throw new Error(typeof body.detail === 'string' ? body.detail : '请求失败，请检查运行环境。');
  return body;
}
function buttons() {
  $('runButton').disabled = busy || !selectedFile || !health?.video_files_ready;
  $('sampleButton').disabled = busy || !health?.sample_ready;
  $('modeSelect').disabled = busy;
  $('fileInput').disabled = busy;
  $('changeVideo').disabled = busy;
}
async function refreshHealth() {
  try {
    health = await requestJSON('/api/health');
    text('datasetName', health.dataset);
    text('classCount', health.classes.length || '—');
    text('limits', `含音轨 · 最长 ${health.max_duration_seconds} 秒 · 最大 ${health.max_upload_mb} MB`);
    const badge = $('healthBadge');
    badge.classList.toggle('ready', health.video_files_ready);
    badge.replaceChildren(document.createElement('i'), document.createTextNode(health.video_files_ready ? '视频组件已就绪' : '视频组件待补全'));
    $('notice').classList.toggle('ok', health.video_files_ready);
    text('notice', health.video_files_ready
      ? '模型与编码器文件已就绪。请上传含音轨的视频进行实际推理；相对置信分数尚未校准。'
      : `当前尚缺：${health.missing.join('、')}。可以选择视频预览；补全权重前不会生成视频预测。已有模型时，可单独运行真实特征验证。`);
  } catch (error) {
    text('notice', `无法连接本机服务：${error.message}`);
    text('healthBadge', '服务未连接');
  }
  buttons();
}
function choose(file) {
  if (!file || busy) return;
  show('errorBox', false);
  if (!/\.(mp4|avi|mov|mkv|webm)$/i.test(file.name)) return fail('请选择支持的视频文件。');
  if (health && file.size > health.max_upload_mb * 1024 * 1024) return fail('视频超过文件大小限制。');
  selectedFile = file;
  history.replaceState(null, '', location.pathname);
  document.getElementById('savedPreview')?.remove();
  $('videoPreview').hidden = false;
  show('resultContent', false); show('emptyResult', true); show('progressWrap', false);
  text('resultTag', '等待输入');
  if (objectURL) URL.revokeObjectURL(objectURL);
  objectURL = URL.createObjectURL(file);
  $('videoPreview').src = objectURL;
  text('fileInfo', `${file.name} · ${(file.size / 1024 / 1024).toFixed(2)} MB`);
  show('previewError', false); show('dropzone', false); show('videoWrap', true);
  buttons();
}
function fail(message) { text('errorBox', message); show('errorBox', true); }
function begin() {
  busy = true; buttons(); show('emptyResult', false); show('resultContent', false);
  show('errorBox', false); show('progressWrap', true); text('resultTag', '计算中');
  text('progressMessage', '正在提交任务'); text('progressPercent', '0%'); $('progressBar').style.width = '0%';
}
async function follow(job) {
  const deadline = Date.now() + 600000;
  while (Date.now() < deadline) {
    const state = await requestJSON(`/api/jobs/${job.id}`);
    const progress = Math.max(0, Math.min(100, Number(state.progress || 0)));
    text('progressMessage', state.message || (state.status === 'queued' ? '等待前一项任务完成' : '正在初始化模型'));
    text('progressPercent', `${progress}%`); $('progressBar').style.width = `${progress}%`;
    if (state.status === 'failed') throw new Error(state.error || '模型推理失败。');
    if (state.status === 'completed') { render(state.result, job.id); return; }
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  throw new Error('页面等待已超时，请查看本机任务日志。');
}
function render(result, jobId) {
  show('progressWrap', false); show('resultContent', true); text('resultTag', '真实模型输出');
  text('inputKind', result.input_kind === 'raw_video' ? '视频输入 → 特征提取 → KA-GZSL' : '已有 UCF 特征 → KA-GZSL（非视频链路验证）');
  text('predictedClass', result.prediction.label);
  text('confidenceValue', percent(result.prediction.confidence));
  text('seenBadge', result.prediction.seen ? '已见类 / Seen' : '未见类 / Unseen');
  const list = $('rankList'); list.replaceChildren();
  result.top5.forEach((item, index) => {
    const row = document.createElement('div'); row.className = 'rank';
    const line = document.createElement('div'); line.className = 'rank-line';
    const name = document.createElement('span'); name.className = 'rank-name';
    const rank = document.createElement('span'); rank.textContent = String(index + 1).padStart(2, '0');
    name.append(rank, document.createTextNode(item.label));
    const value = document.createElement('span'); value.className = 'rank-value'; value.textContent = percent(item.confidence);
    line.append(name, value);
    const track = document.createElement('div'); track.className = 'rank-track';
    const fill = document.createElement('i'); fill.style.width = `${Math.max(0, Math.min(1, item.confidence)) * 100}%`;
    track.append(fill); row.append(line, track); list.append(row);
  });
  text('remainingScore', `其余候选合计：${percent(result.remaining_probability)}。Top-5 分数不必合计为 100%。`);
  text('elapsedValue', `${result.elapsed_seconds.toFixed(2)} s`);
  text('candidatesValue', `${result.candidate_count} 类`);
  const warnings = $('resultWarnings'); warnings.replaceChildren();
  result.warnings.forEach(message => { const p = document.createElement('p'); p.textContent = message; warnings.append(p); });
  $('downloadResult').href = `/api/jobs/${jobId}/result`;
  history.replaceState(null, '', `?job=${encodeURIComponent(jobId)}`);
  $('modeSelect').value = result.mode;
  text('classCount', result.candidate_count);
  if (result.input_kind === 'raw_video' && !selectedFile) {
    document.getElementById('savedPreview')?.remove();
    const image = document.createElement('img'); image.id = 'savedPreview';
    image.src = `/api/jobs/${jobId}/preview`; image.alt = '该推理任务的视频中间帧';
    image.style.cssText = 'display:block;width:100%;border-radius:10px';
    $('videoWrap').prepend(image); $('videoPreview').hidden = true;
    text('fileInfo', '历史结果 · 视频中间帧；选择新视频后重新计算');
    show('dropzone', false); show('videoWrap', true);
  }
}
$('fileInput').addEventListener('change', event => choose(event.target.files[0]));
$('changeVideo').addEventListener('click', () => $('fileInput').click());
$('videoPreview').addEventListener('error', () => show('previewError', true));
$('dropzone').addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); $('fileInput').click(); } });
['dragenter', 'dragover'].forEach(type => $('dropzone').addEventListener(type, event => { event.preventDefault(); $('dropzone').classList.add('dragging'); }));
['dragleave', 'drop'].forEach(type => $('dropzone').addEventListener(type, event => { event.preventDefault(); $('dropzone').classList.remove('dragging'); }));
$('dropzone').addEventListener('drop', event => choose(event.dataTransfer.files[0]));
$('runButton').addEventListener('click', async () => {
  if (!selectedFile || busy) return;
  begin();
  try {
    const form = new FormData(); form.append('file', selectedFile); form.append('mode', $('modeSelect').value);
    await follow(await requestJSON('/api/jobs', {method:'POST',headers:{'X-KA-Demo-Token':health.server_token},body:form}));
  } catch (error) { show('progressWrap', false); text('resultTag', '未完成'); fail(error.message); }
  finally { busy = false; buttons(); }
});
$('sampleButton').addEventListener('click', async () => {
  if (busy) return; begin();
  try { await follow(await requestJSON('/api/sample', {method:'POST',headers:{'X-KA-Demo-Token':health.server_token}})); }
  catch (error) { show('progressWrap', false); text('resultTag', '未完成'); fail(error.message); }
  finally { busy = false; buttons(); }
});
window.addEventListener('beforeunload', () => { if (objectURL) URL.revokeObjectURL(objectURL); });
$('modeSelect').addEventListener('change', () => {
  if (health) text('classCount', $('modeSelect').value === 'zsl' ? health.unseen_count : health.classes.length);
});
async function initialize() {
  await refreshHealth();
  const jobId = new URLSearchParams(location.search).get('job');
  if (!jobId) return;
  if (!/^[a-f0-9]{32}$/.test(jobId)) return fail('结果链接格式无效。');
  begin();
  try { await follow({id:jobId}); }
  catch (error) { show('progressWrap', false); text('resultTag', '未完成'); fail(error.message); }
  finally { busy = false; buttons(); }
}
initialize();
