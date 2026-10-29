"""Whole-frame wide media below text scrolls as one post, then holds centered."""
from pathlib import Path
from http.server import ThreadingHTTPServer
import importlib.util,threading,json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('helper',root/'ze_local_importer.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
class Handler(helper.Handler):
 def do_GET(self):
  if self.path.startswith('/fixtures/'):return self._send_media(root/'tests/fixtures'/Path(self.path).name)
  super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source');page.locator('#useWholePost').click()
  page.evaluate('''async()=>zeCommitPost(await zePreparePost({text:'نص طويل يتحرك إلى الأعلى مع الفيديو، ثم يبقى الفيديو في منتصف الرول. '.repeat(15),attachments:[{type:'video',url:'/fixtures/landscape.mp4'}]}))''');page.wait_for_function('zePost.items[0].el.readyState>=2')
  assert page.evaluate('zeAutoPostPosition()')=='right' and not page.evaluate('zeWholeBelowMotion()')
  page.locator('#wholeFrameArrangement').select_option('below');assert page.evaluate('zeWholeBelowMotion()')
  for duration in [8,50]:
   page.evaluate('(d)=>{zeSetVideoDuration(d);document.getElementById("scrollStart").value=d===8?2:7;document.getElementById("scrollDuration").value=d===8?4:48}',duration)
   for flip in [False,True]:
    page.evaluate('(v)=>setFlipped(v)',flip)
    samples=[page.evaluate('(t)=>zeWholeBelowPositions(100,180,600,260,t)',t) for t in [0,duration*.6,duration-1,duration]]
    assert samples[1]['text']['y']<samples[0]['text']['y'] and samples[1]['media']['y']<samples[0]['media']['y']
    for sample in samples:assert abs(sample['text']['y']-samples[0]['text']['y']-(sample['media']['y']-samples[0]['media']['y']))<.01,samples
    assert samples[-1]['media']==dict(x=100,y=180,w=600,h=260) and samples[-1]==samples[-2],samples
  # Painted text is safe during shared travel; media may occupy the permitted lower part.
  data=page.evaluate('''(()=>{const old=zeDrawSocialText;let changed=0,outside=0;for(const t of [2.04,5,15,30,45,50]){setT(t);const a=c.getImageData(0,0,1920,1080).data;zeDrawSocialText=()=>{};draw();const b=c.getImageData(0,0,1920,1080).data;zeDrawSocialText=old;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3]){changed++;if(Math.floor(i/4/1920)>=zeBroadcastBounds().bottom*2)outside++}}draw();return {changed,outside}})()''');assert data['changed']>0 and data['outside']==0,data
  with page.expect_download() as output:page.locator('#saveJson').click()
  output.value.save_as('/tmp/ze-beta276-below.json');saved=json.loads(Path('/tmp/ze-beta276-below.json').read_text());assert saved['project']=='Main roll' and saved['postArrangement']['resolved']=='below' and saved['postArrangement']['textScroll']=='together-then-center'
  page.locator('#postTextPlacement').select_option('hidden');assert not page.evaluate('zeWholeBelowMotion()') and page.evaluate('zeSocialRegions(100,180,600,260).media.y===180')
  page.locator('#postTextPlacement').select_option('roll');page.locator('#wholeFrameArrangement').select_option('right');assert not page.evaluate('zeWholeBelowMotion()')
  assert not errors and not page.evaluate('state.renderError'),errors;browser.close();print('Wide below-text post moves text/media together, stops centered before end at 8/50s, supports flip, safe text and Hide/right overrides: passed',flush=True)
finally:server.shutdown();server.server_close()
