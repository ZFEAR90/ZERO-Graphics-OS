"""Run every importer/unit and browser check; preserve exact exits and failure logs."""
from pathlib import Path
import sys,subprocess,json,concurrent.futures,datetime
root=Path(__file__).resolve().parents[1];out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/main-roll-regression');out.mkdir(parents=True,exist_ok=True)
commands=[('unittest',[sys.executable,'-m','unittest','discover','-s','tests','-p','test_*.py','-q'])]+[(p.name,[sys.executable,str(p)]) for p in sorted((root/'tests').glob('browser*check.py'))]
def run(entry):
 name,command=entry
 with (out/(name+'.log')).open('w') as log:
  try:result=subprocess.run(command,cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=180);code=result.returncode;status='passed' if code==0 else 'failed'
  except subprocess.TimeoutExpired:code=None;status='failed-timeout'
 return {'name':name,'status':status,'exit_code':code,'log':str(out/(name+'.log'))}
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for result in pool.map(run,commands):
  results.append(result);print(result['name'],result['status'],flush=True)
  report={'results':results,'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']!='passed' for r in results),'skipped':0,'unrun':len(commands)-len(results)};(out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
sys.exit(1 if report['failed'] else 0)
