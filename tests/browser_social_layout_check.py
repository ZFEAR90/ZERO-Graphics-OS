"""Centered social-post option: side platform, inset identity, independent text scroll and media."""
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
  assert page.locator('#portraitLayout').input_value()=='reference'
  page.locator('#portraitLayout').select_option('social',force=True);assert not page.locator('#showBullets').is_checked() and page.locator('#showBullets').is_disabled()
  text='هذه فقرة طويلة قابلة للتحرير. النص يتحرك داخل مساحته فقط بينما تبقى الصورة والفيديو ظاهرين. '
  for kind,src in [('video','/fixtures/portrait.mp4'),('video','/fixtures/landscape.mp4'),('image','/fixtures/photo.png')]:
   page.evaluate(r'''async(v)=>{zeCommitPost(await zePreparePost({text:(v.text.repeat(4)+'\n\n').repeat(5),attachments:[{type:v.kind,url:v.src}]}));document.getElementById('displayname').value='اسم حساب عربي طويل قابل للتحرير';document.getElementById('account').value='@EditableAccount';setT(5)}''',dict(kind=kind,src=src,text=text))
   if kind=='video':page.wait_for_function('zePost.items[0].el.readyState>=2 && !zePost.items[0].el.seeking')
   assert page.locator('#postTextPlacement').input_value()=='roll' and page.locator('#postScrollMode').is_disabled()
   for flipped in [False,True]:
    page.evaluate('(v)=>setFlipped(v)',flipped)
    layout=page.evaluate('''(()=>{const source=getBBox('source'),head=getBBox('identity'),k=head.w/R.identity.w,local=headerLayout(c),paint=p=>({x:head.x+(p.x-R.identity.x)*k,y:head.y+(p.y-R.identity.y)*k,w:p.w*k,h:p.h*k});return {source,avatar:paint(local.avatar),name:paint(local.name),handle:paint(local.handle),platform:paint(local.platform),bullet:getBBox('bullet')}})()''');s=layout['source'];logo=layout['platform'];assert abs(s['x']+s['w']/2-480)<.01 and layout['bullet']['w']==0
    assert logo['x']+logo['w']<=s['x']-11.99 if flipped else logo['x']>=s['x']+s['w']+11.99,layout
    for key in ['avatar','name','handle']:
     b=layout[key];assert s['x']<=b['x'] and b['x']+b['w']<=s['x']+s['w'] and s['y']<=b['y'] and b['y']+b['h']<s['y']+120,layout
    for position in ['below','right']:
     page.locator('#socialMediaPosition').select_option(position,force=True)
     regions=page.evaluate("zeSocialRegions(100,180,600,300)");t,m=regions['text'],regions['media']
     if position=='below':assert t['y']+t['h']<m['y'] and abs(t['w']-m['w'])<.01
     else:assert t['x']+t['w']<m['x'] and t['x']==100 and m['x']>100
     snapshots=[]
     for time in [5,45]:
      snapshots.append(page.evaluate('''(t)=>{const canvas=document.createElement('canvas');canvas.width=960;canvas.height=540;const ctx=canvas.getContext('2d'),oldText=CanvasRenderingContext2D.prototype.drawImage,oldMedia=zeDrawCleanMedia;let text=null,media=null;CanvasRenderingContext2D.prototype.drawImage=function(im,...args){if(im===zePost.socialDoc?.canvas)text={x:args[0],y:args[1]};return oldText.call(this,im,...args)};zeDrawCleanMedia=(c,im,x,y,w,h,item)=>{media={x,y,w,h};oldMedia(c,im,x,y,w,h,item)};try{zeDrawSocialPost(ctx,100,180,600,300,t)}finally{CanvasRenderingContext2D.prototype.drawImage=oldText;zeDrawCleanMedia=oldMedia}return {text,media}}''',time))
     assert snapshots[1]['text']['y']<snapshots[0]['text']['y'],snapshots
     if page.evaluate('zeWholeBelowMotion()'):assert snapshots[1]['media']['y']<snapshots[0]['media']['y'] and abs((snapshots[1]['media']['y']-snapshots[0]['media']['y'])-(snapshots[1]['text']['y']-snapshots[0]['text']['y']))<.01,snapshots
     else:assert snapshots[0]['media']==snapshots[1]['media'],snapshots
     for fit in ['fit','fill']:
      page.locator('#postMediaFit').select_option(fit);page.evaluate('setT(5)');assert page.evaluate('getBBox("source").w')==s['w']
   print(src,'centered frame, side platform, inset editable identity, two placements, flip and independent scroll: passed',flush=True)
  # Text-only mode and hidden text use all the available body space; all text remains above the lower third.
  page.locator('#postTextPlacement').select_option('hidden');assert page.evaluate('zeSocialRegions(0,100,600,300).text===null')
  page.locator('#postTextPlacement').select_option('roll');page.locator('#postContentMode').select_option('text')
  assert page.evaluate('zeSocialRegions(0,100,600,300).media===null')
  for direction,text in [('rtl','نص عربي طويل فوق الخبر العاجل. '),('ltr','Long English text scrolls above the news safe boundary. ')]:
   page.locator('#postBody').fill(text*90);page.locator('#rollLanguage').select_option(direction)
   result=page.evaluate('''(()=>{const good=zeDrawSocialText;let changed=0,outside=0;for(const t of [2.04,2.2,2.8,5,25,49.96]){setT(t);const a=c.getImageData(0,0,1920,1080).data;zeDrawSocialText=()=>{};draw();const b=c.getImageData(0,0,1920,1080).data;zeDrawSocialText=good;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3]){changed++;if(Math.floor(i/4/1920)>=zeBroadcastBounds().bottom*2)outside++}}draw();return {changed,outside}})()''');assert result['changed']>0 and result['outside']==0,result
  before=page.evaluate('zeSafeLayout()');page.evaluate('state.screenOffsets.source={x:15,y:-20};draw()');after=page.evaluate('zeSafeLayout()');assert after['source']['y']-before['source']['y']==-20 and after['identity']['y']-before['identity']['y']==-20
  # Pointer drag and Ctrl+Z restore the complete source/profile/platform group.
  page.locator('#canvas').scroll_into_view_if_needed();page.evaluate('setT(5);selectLayer("source")');before_drag=page.evaluate('zeSafeLayout()')
  point=page.evaluate('''(()=>{const r=cvs.getBoundingClientRect(),head=getBBox('identity'),local=headerLayout(c).platform,k=head.w/R.identity.w,x=head.x+(local.x-R.identity.x+local.w*.1)*k,y=head.y+(local.y-R.identity.y+local.h*.5)*k;return {x:r.left+x/W*r.width,y:r.top+y/H*r.height}})()''')
  page.mouse.move(point['x'],point['y']);page.mouse.down();page.mouse.move(point['x']+16,point['y']-14,steps=4);page.mouse.up();assert page.evaluate('zeSafeLayout()')!=before_drag
  page.keyboard.press('Control+z');assert page.evaluate('zeSafeLayout()')==before_drag
  with page.expect_download() as output:page.locator('#saveJson').click()
  output.value.save_as('/tmp/ze-beta274.json');saved=json.loads(Path('/tmp/ze-beta274.json').read_text());assert saved['headerAnchor']=='native-post-top-left' and saved['socialPost']['mediaPosition']=='right' and saved['socialPost']['textSizePixels']==44
  page.locator('#portraitLayout').select_option('reference',force=True);assert page.locator('#showBullets').is_checked() and not page.locator('#showBullets').is_disabled() and page.locator('#postScrollMode').is_disabled()
  page.set_viewport_size({'width':780,'height':1000});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors and not page.evaluate('state.renderError'),errors;print('Text-only/hidden modes, RTL/LTR painted safety, attached movement, saved settings and prior layout restoration: passed',flush=True);browser.close()
finally:server.shutdown();server.server_close()
