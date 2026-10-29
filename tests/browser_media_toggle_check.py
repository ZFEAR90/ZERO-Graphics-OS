"""Disabling post media keeps the chosen layout and reveals editable post text."""
from pathlib import Path
from http.server import ThreadingHTTPServer
import importlib.util,threading,json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('helper',root/'ze_local_importer.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
class Handler(helper.Handler):
 def do_GET(self):
  if self.path.startswith('/fixtures/'):return self._send_media(root/'tests/fixtures'/Path(self.path).name)
  super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source');assert page.locator('#portraitLayout').input_value()=='reference'
  text='نص المنشور الحقيقي يبقى في الرول عند إخفاء الفيديو، مع الاحتفاظ بموقع الإطار وهويته. '
  for layout in ['reference','focus','balanced','beside','social']:
   page.locator('#portraitLayout').select_option(layout,force=True)
   for filename in ['landscape.mp4','portrait.mp4']:
    page.evaluate('''async(v)=>{zeCommitPost(await zePreparePost({text:v.text.repeat(10),attachments:[{type:'video',url:'/fixtures/'+v.file}]}));setT(5)}''',dict(text=text,file=filename))
    page.wait_for_function('zePost.items[0].el.readyState>=2 && !zePost.items[0].el.seeking')
    for solo in ([False,True] if layout!='social' else [True]):
     page.locator('#showBullets').set_checked(not solo,force=True) if layout!='social' else None
     for flip in [False,True]:
      for protect in [False,True]:
       page.evaluate('(v)=>{setFlipped(v.flip);document.getElementById("protectLowerThird").checked=v.protect;document.getElementById("allowMediaOverlap").checked=true;state.screenOffsets={source:{x:8,y:-8},identity:{x:0,y:0},bullet:{x:0,y:0}};draw()}',dict(flip=flip,protect=protect))
       before=page.evaluate('zeSafeLayout()');placement=page.locator('#postTextPlacement').input_value();mode=page.locator('#postContentMode').input_value()
       page.locator('#postVideos').uncheck();after=page.evaluate('zeSafeLayout()')
       assert before==after,(layout,filename,solo,flip,protect,before,after)
       assert page.evaluate('zeVisualItems().length===0 && zePostRollText()===zeCleanPostText(document.getElementById("postBody").value)')
       assert page.locator('#postTextPlacement').input_value()==placement and page.locator('#postContentMode').input_value()==mode
       assert page.locator('#portraitLayout').input_value()==layout
       page.locator('#postVideos').check();assert page.evaluate('zeSafeLayout()')==before
       assert page.evaluate('zePostRollText()!==""')==(placement=='roll')
    print(layout,filename,'stable frame/header/side after Include videos off/on, with original text fallback: passed',flush=True)
   # Individual media exclusion and explicit hiding use the same policy.
   page.get_by_role('checkbox',name='Include Video 1',exact=True).uncheck();assert page.evaluate('!!zePostRollText()')
   page.locator('#postTextPlacement').select_option('hidden');assert page.evaluate('zePostRollText()===""')
   page.get_by_role('checkbox',name='Include Video 1',exact=True).check();page.locator('#postTextPlacement').select_option('roll')
  # New text-only imports still use the prior larger text-only solo treatment.
  page.locator('#portraitLayout').select_option('reference',force=True);page.locator('#showBullets').uncheck()
  page.evaluate('''async(text)=>zeCommitPost(await zePreparePost({text,attachments:[]}))''',text)
  assert page.evaluate('getBBox("source").w===402 && zeReferenceMediaFrame()')
  assert not errors and not page.evaluate('state.renderError'),errors
  browser.close();print('Main default, individual exclusions, explicit Hide post text, restored media routing and fixed text-only layout: passed',flush=True)
finally:server.shutdown();server.server_close()
