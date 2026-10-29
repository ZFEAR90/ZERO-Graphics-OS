"""Post text routing, filled native-aspect frames, solo inset header, joint scroll, safe black panels."""
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
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source')
  page.locator('#portraitLayout').select_option('focus')  # Explicit legacy adaptive treatment; reference default has its own check.
  def panel_pixels():
   for flip in [False,True]:
    for protect in [False,True]:
     for move in [0,100,250]:
      result=page.evaluate('''(v)=>{document.getElementById('protectLowerThird').checked=v.protect;document.getElementById('compositionY').value=v.move;state.layers.bullet.scale=v.move===250?1.3:1;setFlipped(v.flip);setT(5);const a=c.getImageData(0,0,1920,1080).data,oldA=zeAdaptiveBullet,oldR=zeSafeReferenceBullet;zeAdaptiveBullet=()=>{};zeSafeReferenceBullet=()=>{};draw();const b=c.getImageData(0,0,1920,1080).data;zeAdaptiveBullet=oldA;zeSafeReferenceBullet=oldR;draw();let changed=0,outside=0;const bottom=zeBroadcastBounds().bottom*2;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3]){changed++;if(Math.floor(i/4/1920)>=bottom)outside++}return {changed,outside,box:zeVisibleBounds('bullet',getBBox('bullet')),bottom:zeBroadcastBounds().bottom}}''',{'flip':flip,'protect':protect,'move':move})
      assert result['changed']>0 and result['outside']==0,result
      assert result['box']['y']+result['box']['h']<=result['bottom']+.01,result
   page.evaluate("document.getElementById('compositionY').value=0;document.getElementById('protectLowerThird').checked=false;state.layers.bullet.scale=1;setFlipped(false)")
  panel_pixels()
  text='خبر أصلي قابل للتحرير مع صورة أو فيديو. https://t.co/example\n\nتفاصيل إضافية عن الحدث.'
  page.evaluate('''async(text)=>{const prepared=await zePreparePost({text,attachments:[{type:'video',url:'/fixtures/landscape.mp4'}]});zeCommitPost(prepared)}''',text)
  assert page.locator('#postTextPlacement').input_value()=='bullet' and page.locator('#postMediaFit').input_value()=='fill'
  assert page.locator('#bullets').input_value()==page.locator('#postBody').input_value() and 'http' not in page.locator('#bullets').input_value()
  assert page.evaluate('zePostRollText()==="" && zePost.bulletLinked')
  b=page.evaluate('getBBox("source")');a=page.evaluate('zeBroadcastBounds()');assert b['y']>140 and a['top']<b['y']+b['h']<a['top']+30,b
  def native_body():
   result=page.evaluate('''(()=>{const b=getBBox('source'),item=zePrimaryMedia(),w=b.w*365/402,h=b.h*372/398-(zeEmbeddedHeader()?zeEmbeddedBand():0);return {frameRatio:w/h,mediaRatio:item.width/item.height}})()''');assert abs(result['frameRatio']-result['mediaRatio'])<.00001,result
  native_body();panel_pixels();print('Black panel and text protected through flips/movement/scales, real post copied to bullets, filled balanced frame: passed',flush=True)
  # Custom bullet edits survive text being returned to the roll; unmodified copied text moves cleanly.
  page.locator('#bullets').fill('نص تحريري مختلف');page.locator('#postTextPlacement').select_option('roll');assert page.locator('#bullets').input_value()=='نص تحريري مختلف';assert page.evaluate('zeScrollTogether() && zePinnedVideos().length===0')
  positions=[]
  for time in [5,30]:
   positions.append(page.evaluate('''(t)=>{const ctx=document.createElement('canvas').getContext('2d'),old=zeDrawFramedMedia,oldText=CanvasRenderingContext2D.prototype.drawImage;let media=null,documentY=null;zeDrawFramedMedia=(c,frame,x,y,w,h,item)=>{media={y:c.getTransform().f+y*c.getTransform().d};return old(c,frame,x,y,w,h,item)};CanvasRenderingContext2D.prototype.drawImage=function(frame,...args){if(frame===zePost.doc)documentY=this.getTransform().f;return oldText.call(this,frame,...args)};try{zeDrawPost(ctx,0,0,400,160,t)}finally{zeDrawFramedMedia=old;CanvasRenderingContext2D.prototype.drawImage=oldText}return {media,documentY}}''',time))
  assert positions[1]['media']['y']<positions[0]['media']['y'] and abs((positions[1]['media']['y']-positions[0]['media']['y'])-(positions[1]['documentY']-positions[0]['documentY']))<.01,positions
  page.locator('#copyPostToBullets').click();copied=page.locator('#bullets').input_value();assert copied==page.locator('#postBody').input_value();page.locator('#postTextPlacement').select_option('roll');assert page.locator('#bullets').input_value()==''
  page.locator('#postTextPlacement').select_option('hidden');assert page.evaluate('zePostRollText()===""');page.locator('#copyPostToBullets').click()
  page.locator('#postContentMode').select_option('media');page.locator('#postTextPlacement').select_option('roll');assert page.locator('#postContentMode').input_value()=='all' and page.evaluate('!!zePostRollText()')
  page.locator('#copyPostToBullets').click();page.locator('#postMediaFit').select_option('fit');assert page.locator('#postMediaFit').input_value()=='fit';assert page.evaluate('(()=>{const p=zeProtectedPlacement({width:360,height:640},240,300,{framing:{zoom:140,face:{x:20,y:5,w:60,h:55}}});return p.scale===p.base})()');page.locator('#postMediaFit').select_option('fill')
  assert page.evaluate('(()=>{const ctx=document.createElement("canvas").getContext("2d"),calls=[];ctx.fillText=(word,x)=>calls.push({word,x});drawJustified(ctx,"First second third",300,40,250,"none",0,1,false);return calls[0].word==="First" && calls[0].x<calls[1].x && calls[1].x<calls[2].x})()')
  print('Edited bullets preserved, copied text movable, joined text/media scroll, Fill/Fit and hidden text choices: passed',flush=True)
  # Wide solo card reserves a header strip and overlaps the platform at its upper right.
  page.locator('#showBullets').uncheck();page.evaluate('setT(5)');assert page.evaluate('zeEmbeddedHeader()');native_body()
  layout=page.evaluate('''(()=>{const b=getBBox('source'),head=getBBox('identity'),l=headerLayout(c),k=head.w/R.identity.w,box=p=>({x:head.x+(p.x-R.identity.x)*k,y:head.y+(p.y-R.identity.y)*k,w:p.w*k,h:p.h*k});return {source:b,platform:box(l.platform),avatar:box(l.avatar),name:box(l.name),handle:box(l.handle)}})()''');s=layout['source'];logo=layout['platform'];assert logo['x']<s['x']+s['w']<logo['x']+logo['w'] and logo['y']<s['y']<logo['y']+logo['h'],layout
  for key in ['avatar','name','handle']:
   box=layout[key];assert s['x']<=box['x'] and box['x']+box['w']<=s['x']+s['w'] and s['y']<box['y'],layout
  before=page.evaluate('zeSafeLayout()');page.evaluate('state.screenOffsets.source={x:0,y:-35};draw()');after=page.evaluate('zeSafeLayout()');assert abs(after['source']['y']-before['source']['y']+35)<.01 and abs(after['identity']['y']-before['identity']['y']+35)<.01
  page.evaluate('state.screenOffsets.source={x:0,y:0};state.screenOffsets.identity={x:200,y:200};draw()');assert page.evaluate('zeEmbeddedHeader()');page.evaluate('selectLayer("identity")');assert page.evaluate('state.selected==="source"')
  page.evaluate('state.screenOffsets.source={x:0,y:0}');page.locator('#respectSafeArea').click();assert page.evaluate('getBBox("source").y+getBBox("source").h<=zeBroadcastBounds().bottom+.01');native_body()
  print('Solo native-aspect filled media, inset account/profile, overlapping top-right platform, movement and strict bounds: passed',flush=True)
  # Photos use the same native sizing; no text choice is lost when media is replaced.
  page.locator('#respectSafeArea').click();page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures/photo.png'));page.wait_for_function('zePost.items[0].type==="image"');native_body();page.locator('#postBody').fill('صورة مع نص قابل للاختيار');page.locator('#copyPostToBullets').click()
  with page.expect_download() as download:page.locator('#saveJson').click()
  download.value.save_as('/tmp/ze-beta272.json');saved=json.loads(Path('/tmp/ze-beta272.json').read_text());assert saved['headerAnchor']=='inside-roll' and saved['safeArea']['bulletPanelAlwaysProtected'] and saved['postMedia']['textPlacement']=='bullet' and saved['postMedia']['fit']=='fill'
  page.set_viewport_size({'width':780,'height':1000});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not page.evaluate('state.renderError') and not errors,errors;print('Photo geometry and saved text-placement, fitting, header and panel policies: passed',flush=True);browser.close()
finally:server.shutdown();server.server_close()
