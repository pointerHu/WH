"""Start the local demo once; never alter another process listening on this port."""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import ROOT, UPSTREAM_COMMIT

def healthy():
    try:
        with urllib.request.urlopen('http://127.0.0.1:8765/api/health', timeout=2) as response:
            state = json.load(response)
    except (OSError, ValueError):
        return False
    if state.get('upstream_commit') != UPSTREAM_COMMIT:
        raise RuntimeError('Port 8765 is occupied by a different application; it was not stopped.')
    return True

if healthy():
    print('KA-GZSL demo is already running: http://127.0.0.1:8765')
else:
    (ROOT / 'runtime').mkdir(exist_ok=True)
    with (ROOT / 'runtime/server.log').open('a') as log:
        process = subprocess.Popen(['bash', str(ROOT / 'scripts/serve.sh')], cwd=str(ROOT), stdout=log, stderr=subprocess.STDOUT, start_new_session=True, stdin=subprocess.DEVNULL)
    (ROOT / 'runtime/server.pid').write_text(str(process.pid))
    for _ in range(40):
        if healthy():
            print('KA-GZSL demo started: http://127.0.0.1:8765')
            break
        if process.poll() is not None:
            raise RuntimeError('Startup failed; inspect runtime/server.log')
        time.sleep(0.5)
    else:
        raise RuntimeError('Startup check timed out; inspect runtime/server.log')
