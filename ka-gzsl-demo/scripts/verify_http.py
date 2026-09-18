"""Real HTTP-to-worker verification; never submits fake raw-video predictions."""
import json, sys, time, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import ROOT, write_json

def call(path, method='GET', token=None):
    headers = {'X-KA-Demo-Token': token} if token else {}
    req = urllib.request.Request('http://127.0.0.1:8765' + path, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.load(response)

health = call('/api/health')
job = call('/api/sample', 'POST', health['server_token'])
for _ in range(120):
    state = call('/api/jobs/' + job['id'])
    if state['status'] in ('completed', 'failed'):
        break
    time.sleep(1)
assert state['status'] == 'completed', state
result = state['result']
assert result['input_kind'] == 'cached_feature_validation'
assert result['confidence_kind'] == 'relative_softmax_uncalibrated'
assert result['candidate_count'] == 48
report = {'status': 'passed', 'input_kind': result['input_kind'], 'candidate_count': result['candidate_count'], 'prediction': result['prediction'], 'elapsed_seconds': result['elapsed_seconds'], 'raw_video_end_to_end_verified': False, 'result_download_verified': call('/api/jobs/' + job['id'] + '/result')['prediction'] == result['prediction']}
write_json(ROOT / 'artifacts/http_verification.json', report)
write_json(ROOT / 'artifacts/http_feature_result.json', result)
print(json.dumps(report, ensure_ascii=False, indent=2))
