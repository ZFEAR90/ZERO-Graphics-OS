from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import threading,json,base64,subprocess,importlib.util
spec=importlib.util.spec_from_file_location("helper",Path(__file__).resolve().parents[1]/"ze_local_importer.py");helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
root=Path(__file__).resolve().parents[1];fixture=root/'tests'/'fixtures'
class Handler(helper.Handler):
 def do_GET(self):
  if self.path.startswith('/fixtures/'):
   return self._send_media(fixture/Path(self.path).name)
  else:super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1600,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('assets.avatar && state.stvLoaded')
  page.locator('#portraitLayout').select_option('focus')  # Explicit legacy adaptive treatment; reference default has its own check.
  page.locator('#postMediaFit').select_option('fit',force=True)
  assert not page.evaluate('state.renderError');assert not errors,errors
  page.locator('.control-panel').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
  page.locator('.editor-tab-panel').evaluate_all('(els)=>els.forEach(el=>el.hidden=false)');page.locator('.element-overrides').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
  avatar=page.evaluate('assets.avatar.src');photo='data:image/png;base64,'+base64.b64encode((fixture/'photo.png').read_bytes()).decode()
  payload={'name':'Real Test Author','handle':'author','platform':'Facebook','text':'A public post with independently editable photos and video.','avatar_data':avatar,'status':'partial','attachments':[{'type':'image','data_url':photo},{'type':'video','url':'/fixtures/landscape.mp4'}]}
  page.route('**/api/health',lambda route:route.fulfill(content_type='application/json',body=json.dumps({'service':'ze-os-importer','version':'0.7-beta2.3'})))
  page.route('**/api/post?*',lambda route:route.fulfill(content_type='application/json',body=json.dumps(payload)))
  page.locator('#postUrl').fill('https://www.facebook.com/author/posts/123');page.locator('#importPost').click()
  page.wait_for_function('zePost.active && zePost.items.length===2')
  assert page.locator('#displayname').input_value()=='Real Test Author'
  page.evaluate('setT(4)');page.locator('#canvas').screenshot(path='/tmp/ze-media-with-bullets.png')
  for flipped in [False,True]:
   page.evaluate('(v)=>setFlipped(v)',flipped)
   boxes=page.evaluate('zePostBoxes()');src=boxes['source'];bullet=boxes['bullet'];head=boxes['identity']
   assert abs(src['y']-bullet['y'])<.01 and abs(src['h']-bullet['h'])<.01
   assert head['y']+head['h']<src['y']
   assert abs(head['x']-src['x'])<.01 if flipped else abs(head['x']+head['w']-src['x']-src['w'])<.01
   assert (bullet['x']>=src['x']+src['w']) if flipped else (bullet['x']+bullet['w']<=src['x'])
  page.locator('#postVideos').uncheck();assert page.evaluate('zeVisualItems().length')==1
  page.locator('#postPhotos').uncheck();assert page.evaluate('zeVisualItems().length')==0
  page.locator('#postVideos').check();page.locator('#postContentMode').select_option('media')
  page.locator('#canvas').screenshot(path='/tmp/ze-media-video-only.png')
  page.locator('#showBullets').uncheck();assert page.evaluate('getBBox("bullet").w')==0
  assert page.evaluate('(()=>{const bs=["source","identity"].map(n=>zeVisibleBounds(n,getBBox(n)));return Math.abs((Math.min(...bs.map(b=>b.x))+Math.max(...bs.map(b=>b.x+b.w)))/2-480)<.01})()')
  page.locator('#showBullets').check()
  page.evaluate('setT(2.88)');page.wait_for_function('Math.abs(zePost.items[1].el.currentTime-1)<.1')
  assert page.evaluate('zePost.items[1].el.paused')
  page.locator('#play').click();page.wait_for_timeout(250);assert page.evaluate('!zePost.items[1].el.paused');page.locator('#play').click();page.wait_for_timeout(100);assert page.evaluate('zePost.items[1].el.paused')
  page.locator('#postAudio').check();page.wait_for_function('zePost.audio && zePost.audio.state==="running"')
  for audio in [True,False]:
   page.locator('#postAudio').set_checked(audio)
   with page.expect_download(timeout=25000) as recording:page.locator('#record').click()
   path=f'/tmp/ze-post-audio-{audio}.webm';recording.value.save_as(path)
   result=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type','-of','json',path]))
   types=[stream['codec_type'] for stream in result['streams']];assert ('audio' in types)==audio,(audio,types)
   print('RECORD audio',audio,types)
  page.locator('#postFiles').set_input_files([str(fixture/'portrait.png'),str(fixture/'audio.wav')])
  page.wait_for_function('zePost.items.length===4')
  page.locator('#postFiles').set_input_files(str(fixture/'portrait.mp4'));page.wait_for_function('zePost.items.length===5')
  page.evaluate('zePost.items[0].enabled=false;zePost.items[1].enabled=false;zePost.items[2].enabled=false;zeRefreshMediaList();zeInvalidatePost();setT(2.88)')
  assert page.evaluate('getBBox("source").w')<300
  page.locator('#canvas').screenshot(path='/tmp/ze-media-portrait.png')
  page.locator('#postAudio').check();page.wait_for_function('zePost.items[3].gain && zePost.items[4].gain')
  page.locator('#postVideos').uncheck();page.wait_for_timeout(100)
  assert page.evaluate('zeVisualItems().length')==0
  assert page.evaluate('zePost.items[4].gain.gain.value')==1
  page.evaluate('zePost.items[4].enabled=false');page.wait_for_timeout(100);assert page.evaluate('zePost.items[4].gain.gain.value')==0
  assert page.evaluate('zePost.items[3].gain.gain.value')==1
  print('Portrait reflow, multi-file upload, standalone audio, and audio without visible video passed')
  assert not page.evaluate('state.renderError');assert not errors,errors
  print('Import, individual media toggles, linked layout, flip, centering, video seeking/play/pause, local upload, and audio export passed')
  browser.close()
finally:server.shutdown();server.server_close()
