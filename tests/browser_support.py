"""Shared real-browser fixture: range-capable media, fixed scene time, failure evidence."""
from pathlib import Path
from http.server import ThreadingHTTPServer
from contextlib import contextmanager
from functools import partial
import importlib.util,threading,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('main_roll_test_importer',ROOT/'ze_local_importer.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
class Handler(helper.Handler):
 def do_GET(self):
  if self.path.startswith('/fixtures/'):return self._send_media(ROOT/'tests/fixtures'/Path(self.path).name)
  super().do_GET()
 def log_message(self,*args):pass
class Scene:
 def __init__(self,page,url):self.page=page;self.url=url
 def all_controls(self):self.page.evaluate("document.querySelectorAll('.editor-tab-panel').forEach(e=>e.hidden=false);document.querySelectorAll('details').forEach(e=>e.open=true)")
 def post(self,text='Editable post',files=('portrait.png',)):
  self.page.evaluate('''async v=>{zeCommitPost(await zePreparePost({text:v.text,attachments:v.files.map(f=>({type:f.endsWith('.mp4')?'video':'image',url:'/fixtures/'+f}))}));zePost.items.forEach((item,i)=>item.label=v.files[i]);zeRefreshMediaList();setT(5)}''',dict(text=text,files=list(files)))
  self.page.wait_for_function('zePost.items.filter(i=>i.type==="video").every(i=>i.el.readyState>=2&&!i.el.seeking)')
 def value(self,id,value):self.page.locator('#'+id).evaluate("(el,v)=>{if(el.type==='checkbox')el.checked=v;else el.value=v;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}))}",value)
 def boxes(self):return self.page.evaluate('structuredClone(zeSafeLayout())')
 def drag(self,name,dx=-10,dy=-8):
  p=self.page;p.locator('#canvas').scroll_into_view_if_needed();b=p.evaluate('(n)=>zeSelectionBounds(n)',name);r=p.locator('#canvas').bounding_box();x=r['x']+(b['x']+b['w']/2)/960*r['width'];y=r['y']+(b['y']+b['h']/2)/540*r['height'];p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+dx,y+dy,steps=8);p.mouse.up()
@contextmanager
def scene(name):
 server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();errors=[]
 try:
  with sync_playwright() as pw:
   browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1600,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)))
   try:
    url=f'http://127.0.0.1:{server.server_port}';page.goto(url+'/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('assets.source&&state.stvLoaded');yield Scene(page,url);assert not errors and not page.evaluate('state.renderError'),errors
   except Exception:
    target=Path('/tmp/ze-browser-evidence')/name;target.mkdir(parents=True,exist_ok=True)
    try:page.screenshot(path=str(target/'failure.png'),full_page=True);(target/'errors.json').write_text(json.dumps(errors))
    except Exception:pass
    raise
   finally:browser.close()
 finally:server.shutdown();server.server_close()
