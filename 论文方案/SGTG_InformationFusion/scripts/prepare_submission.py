"""Build a self-contained flat submission copy on VOA; never edits original materials."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, shutil, subprocess, zipfile
P=Path(__file__).resolve().parents[1]; S=P/'source'
p=argparse.ArgumentParser(); p.add_argument('--source-build',default='build-final-20260923-r4'); args=p.parse_args()
D=S/args.source_build; F=P/'submission_flat'; A=P/'audit/stage5'
if not (D/'main.pdf').is_file() or not (D/'main.bbl').is_file():
    raise SystemExit('Build source successfully first.')
if F.exists():
    raise SystemExit('submission_flat already exists; inspect/archive it before regeneration.')
F.mkdir(); A.mkdir(parents=True,exist_ok=True)
files=[]
for f in S.rglob('*'):
    rel=f.relative_to(S)
    if not f.is_file() or any(x.startswith('build') for x in rel.parts): continue
    if rel.parts[0]=='license' or f.name in ('reference_order.tex','cas-model2-names.bst','main.bbl'): continue
    if f.suffix.lower() in ('.tex','.cls','.sty','.bst','.bib','.pdf','.png','.jpeg','.jpg'): files.append(f)
mapping={f.relative_to(S).as_posix():f.name for f in files}
mapping['cas-dc.cls']='cas-dc-flat.cls'; mapping['cas-common.sty']='cas-common-flat.sty'
if len(set(n.lower() for n in mapping.values()))!=len(mapping): raise SystemExit('Filename collision.')
changes=[]
for f in files:
    rel=f.relative_to(S).as_posix(); target=F/mapping[rel]
    if f.suffix in ('.tex','.cls','.sty'):
        text=f.read_text('utf-8'); original=text
        for old,new in sorted(mapping.items(),key=lambda q:len(q[0]),reverse=True):
            if '/' in old: text=text.replace(old,new)
        text=text.replace('{cas-dc}','{cas-dc-flat}').replace('{cas-common}','{cas-common-flat}')
        text=re.sub(r'(?m)^% !TeX root = .*$', '% !TeX root = main.tex',text)
        if f.name in ('cas-dc.cls','cas-common.sty'):
            text='% Renamed modified CAS 2.4 copy: only flat dependency paths/names changed.\n% Original copyright and LPPL terms below remain applicable.\n'+text
        target.write_text(text,encoding='utf-8',newline='\n')
        if text!=original: changes.append(rel)
    else: shutil.copy2(f,target)
for original,name in [('license/README','CAS_README.txt'),('license/manifest.txt','CAS_ORIGINAL_MANIFEST.txt')]:
    shutil.copy2(S/original,F/name)
(F/'SOURCE_NOTICE.txt').write_text('SGTG typesetting manuscript with pending author confirmations, not a submission-ready certification.\nMain entry: main.tex. Use XeLaTeX + BibTeX.\nCAS-DC/common copies are renamed only to adapt dependencies to a flat folder; LPPL headers retained.\nNo source/ or external manuscript directory is needed.\nNo author-unconfirmed declarations or Highlights are included.\n',encoding='utf-8')
O=A/('flat-build-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')); O.mkdir()
exe=Path(r'C:\Users\admin\texlive\2026\bin\windows\latexmk.exe')
if os.name!='nt' or not exe.is_file(): raise SystemExit('VOA Windows toolchain required.')
relout=os.path.relpath(O,F).replace('\\','/')
cmd=[str(exe),'-g','-xelatex','-synctex=1','-interaction=nonstopmode','-file-line-error','-halt-on-error','-outdir='+relout,'-auxdir='+relout,'main.tex']
started=datetime.datetime.now().astimezone().isoformat()
with (O/'console.log').open('wb') as log:
    proc=subprocess.run(cmd,cwd=F,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
record={'started':started,'ended':datetime.datetime.now().astimezone().isoformat(),'cwd':str(F),'args':cmd,'exit_code':proc.returncode,'output':str(O),'initial_auxiliary_files':[]}
(A/'flat-build.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
if proc.returncode: raise SystemExit('Flat build failed: '+str(O/'console.log'))
shutil.copy2(O/'main.bbl',F/'main.bbl')
shutil.copy2(D/'main.bbl',S/'main.bbl')
shutil.copy2(D/'main.pdf',P/'SGTG_InformationFusion.pdf')
zip_path=P/'SGTG_InformationFusion_submission.zip'
if zip_path.exists(): raise SystemExit('Existing ZIP not overwritten.')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as archive:
    for f in sorted(F.iterdir()):
        assert f.is_file(); archive.write(f,f.name)
from pypdf import PdfReader
src_pdf=PdfReader(D/'main.pdf'); flat_pdf=PdfReader(O/'main.pdf')
assert len(src_pdf.pages)==len(flat_pdf.pages)
assert [(p.extract_text() or '') for p in src_pdf.pages]==[(p.extract_text() or '') for p in flat_pdf.pages], 'Flat text differs'
assert (D/'main.bbl').read_bytes()==(O/'main.bbl').read_bytes(), 'Bibliography differs'
external=[]; inputs=[]; texroot=exe.parents[2].resolve()
for line in (O/'main.fls').read_text('utf-8',errors='replace').splitlines():
    if not line.startswith('INPUT '): continue
    x=Path(line[6:]); x=(F/x).resolve() if not x.is_absolute() else x.resolve()
    inputs.append(str(x))
    if x.is_relative_to(texroot) or x.is_relative_to(F.resolve()) or x.is_relative_to(O.resolve()): continue
    external.append(str(x))
assert not external, external
manifest=[{'file':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(F.iterdir())]
with zipfile.ZipFile(zip_path) as archive:
    assert archive.testzip() is None
    assert all('/' not in n and '\\' not in n for n in archive.namelist())
    assert all(archive.read(f.name)==f.read_bytes() for f in F.iterdir())
result={'mapping':mapping,'modified_text_paths':changes,'flat_files':manifest,'flat_build':record,'external_inputs':external,'pdf_pages':len(src_pdf.pages),'source_flat_page_text_equal':True,'bbl_equal':True,'zip_test_passed':True,'zip':str(zip_path),'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest()}
(A/'submission-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'flat_files':len(manifest),'pdf_pages':len(src_pdf.pages),'flat_exit':proc.returncode,'source_flat_text_equal':True,'zip':str(zip_path),'flat_build_output':str(O)},ensure_ascii=False,indent=2))
