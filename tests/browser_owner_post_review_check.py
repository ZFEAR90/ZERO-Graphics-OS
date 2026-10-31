"""Latest owner: complete Main post, strap clearance, profile initials and natural below media."""
from browser_support import scene,ROOT
from pathlib import Path
with scene('owner-post-review') as s:
 p=s.page;s.post('هذا نص أصلي طويل داخل المنشور، يبقى أسفل الشريط العلوي وصف الحساب. '*70,('portrait.png',));s.all_controls()
 assert p.locator('#showRollAccount').is_checked() and p.locator('#showPostText').is_checked()
 bullet=p.locator('#bullets').input_value()
 for layout in ['reference','focus','portrait','social']:
  s.value('portraitLayout',layout)
  for flip in [False,True]:
   p.evaluate('(v)=>setFlipped(v)',flip)
   for show in [False,True]:
    s.value('showRollAccount',show)
    result=p.evaluate('''()=>{const b=getBBox('source'),x=b.x+b.w*(1-365/402)/2,y=b.y+b.h*(1-372/398)/2,w=b.w*365/402,h=b.h*372/398;return {body:zeRollContentBounds(x,y,w,h),strap:b.y-8+Math.min(28,b.h*.07),social:zeSocialMode()}}''')
    if not result['social']:assert result['body']['y']>=result['strap']+7.99,result
    for t in [.8,1.2,2.12,5,25,49.96]:
     p.evaluate('(t)=>setT(t)',t)
     assert not p.evaluate('state.renderError')
    assert p.locator('#bullets').input_value()==bullet
    if layout=='reference' and not flip:p.locator('#canvas').screenshot(path=f'/tmp/ze-owner-main-account-{show}.png')
 # Actual painted post-text pixels must never enter the top accent strap.
 for layout in ['reference','focus','portrait','social']:
  s.value('portraitLayout',layout);s.value('socialMediaPosition','below')
  pixels=p.evaluate("""()=>{const old=zeDrawSocialText;let changed=0,above=0;for(const t of [1.84,2.12,5,25,49.96]){setT(t);const a=c.getImageData(0,0,1920,1080).data;zeDrawSocialText=()=>{};draw();const b=c.getImageData(0,0,1920,1080).data;zeDrawSocialText=old;const src=getBBox('source'),top=zeSocialMode()?src.y:src.y-8+Math.min(28,src.h*.07)+8;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]||a[i+3]!==b[i+3]){changed++;if(Math.floor(i/4/1920)<Math.floor(top*2))above++}}draw();return {changed,above}}""")
  assert pixels['changed']>0 and pixels['above']==0,(layout,pixels)
 # Main switches are independent; Whole's native account is not controlled by them.
 s.value('portraitLayout','reference')
 for profile in [False,True]:
  for name in [False,True]:
   s.value('showRollAccount',True);s.value('showRollProfile',profile);s.value('showRollName',name)
   out=p.evaluate("""()=>{const canvas=document.createElement('canvas');canvas.width=400;canvas.height=100;const ctx=canvas.getContext('2d'),oldCover=cover,oldLabel=zeDrawNativePostLabel;let images=0,labels=0;cover=(...args)=>{images++;oldCover(...args)};zeDrawNativePostLabel=(...args)=>{labels++;oldLabel(...args)};const band=zeInlinePostAccount(ctx,0,0,350);cover=oldCover;zeDrawNativePostLabel=oldLabel;return {images,labels,band}}""")
   assert out['images']==int(profile) and out['labels']==2*int(name),out
   assert (out['band']>0)==(profile or name)
 s.value('portraitLayout','social');p.evaluate('setT(5)');before=p.locator('#canvas').screenshot();s.value('showRollProfile',False);s.value('showRollName',False);assert p.locator('#canvas').screenshot()==before
 assert not p.locator('#mainPostAccountControls').is_visible()
 s.value('showRollProfile',True);s.value('showRollName',True)
 # Shared document cannot paint text into its pinned account/header band.
 s.value('portraitLayout','social');s.value('showRollAccount',True);s.value('socialMediaPosition','below')
 for fit in ['fit','fill']:
  s.value('postMediaFit',fit)
  for text in ['Short caption.', 'Long caption. '*120]:
   s.value('postBody',text)
   data=p.evaluate('''()=>{const a=zeWholeBelowPositions(10,100,500,300,0),b=zeWholeBelowPositions(10,100,500,300,50);return {a,b}}''')
   a,b=data['a'],data['b'];assert a['media']['y']>=a['text']['y']+a['text']['h']+11.99
   assert abs(a['media']['w']/a['media']['h']-p.evaluate('zeVisualItems()[0].width/zeVisualItems()[0].height'))<.001
   assert abs((b['text']['y']-a['text']['y'])-(b['media']['y']-a['media']['y']))<.001
   if fit=='fill':assert a['media']['w']==500 and a['media']['h']>300 and b['offset']>0
 s.value('postBody','Tiny caption');s.value('postMediaFit','fit')
 no_overflow=p.evaluate('''()=>{const a=zeWholeBelowPositions(0,100,200,700,0),b=zeWholeBelowPositions(0,100,200,700,50);return {a,b}}''')
 assert no_overflow['a']['overflow']==0 and no_overflow['a']['media']==no_overflow['b']['media']
 # Missing profile produces a visible Unicode initial for every supported platform.
 for platform in ['Telegram','X','Facebook','Instagram','Threads']:
  data=p.evaluate('''platform=>{zeSolo.postPlatform=platform;assets.avatar=null;document.getElementById('displayname').value='علي Example';const a=zeAccountImage(),g=a.getContext('2d'),pixels=g.getImageData(0,0,160,160).data;let white=0;for(let i=0;i<pixels.length;i+=4)if(pixels[i]>240&&pixels[i+1]>240&&pixels[i+2]>240)white++;const logo=zePlatformCanvas(platform);return {white,logo:logo.width,bundled:!!zePlatformLogos[platform]}}''',platform)
  assert data['white']>100 and data['logo']==200 and data['bundled'],data
 s.value('portraitLayout','reference');s.value('showRollAccount',True);s.value('postBody','Aligned original post text. '*12);p.evaluate('setT(5)');p.locator('#canvas').screenshot(path='/tmp/ze-owner-main-complete.png')
 print('Complete Main post/account toggle, top strap clearance, natural media bounds, overflow-only shared travel, five platform logos and Unicode initial fallbacks: passed')
