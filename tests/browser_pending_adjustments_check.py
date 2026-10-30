"""Owner corrections: independent bullets, retained layouts and disjoint painted regions."""
from browser_support import scene,ROOT
from pathlib import Path
with scene('pending-adjustments') as s:
 p=s.page;s.all_controls()
 assert p.locator('#showPostText').is_visible()
 assert not p.locator('#postTextPlacement').is_visible()
 assert p.locator('#portraitLayout option').evaluate_all('els=>els.map(e=>e.value)')==['reference','social','focus','portrait']
 cases=0
 for file in ['portrait.png','photo.png','landscape.mp4']:
  s.value('bullets','Independent external bulletin')
  s.post('Original post text. '*150,(file,))
  assert p.locator('#bullets').input_value()=='Independent external bulletin'
  for layout in ['reference','focus','social','portrait']:
   s.value('portraitLayout',layout)
   for flip in [False,True]:
    p.evaluate('(v)=>setFlipped(v)',flip)
    for position in ['right','below']:
     s.value('socialMediaPosition',position)
     for fit in ['fit','fill']:
      s.value('postMediaFit',fit)
      for show in [False,True]:
       p.locator('#showPostText').set_checked(show)
       assert bool(p.evaluate('zePostRollText()'))==show
       assert p.locator('#bullets').input_value()=='Independent external bulletin'
       for size in [(180,200),(600,300)]:
        result=p.evaluate('''v=>{const [w,h]=v,regions=zeSocialRegions(10,30,w,h),calls=[],original=zeDrawCleanMedia;
         zeDrawCleanMedia=(ctx,frame,x,y,w,h,item,center)=>{calls.push({x,y,w,h});original(ctx,frame,x,y,w,h,item,center)};
         const canvas=document.createElement('canvas');canvas.width=800;canvas.height=600;const ctx=canvas.getContext('2d');
         const at=t=>{calls.length=0;zeDrawSocialPost(ctx,10,30,w,h,t);return structuredClone(calls)};
         const first=at(0),last=at(50);zeDrawCleanMedia=original;
         return {regions,first,last,together:zeScrollTogether(),boxes:zeWholeBelowMotion()?[zeWholeBelowPositions(10,30,w,h,0),zeWholeBelowPositions(10,30,w,h,50)]:null}}''',list(size))
        r=result['regions'];a=r['text'];b=r['media']
        assert b and b['w']>0 and b['h']>0,result
        if show:
         assert a and (a['x']+a['w']<=b['x'] or a['y']+a['h']<=b['y']),r
         if position=='right':assert result['first']==result['last'],result
         elif layout=='social':
          start,end=result['boxes'];dt=end['text']['y']-start['text']['y'];dm=end['media']['y']-start['media']['y']
          assert dt<0 and abs(dt-dm)<.01,result
          for box in [start,end]:assert box['text']['y']+box['text']['h']<=box['media']['y'],box
        cases+=1
  s.value('portraitLayout','reference');s.value('socialMediaPosition','below');p.locator('#useWholePost').click()
  assert p.locator('#socialMediaPosition').input_value()=='below'
 s.value('postContentMode','media');assert not p.locator('#showPostText').is_checked();p.locator('#showPostText').check();assert p.locator('#postContentMode').input_value()=='all' and p.evaluate('!!zePostRollText()')
 # Text-only channel import has no phantom post image and keeps the editable original body.
 s.post('Telegram original\nSecond line',())
 assert p.evaluate('zePost.items.length===0 && zePostRollText()===document.getElementById("postBody").value')
 for layout in ['reference','focus','social','portrait']:
  s.value('portraitLayout',layout);p.evaluate('setT(5)')
  p.locator('#canvas').screenshot(path=f'/tmp/ze-{layout}-text-only.png')
 s.post('A long caption '*80,('portrait.png',));s.value('portraitLayout','social');s.value('socialMediaPosition','right')
 for t in [.32,.8,1.2,2.12,5]:
  p.evaluate('(t)=>setT(t)',t);p.locator('#canvas').screenshot(path=f'/tmp/ze-pending-entrance-{t}.png')
 print(f'{cases} layout/flip/shape/size/fit/toggle cases: disjoint text/media, fixed right media, shared below travel; independent bullets and text-only import passed')
