"""Whole roll uses a pinned native top-left account row, with no broadcast header straps."""
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
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source');page.locator('#useWholePost').click();page.locator('#showBullets').uncheck()
  page.evaluate('''async()=>{zeCommitPost(await zePreparePost({text:'نص طويل داخل المنشور يتحرك دون أن تتغير مواضع صورة الحساب واسمه. '.repeat(25),attachments:[{type:'video',url:'/fixtures/landscape.mp4'}]}));document.getElementById('displayname').value='Native post account';document.getElementById('account').value='@PinnedAccount'}''');page.wait_for_function('zePost.items[0].el.readyState>=2 && !zePost.items[0].el.seeking')
  def geometry():
   return page.evaluate('''(()=>{const source=getBBox('source'),head=getBBox('identity'),local=headerLayout(c),k=head.w/R.identity.w,p=b=>({x:head.x+(b.x-R.identity.x)*k,y:head.y+(b.y-R.identity.y)*k,w:b.w*k,h:b.h*k});return {source,avatar:p(local.avatar),name:p(local.name),handle:p(local.handle),platform:p(local.platform)}})()''')
  first=None
  for flipped in [False,True]:
   page.evaluate('(v)=>setFlipped(v)',flipped);g=geometry();s=g['source'];a=g['avatar']
   assert abs(a['x']-(s['x']+s['w']*(1-365/402)/2+10))<.01 and abs(a['y']-(s['y']+s['h']*(1-372/398)/2+10))<.01,g
   assert g['name']['x']>a['x']+a['w'] and g['handle']['x']==g['name']['x'],g
   assert g['platform']['x']+g['platform']['w']<s['x'] if flipped else g['platform']['x']>s['x']+s['w'],g
   if first:
    for key in ['avatar','name','handle']:assert g[key]==first[key],(first,g)
   else:first=g
   for arrangement in ['right','below']:
    page.locator('#wholeFrameArrangement').select_option(arrangement)
    snapshots=[]
    for t in [5,25,49.96]:
     snapshots.append(page.evaluate('''(t)=>{setT(t);const h=getBBox('identity'),l=headerLayout(c),k=h.w/R.identity.w,x=Math.floor((h.x+(l.avatar.x-R.identity.x)*k)*2),y=Math.floor((h.y+(l.avatar.y-R.identity.y)*k)*2),w=Math.ceil((Math.max(l.name.x+l.name.w,l.handle.x+l.handle.w)-l.avatar.x)*k*2),height=Math.ceil(zeSocialBand()*2-20),ctx=document.createElement('canvas').getContext('2d');ctx.canvas.width=w;ctx.canvas.height=height;ctx.drawImage(cvs,x,y,w,height,0,0,w,height);return ctx.canvas.toDataURL()}''',t))
    assert snapshots[0]==snapshots[1]==snapshots[2],(flipped,arrangement,'Account row scrolled or changed')
   # Check real painted labels have white space around dark glyphs, with no solid strap.
   result=page.evaluate('''(()=>{setT(5);const h=getBBox('identity'),l=headerLayout(c),k=h.w/R.identity.w,b=l.name,x=Math.floor((h.x+(b.x-R.identity.x)*k)*2),y=Math.floor((h.y+(b.y-R.identity.y)*k)*2),w=Math.max(1,Math.floor(b.w*k*2)),height=Math.max(1,Math.floor(b.h*k*2)),a=c.getImageData(x,y,w,height).data;let white=0,dark=0;for(let i=0;i<a.length;i+=4){if(a[i]>245&&a[i+1]>245&&a[i+2]>245)white++;if(a[i]<100&&a[i+1]<100&&a[i+2]<100)dark++}return {white: white/(w*height),dark:dark/(w*height)}})()''');assert result['white']>.55 and 0<result['dark']<.4,result
   calls=page.evaluate('''(()=>{const old=headerLabel;let calls=0;headerLabel=(...args)=>{calls++;old(...args)};draw();headerLabel=old;return calls})()''');assert calls==0,calls
  # Native row stays padded inside the resized roll at large requested avatar/label scales.
  for flip in [False,True]:
   page.evaluate('(v)=>setFlipped(v)',flip)
   for scale in [.3,1.2]:
    old=page.evaluate("({source:state.layers.source.scale,avatar:val('avatarScale'),label:val('labelScale'),group:val('headerGroupScale')})")
    page.evaluate("v=>{state.layers.source.scale=v;document.getElementById('avatarScale').value=250;document.getElementById('labelScale').value=250;document.getElementById('headerGroupScale').value=150;draw()}",scale);g=geometry();source=g['source']
    for name in ['avatar','name','handle']:
     a=g[name];assert a['x']>=source['x']+8 and a['y']>=source['y']+8 and a['x']+a['w']<=source['x']+source['w']-8 and a['y']+a['h']<=source['y']+source['h']-8,g
    assert page.evaluate('headerLayout(c).platform.w')==66
    page.evaluate("v=>{state.layers.source.scale=v.source;document.getElementById('avatarScale').value=v.avatar;document.getElementById('labelScale').value=v.label;document.getElementById('headerGroupScale').value=v.group;draw()}",old)
  page.locator('#postTextPlacement').select_option('hidden');assert geometry()['avatar']==first['avatar']
  page.locator('#postTextPlacement').select_option('roll');page.locator('#displayname').fill('اسم عربي قابل للتحرير');page.locator('#account').fill('@EditedAccount');page.evaluate('setT(5)');assert page.evaluate('headerLayout(c).nameText')=='اسم عربي قابل للتحرير'
  with page.expect_download() as output:page.locator('#saveJson').click()
  output.value.save_as('/tmp/ze-beta277-native.json');saved=json.loads(Path('/tmp/ze-beta277-native.json').read_text());assert saved['headerAnchor']=='native-post-top-left' and saved['socialPost']['accountPinned'] and saved['socialPost']['accountStyle']=='plain native row'
  page.locator('#useMainRoll').click();calls=page.evaluate('''(()=>{const old=headerLabel;let calls=0;headerLabel=(...args)=>{calls++;old(...args)};draw();headerLabel=old;return calls})()''');assert calls>0
  assert not errors and not page.evaluate('state.renderError'),errors;browser.close();print('Native account at top-left in both flips; identical row pixels during right/below scrolling; no straps; editable fields and native-row JSON; Main header preserved: passed',flush=True)
finally:server.shutdown();server.server_close()
