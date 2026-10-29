"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('video-sequence') as s:
 p=s.page;s.post('Video post',('portrait.mp4','landscape.mp4'));s.all_controls();p.locator('#postAudio').check();p.wait_for_function('zePost.items.every(i=>i.gain)')
 p.evaluate('setT(2.2);state.playing=true');p.wait_for_function('!zePost.items[0].el.paused&&zePost.items[1].el.paused');p.evaluate('state.playing=false')
 slot=p.evaluate('(timeline(DURATION)-val("sourceTiming")-1.88)/2');p.evaluate('(t)=>setT(t)',1.88+slot+.4);p.wait_for_function('zePost.items.every(i=>!i.el.seeking)&&Math.abs(zePost.items[1].el.currentTime-.4)<.02')
 weights=p.evaluate('zePost.items.map(i=>i.gain.gain.value)');assert all(abs(w-.5)<.01 for w in weights),weights
 p.evaluate('zePost.items[0].endBehavior="loop";state.playing=true');p.wait_for_function('zePost.items.every(i=>!i.el.paused)');p.evaluate('state.playing=false;setT(50)');p.wait_for_function('zePost.items.every(i=>!i.el.seeking)')
 assert p.evaluate('zePost.items.every(i=>!!zePostFrame(i))')
 assert p.evaluate("(()=>{const i=zePost.items[1];i.endBehavior='hold';const a=zeMediaPlaybackTarget(i,100);i.endBehavior='loop';const b=zeMediaPlaybackTarget(i,100);return !a.canPlay&&b.canPlay&&a.target<i.el.duration&&b.target<i.el.duration})()")
 assert p.evaluate("(()=>{const i=zePost.items[1];zePostFrame(i);const frame=i.lastFrame;Object.defineProperty(i.el,'readyState',{value:1,configurable:true});const retained=zePostFrame(i)===frame;delete i.el.readyState;const ctx=frame.getContext('2d'),a=ctx.getImageData(10,10,1,1).data;return retained&&a[3]===255&&Math.max(...a.slice(0,3))>30})()")
 print('Real range-served videos: active/overlap playback, incoming local time, audio crossfade, Hold/Loop and decoded-frame fallback: passed')
