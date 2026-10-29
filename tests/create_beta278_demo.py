"""Reproducible UI walkthrough + actual 50-second opaque WebM (fixture import)."""
from pathlib import Path
from http.server import ThreadingHTTPServer
import importlib.util,threading,json,subprocess
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];out=root/'demo';out.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('helper',root/'ze_local_importer.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
class Handler(helper.Handler):
 def do_GET(self):
  if self.path.startswith('/fixtures/'):return self._send_media(root/'tests/fixtures'/Path(self.path).name)
  super().do_GET()
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);ctx=browser.new_context(viewport={'width':1440,'height':1000},record_video_dir='/tmp/ze-demo278',record_video_size={'width':1440,'height':1000});page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('assets.source && state.stvLoaded');page.evaluate('''()=>{const label=document.createElement('div');label.id='demoCaption';label.style.cssText='position:fixed;bottom:158px;left:410px;right:22px;z-index:100;background:#160e20ee;color:white;padding:14px;border:1px solid #ca5277;border-radius:8px;font:16px Arial;pointer-events:none';document.body.append(label)}''')
  def caption(text,wait=800):page.locator('#demoCaption').evaluate('(el,text)=>el.textContent=text',text);page.wait_for_timeout(wait)
  def open_panel(key):page.locator('[data-panel="'+key+'"]').evaluate('(el)=>el.open=true')
  caption('Main roll · Beta 2.7.8 recovery · approved Mouwajaha V0.7 base')
  payload={'platform':'X','name':'Fixture broadcast account','handle':'mainroll_demo','text':'نص المنشور العربي داخل الرول. يحافظ التصميم على مساحة الأخبار ويعرض الصورة بجانب النص. '*4,'attachments':[{'type':'image','url':'/fixtures/portrait.png'}]}
  page.route('**/api/post?*',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(payload)))
  open_panel('import');page.locator('#postUrl').fill('https://x.com/mainroll_demo/status/123456789');caption('Import a post · controlled local fixture; no claim of live platform extraction');page.locator('#importPost').click();page.wait_for_function('zePost.active');page.evaluate('setT(5)');caption('Main roll · portrait media right / text left · reference frame size')
  page.locator('#bullets').fill('الخبر الأول يبقى داخل اللوحة السوداء\n\nالخبر الثاني ينتقل بسلاسة');page.evaluate("document.getElementById('bulletSplitMode').value='blank';zeUpdateParagraphEditor()");page.locator('#canvas').screenshot(path=str(out/'ZE_OS_V07_Beta278_Main.png'))
  open_panel('postmedia');page.locator('#postMediaFit').select_option('fit');caption('Fit shows the complete image inside the same frame');page.locator('#postMediaFit').select_option('fill');caption('Fill covers the frame · manual protected crop remains available')
  page.locator('#postTextPlacement').select_option('bullet');caption('Post text outside the roll · editable bulletin');page.locator('#postTextPlacement').select_option('roll');caption('Post text inside · bulletin content is preserved')
  page.locator('#showBullets').uncheck();caption('Bullet off · centered roll');page.locator('#showBullets').check();page.locator('#flip').check();caption('Flip swaps composition · text and media pixels keep their orientation');page.locator('#flip').uncheck()
  page.locator('#useWholePost').click();page.locator('#showBullets').uncheck();caption('Whole roll frame · pinned account inside · text/media scroll together');page.locator('#canvas').screenshot(path=str(out/'ZE_OS_V07_Beta278_Whole.png'));page.evaluate('setT(25)');caption('Whole post movement · account row remains pinned');page.evaluate('setT(5)')
  for file,label in [('photo.png','Landscape media'),('portrait.png','Portrait media')]:
   page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures'/file));page.wait_for_function('zePost.items.length===1');page.evaluate('setT(5)');caption(label+' · Whole roll frame')
  page.evaluate('''async()=>{const a=document.createElement('canvas');a.width=a.height=400;const c=a.getContext('2d');c.fillStyle='#168fb5';c.fillRect(0,0,400,400);c.fillStyle='#f2d368';c.fillRect(20,20,160,360);zeCommitPost(await zePreparePost({text:'Square media inside Main roll',attachments:[{type:'image',url:a.toDataURL()}]}));setT(5)}''');caption('Square media · same frame and editable Fill/Fit')
  page.locator('#useMainRoll').click();page.locator('#showBullets').check();page.evaluate("document.getElementById('protectLowerThird').checked=false;zeUpdateSafePreview();setT(5)")
  # Real mouse move followed by toolbar undo/redo.
  page.evaluate("selectLayer('source')");b=page.evaluate("getBBox('source')");r=page.locator('#canvas').bounding_box();x=r['x']+(b['x']+b['w']/2)/960*r['width'];y=r['y']+(b['y']+b['h']/2)/540*r['height'];page.mouse.move(x,y);page.mouse.down();page.mouse.move(x-30,y-20,steps=15);page.mouse.up();caption('Drag roll · movement saved as one history step');page.locator('#undoEdit').click();caption('Undo restores the move');page.locator('#redoEdit').click();caption('Redo reapplies it');page.locator('#undoEdit').click()
  page.locator('#respectSafeArea').click();caption('Respect safe area On · bullet text always protected');page.locator('#respectSafeArea').click();caption('Safe area Off · roll can use lower-third space; bulletin stays protected')
  page.locator('#backgroundFile').set_input_files(str(root/'tests/fixtures/portrait.png'));page.wait_for_timeout(200);caption('Loop/image palette · automatic three-color adaptation');page.locator('#accentColor').evaluate("el=>{el.value='#dd8b25';el.dispatchEvent(new Event('input',{bubbles:true}))}");caption('Manual primary color override · individual overrides under Advanced')
  page.evaluate("async()=>{zeCommitPost(await zePreparePost({text:'تتابع الصور والفيديو داخل نفس الإطار دون انعكاس. ',attachments:[{type:'video',url:'/fixtures/portrait.mp4'},{type:'image',url:'/fixtures/photo.png'},{type:'video',url:'/fixtures/landscape.mp4'}]}));document.getElementById('postScrollMode').value='fixed';document.getElementById('bullets').value='الفقرة الأولى تدخل سطراً بعد سطر وتخرج بالاتجاه المعاكس.\\n\\nالفقرة الثانية تبقى حتى نهاية الفيديو.';document.getElementById('bulletSplitMode').value='blank';zeSetVideoDuration(50);setT(5)}");page.wait_for_function('zePost.items.filter(i=>i.type==="video").every(i=>i.el.readyState>=2&&!i.el.seeking)')
  slot=page.evaluate('(timeline(DURATION)-val("sourceTiming")-1.88)/3')
  caption('Multiple media · smooth directional mask, complementary reveal, final item holds')
  for flip in [False,True]:
   page.evaluate('(v)=>setFlipped(v)',flip)
   for n in range(24):page.evaluate('(t)=>setT(t)',1.88+slot+n/25);page.wait_for_timeout(25)
  page.evaluate("setFlipped(false);zeSyncParagraphs();zeParagraphModel.items[0].manual=2;zeParagraphModel.cache=null;setT(5)");start=page.evaluate('zeParagraphSchedule().rows[0].exitStart');caption('Paragraph handoff · staggered lines overlap inside the black mask')
  for n in range(35):page.evaluate('(t)=>setT(t)',start+n/25);page.wait_for_timeout(25)
  caption('Final browser render · actual 50-second opaque WebM · native MOV alpha is deferred')
  page.evaluate("document.getElementById('postAudio').checked=true;zeSetVideoDuration(50);document.getElementById('safeAreas').checked=false;zeUpdateSafePreview();draw()")
  with page.expect_download(timeout=90000) as video:page.locator('#renderVideo').click()
  video.value.save_as(str(out/'ZE_OS_V07_Beta278_50s.webm'));assert page.evaluate('state.t')==50 and not page.evaluate('state.recording');caption('Render complete · 50 seconds · final paragraph and media hold',1000)
  assert not errors and not page.evaluate('state.renderError'),errors
  recording=page.video;ctx.close();recording.save_as(str(out/'ZE_OS_V07_Beta278_Walkthrough.webm'));browser.close()
 subprocess.run(['ffmpeg','-y','-i',str(out/'ZE_OS_V07_Beta278_Walkthrough.webm'),'-c:v','libx264','-preset','fast','-crf','24','-pix_fmt','yuv420p',str(out/'ZE_OS_V07_Beta278_Demo.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 print('Walkthrough MP4, real 50-second WebM and Main/Whole screenshots saved.',flush=True)
finally:server.shutdown();server.server_close()
