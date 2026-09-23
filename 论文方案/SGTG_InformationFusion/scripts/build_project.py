"""VOA Windows XeLaTeX build. Never cleans a directory or changes global settings."""
from pathlib import Path
import argparse, datetime, json, os, subprocess, sys
P = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--out', default='build')
p.add_argument('--full', action='store_true')
a = p.parse_args()
S = P / 'source'; out = S / a.out
if out.resolve().parent != S.resolve() or out.name in ('', '.', '..'):
    raise SystemExit('Output must be a direct subdirectory of source.')
engine = Path(r'C:\Users\admin\texlive\2026\bin\windows\xelatex.exe')
mk = engine.with_name('latexmk.exe')
if os.name != 'nt' or not engine.is_file() or not mk.is_file():
    raise SystemExit('Verified VOA Windows XeLaTeX installation required.')
out.mkdir(exist_ok=True)
args = [str(mk)] + (['-g'] if a.full else []) + ['-xelatex','-synctex=1','-interaction=nonstopmode','-file-line-error','-halt-on-error','-outdir='+a.out,'-auxdir='+a.out,'main.tex']
started = datetime.datetime.now().astimezone().isoformat()
with (out/'console.log').open('wb') as log:
    result = subprocess.run(args,cwd=S,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
record = {'started':started,'ended':datetime.datetime.now().astimezone().isoformat(),'cwd':str(S),'args':args,'exit_code':result.returncode,'output':str(out),'engine_version':subprocess.run([str(engine),'--version'],capture_output=True,text=True).stdout.splitlines()[0]}
(out/'build-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False,indent=2))
print((out/'console.log').read_bytes().decode('utf-8',errors='replace')[-3500:])
sys.exit(result.returncode)
