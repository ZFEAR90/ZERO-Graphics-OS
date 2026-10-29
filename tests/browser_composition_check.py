"""Caption-first cards, centered portrait groups, anchored headers and mandatory text safe mask."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading,json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source')
  page.locator('#bullets').fill('هذا نص طويل لاختبار عدم عبور أي سطر إلى منطقة الخبر العاجل. '*12+'\n\nالنص الأخير يبقى فوق الخط الآمن. '*8)
  def check_pixels(moves=(0,100,250),protections=(False,True)):
   for flip in [False,True]:
    for protected in protections:
     for move in moves:
      result=page.evaluate('''(v)=>{document.getElementById('protectLowerThird').checked=v.protected;document.getElementById('compositionY').value=v.move;setFlipped(v.flip);const plan=zeParagraphSchedule();let changed=0,outside=0;for(const t of [plan.rows[0].entryEnd+.2,plan.rows[0].exitStart+.2,49.9]){setT(t);const a=c.getImageData(0,0,1920,1080).data,good=zeDrawParagraphText;zeDrawParagraphText=()=>{};draw();const b=c.getImageData(0,0,1920,1080).data;zeDrawParagraphText=good;draw();const bottom=zeBroadcastBounds().bottom*2;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3]){changed++;if(Math.floor(i/4/1920)>=bottom)outside++}}return {changed,outside}}''',{'flip':flip,'protected':protected,'move':move})
      assert result['changed']>0 and result['outside']==0,(flip,protected,move,result)
   page.evaluate("document.getElementById('protectLowerThird').checked=false;document.getElementById('compositionY').value=0;setFlipped(false)")
  check_pixels();print('Reference bulletin text stays above lower third through flips/movement/protection modes',flush=True)
  for mode,field in [('regular','lowerThirdTop'),('breaking','breakingNewsTop')]:
   page.evaluate('(v)=>{document.getElementById("lowerThirdMode").value=v.mode;document.getElementById(v.field).value=740}',{'mode':mode,'field':field});check_pixels(moves=(100,),protections=(False,));page.evaluate('(id)=>document.getElementById(id).value=847',field)
  page.evaluate('document.getElementById("lowerThirdMode").value="breaking"')
  page.evaluate("async()=>{document.getElementById('postUrl').value='https://x.com/source/status/123';zeSolo.postUrl=document.getElementById('postUrl').value;const prepared=await zePreparePost({text:'خبر أصلي https://t.co/abc\\nرابط www.example.com/report\\nexample.org/story',attachments:[{type:'image',url:'/tests/fixtures/photo.png'}]});zeCommitPost(prepared)}")
  assert 'http' not in page.locator('#postBody').input_value() and 'example.' not in page.locator('#postBody').input_value()
  page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures/portrait.mp4'));page.wait_for_function('zePost.active')
  page.locator('#postBody').fill('تقرير عن التطورات الجديدة. https://t.co/abc\n\nرابط آخر www.example.com/story\nنص أصلي بلا رابط t.co/XYZ')
  assert page.evaluate("zeCleanPostText(document.getElementById('postBody').value)")=='تقرير عن التطورات الجديدة.\n\nرابط آخر\nنص أصلي بلا رابط'
  page.locator('#postTextPlacement').select_option('roll');page.locator('#postScrollMode').select_option('fixed')
  strings=page.evaluate('''(()=>{const proto=CanvasRenderingContext2D.prototype,old=proto.fillText,text=[];proto.fillText=function(s,...args){text.push(s);return old.call(this,s,...args)};try{zePost.doc=null;zePostDocument()}finally{proto.fillText=old}return text})()''');assert strings and all('http' not in s and 't.co/' not in s and 'www.' not in s for s in strings)
  page.locator('#postTextPlacement').select_option('bullet')
  for mode in ['focus','balanced','beside']:
   page.locator('#portraitLayout').select_option(mode)
   for flip in [False,True]:
    page.evaluate('(v)=>{document.getElementById("protectLowerThird").checked=false;state.screenOffsets={identity:{x:0,y:0},source:{x:0,y:0},bullet:{x:0,y:0}};setFlipped(v);setT(5)}',flip)
    boxes=page.evaluate('zeSafeLayout()');b=boxes['bullet'];h=boxes['identity'];s=boxes['source'];assert h['x']>=b['x']-.01 and h['x']+h['w']<=b['x']+b['w']+.01 and h['y']+h['h']+10<=b['y'],boxes
    if mode=='focus':
     assert s['h']>420 and s['w']>240
     bounds=page.evaluate('(()=>{const bs=["source","bullet","identity"].map(n=>zeVisibleBounds(n,getBBox(n)));return {l:Math.min(...bs.map(b=>b.x)),r:Math.max(...bs.map(b=>b.x+b.w)),t:Math.min(...bs.map(b=>b.y)),b:Math.max(...bs.map(b=>b.y+b.h))}})()');assert abs((bounds['l']+bounds['r'])/2-480)<.01 and abs((bounds['t']+bounds['b'])/2-270)<.01,bounds
    page.evaluate('state.screenOffsets.source={x:18,y:-12};draw()');moved=page.evaluate('zeSafeLayout()');assert moved['identity']==h and moved['bullet']==b
    page.evaluate('state.screenOffsets.source={x:0,y:0};state.screenOffsets.bullet={x:12,y:-10};draw()');moved=page.evaluate('zeSafeLayout()');assert abs(moved['identity']['x']-h['x']-12)<.01 and abs(moved['identity']['y']-h['y']+10)<.01 and moved['source']==s
   print(mode,'header stays above and moves with bullets; roll moves independently',flush=True)
  page.evaluate('state.screenOffsets={identity:{x:0,y:0},source:{x:0,y:0},bullet:{x:0,y:0}}');page.locator('#portraitLayout').select_option('focus');page.locator('#showBullets').uncheck();boxes=page.evaluate('zeSafeLayout()');assert boxes['identity']['y']+boxes['identity']['h']<boxes['source']['y'];page.locator('#showBullets').check()
  check_pixels();print('Imported bulletin text never enters lower third, including tall black panels',flush=True)
  # Every wider fixed-media card places its independently scrolling caption first.
  for filename in ['photo.png','landscape.mp4']:
   page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures'/filename));page.wait_for_function('(name)=>zePost.items.length===1 && zePost.items[0].label===name',arg=filename);page.locator('#postBody').fill('هذه فقرة فوق الصورة وليست تحتها. '*12);page.locator('#postTextPlacement').select_option('roll');page.locator('#postScrollMode').select_option('fixed')
   positions=page.evaluate('''(()=>{const ctx=document.createElement('canvas').getContext('2d'),oldFit=fit,oldDoc=zeDrawPostDocument;let media=null,caption=null;fit=(c,im,x,y,w,h)=>{media={x,y,w,h};oldFit(c,im,x,y,w,h)};zeDrawPostDocument=(c,x,y,w,h,t)=>{caption={x,y,w,h};oldDoc(c,x,y,w,h,t)};try{zeDrawPost(ctx,0,0,400,300,5)}finally{fit=oldFit;zeDrawPostDocument=oldDoc}return {media,caption}})()''');assert positions['caption']['y']+positions['caption']['h']<positions['media']['y'],positions
  # A crop cannot exclude the full manually protected face rectangle. Full frame is the default.
  result=page.evaluate('''(()=>{const frame={width:360,height:640},item={framing:{zoom:140,face:{x:0,y:0,w:100,h:100}}},full=zeProtectedPlacement(frame,240,300,item);if(full.scale!==full.base)throw Error('Full frame cropped');for(const face of [{x:20,y:5,w:60,h:55},{x:80,y:0,w:20,h:25},{x:0,y:70,w:25,h:30}])for(const target of [[240,300],[400,200],[140,400]]){item.framing.face=face;const p=zeProtectedPlacement(frame,...target,item),f=p.face;if(p.x+f.x*p.w<-.001||p.y+f.y*p.h<-.001||p.x+(f.x+f.w)*p.w>target[0]+.001||p.y+(f.y+f.h)*p.h>target[1]+.001)throw Error('Protected face clipped')}return true})()''');assert result
  page.get_by_text('Framing / protect face',exact=True).click()
  zoom=page.get_by_role('spinbutton',name='Zoom for landscape.mp4',exact=True);zoom.fill('130');zoom.press('Tab');assert page.evaluate('zePost.items[0].framing.zoom')==130
  page.get_by_role('spinbutton',name='Face left for landscape.mp4',exact=True).fill('20');page.get_by_role('spinbutton',name='Face left for landscape.mp4',exact=True).press('Tab');assert page.get_by_role('spinbutton',name='Face width for landscape.mp4',exact=True).input_value()=='80'
  with page.expect_download() as download:page.locator('#saveJson').click()
  download.value.save_as('/tmp/ze-beta271.json');saved=json.loads(Path('/tmp/ze-beta271.json').read_text());assert saved['sourceUrl']=='https://x.com/source/status/123' and saved['headerAnchor']=='bullet'
  assert saved['safeArea']['bulletTextAlwaysProtected'] and saved['postMedia']['items'][0]['framing']['zoom']==130 and 'http' not in saved['postMedia']['text']
  assert not page.evaluate('state.renderError') and not errors,errors
  print('Caption-first photos/videos, cleaned URLs, optional protected-region crop and JSON: passed',flush=True);browser.close()
finally:server.shutdown();server.server_close()
