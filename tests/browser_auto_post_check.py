"""Default fixed cadre, automatic portrait/wide composition, independent text scroll and Advanced native sizing."""
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
  assert page.locator('#postTextPlacement').input_value()=='roll' and page.locator('#postScrollMode').input_value()=='fixed'
  assert page.locator('#portraitLayout').input_value()=='reference' and page.locator('#socialMediaPosition').input_value()=='auto'
  assert page.locator('#portraitLayout').evaluate('(el)=>!!el.closest("#advancedOptions")')
  assert not page.locator('#portraitLayout').is_visible();page.locator('#openRollLayouts').click();assert page.locator('#portraitLayout').is_visible();page.locator('#mainTab').click()
  baseline=page.evaluate('zeVisibleBounds("source",getBBox("source"))');page.locator('#bullets').fill('نص تحريري مستقل عن المنشور')
  text='نص المنشور العربي يبقى داخل الرول. يتحرك النص الطويل داخل مساحة مستقلة بينما تبقى الصورة والفيديو ظاهرين. '
  for filename,type_,position in [('portrait.mp4','video','right'),('portrait.png','image','right'),('landscape.mp4','video','below'),('photo.png','image','below'),(None,'image','below')]:
   page.evaluate(r'''async(v)=>{let url=v.file?'/fixtures/'+v.file:null;if(!url){const c=document.createElement('canvas');c.width=c.height=400;c.getContext('2d').fillRect(0,0,400,400);url=c.toDataURL()}zeCommitPost(await zePreparePost({text:(v.text.repeat(3)+'\n\n').repeat(5),attachments:[{type:v.type,url}]}));setT(5)}''',dict(file=filename,type=type_,text=text))
   if type_=='video':page.wait_for_function('zePost.items[0].el.readyState>=2 && !zePost.items[0].el.seeking')
   assert page.locator('#postTextPlacement').input_value()=='roll' and page.locator('#postScrollMode').is_disabled()
   assert page.locator('#bullets').input_value()=='نص تحريري مستقل عن المنشور'
   for flip in [False,True]:
    page.evaluate('(v)=>setFlipped(v)',flip);before=page.evaluate('zeSafeLayout()');s=before['source'];assert s['w']==baseline['w'] and s['h']==baseline['h']
    assert page.evaluate('zeAutoPostPosition()')==position
    regions=page.evaluate('zeSocialRegions(100,100,365,372)');t,m=regions['text'],regions['media']
    if position=='right':assert t['x']+t['w']<m['x'] and t['y']==m['y']
    else:assert t['y']+t['h']<m['y'] and t['x']==m['x']
    snapshots=[]
    for time in [5,45]:
     snapshots.append(page.evaluate('''(t)=>{const canvas=document.createElement('canvas');canvas.width=960;canvas.height=540;const ctx=canvas.getContext('2d'),oldText=CanvasRenderingContext2D.prototype.drawImage,oldMedia=zeDrawCleanMedia;let text=null,media=null;CanvasRenderingContext2D.prototype.drawImage=function(im,...args){if(im===zePost.socialDoc?.canvas)text={x:args[0],y:args[1]};return oldText.call(this,im,...args)};zeDrawCleanMedia=(c,im,x,y,w,h,item)=>{media={x,y,w,h};oldMedia(c,im,x,y,w,h,item)};try{zeDrawSocialPost(ctx,100,100,365,372,t)}finally{CanvasRenderingContext2D.prototype.drawImage=oldText;zeDrawCleanMedia=oldMedia}return {text,media}}''',time))
    assert snapshots[1]['text']['y']<snapshots[0]['text']['y'] and snapshots[0]['media']==snapshots[1]['media'],snapshots
    page.locator('#postContentMode').select_option('media');assert page.evaluate('zeAutoPostPosition()')=='media'
    media=page.evaluate('zeSocialRegions(100,100,365,372)');assert media['text'] is None and media['media']==dict(x=100,y=100,w=365,h=372)
    for fitting in ['fit','fill']:
     page.locator('#postMediaFit').select_option(fitting);assert page.evaluate('zeSafeLayout()')==before
     dimensions=page.evaluate('''(()=>{const item=zePrimaryMedia(),p=zeProtectedPlacement({width:item.width,height:item.height},365,372,item);return p})()''')
     if fitting=='fit':assert dimensions['w']<=365+.01 and dimensions['h']<=372+.01
     else:assert dimensions['w']>=365-.01 and dimensions['h']>=372-.01
    page.locator('#postMediaFit').select_option('fill');page.locator('#postContentMode').select_option('all')
    page.locator('#postTextPlacement').select_option('hidden');assert page.evaluate('zeSocialRegions(100,100,365,372).text===null');page.locator('#postTextPlacement').select_option('roll')
   print(filename or 'square photo','fixed screenshot size, default inside-roll text, automatic',position,', scroll and centered media Fill/Fit: passed',flush=True)
  # Validate centering from painted media pixels (Fit is rendered by the contain path).
  assert page.evaluate('''(()=>{const frame=document.createElement('canvas');frame.width=800;frame.height=200;frame.getContext('2d').fillRect(0,0,800,200);const out=document.createElement('canvas');out.width=365;out.height=372;const ctx=out.getContext('2d');document.getElementById('postMediaFit').value='fit';zeDrawFramedMedia(ctx,frame,0,0,365,372,{});const data=ctx.getImageData(0,0,365,372).data;let l=365,r=0,t=372,b=0;for(let y=0;y<372;y++)for(let x=0;x<365;x++)if(data[(y*365+x)*4+3]>128){l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);b=Math.max(b,y)}document.getElementById('postMediaFit').value='fill';return Math.abs((l+r)/2-182)<1&&Math.abs((t+b)/2-185.5)<1&&t>0&&b<371})()''')
  # Painted post text never crosses the lower-third line in the new default.
  for direction,body in [('rtl',text*40),('ltr','Long English post text stays above the lower-third safe line. '*60)]:
   page.locator('#postBody').fill(body);page.locator('#rollLanguage').select_option(direction)
   data=page.evaluate('''(()=>{let changed=0,outside=0;const old=zeDrawSocialText;for(const t of [1.8,2.04,2.4,5,25,49.96]){setT(t);const a=c.getImageData(0,0,1920,1080).data;zeDrawSocialText=()=>{};draw();const b=c.getImageData(0,0,1920,1080).data;zeDrawSocialText=old;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3]){changed++;if(Math.floor(i/4/1920)>=zeBroadcastBounds().bottom*2)outside++}}draw();return {changed,outside}})()''');assert data['changed']>0 and data['outside']==0,data
  # Explicit text-only and solo remain fixed; optional adaptive mode restores native proportions.
  page.locator('#postContentMode').select_option('text');s=page.evaluate('getBBox("source")');assert s['w']==402 and s['h']==398
  page.locator('#showBullets').uncheck();assert page.evaluate('zeEmbeddedHeader() && getBBox("source").w===402')
  page.locator('#postContentMode').select_option('all');page.locator('#showBullets').check();page.locator('#openRollLayouts').click();page.locator('#portraitLayout').select_option('focus');page.locator('#mainTab').click()
  native=page.evaluate('getBBox("source")');assert native['w']!=402 or native['h']!=398
  page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures/portrait.mp4'));page.wait_for_function('zePost.items[0].label==="portrait.mp4"');portrait=page.evaluate('getBBox("source")');assert portrait['h']>portrait['w']
  page.locator('#openRollLayouts').click();page.locator('#portraitLayout').select_option('reference');page.locator('#socialMediaPosition').select_option('auto');page.locator('#mainTab').click();assert page.evaluate('getBBox("source").w===402 && getBBox("source").h===398')
  # The whole-post idea is directly available in Main, with inset identity and a side platform.
  page.locator('#useWholePost').click();assert page.evaluate('zeSocialMode() && zeNoBullets()') and page.locator('#useWholePost').get_attribute('aria-pressed')=='true'
  inside=page.evaluate('''(()=>{const b=getBBox('source'),head=getBBox('identity'),local=headerLayout(c),k=head.w/R.identity.w,p=part=>({x:head.x+(part.x-R.identity.x)*k,y:head.y+(part.y-R.identity.y)*k,w:part.w*k,h:part.h*k});return {b,avatar:p(local.avatar),name:p(local.name),handle:p(local.handle),platform:p(local.platform)}})()''');b=inside['b'];assert abs(b['x']+b['w']/2-480)<.01
  for key in ['avatar','name','handle']:
   item=inside[key];assert b['x']<=item['x'] and item['x']+item['w']<=b['x']+b['w'] and b['y']<=item['y']<b['y']+100,inside
  platform=inside['platform'];assert platform['x']+platform['w']<b['x'] or platform['x']>b['x']+b['w']
  page.evaluate('''async()=>zeCommitPost(await zePreparePost({text:'Wide post text also stays on the left in Whole roll frame.',attachments:[{type:'video',url:'/fixtures/landscape.mp4'}]}))''')
  assert page.evaluate('zeAutoPostPosition()')=='right' and 'media right' in page.locator('#socialMediaPosition option[value=auto]').text_content()
  assert page.title().startswith('ZE OS — Main roll')
  page.locator('#undoEdit').click();assert page.locator('#portraitLayout').input_value()=='reference';page.locator('#useWholePost').click();assert not page.locator('#showBullets').is_checked() and page.locator('#postTextPlacement').input_value()=='roll'
  page.locator('#useMainRoll').click();assert page.locator('#portraitLayout').input_value()=='reference' and page.locator('#showBullets').is_checked()
  with page.expect_download() as output:page.locator('#saveJson').click()
  output.value.save_as('/tmp/ze-beta276.json');saved=json.loads(Path('/tmp/ze-beta276.json').read_text());assert saved['postArrangement']['selection']=='auto' and saved['rollFrameSizing']=='reference'
  page.set_viewport_size({'width':780,'height':1000});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors and not page.evaluate('state.renderError'),errors;browser.close();print('RTL/LTR painted safety, fixed text-only/solo, native-size option in Advanced, saved defaults and mobile width: passed',flush=True)
finally:server.shutdown();server.server_close()
