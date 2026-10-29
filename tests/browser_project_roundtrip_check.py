"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
from pathlib import Path
import json
with scene('project-roundtrip') as s:
 p=s.page;s.post('Original post',('portrait.mp4','photo.png'));assert p.evaluate('DURATION')==50
 s.value('bulletSplitMode','blank');s.value('bullets','First paragraph\n\nSecond paragraph');s.value('postJustifyMode','space');s.value('mediaTransitionDuration','1.2');s.value('mainDuration','37')
 p.evaluate('zeParagraphModel.items[0].manual=4.5;zeParagraphModel.cache=null;zeUpdateParagraphEditor()')
 p.locator('#useWholePost').click();assert not p.locator('#showBullets').is_checked()
 with p.expect_download() as out:p.locator('#saveJson').click()
 target=Path('/tmp/main-roll-roundtrip.json');out.value.save_as(str(target));data=json.loads(target.read_text());assert len(data['mediaSequence']['slots'])==2 and data['videoTiming']['durationSeconds']==37
 s.value('mainDuration','50');s.value('bulletSplitMode','auto');s.value('postJustifyMode','none');s.value('mediaTransitionDuration','.2');p.locator('#projectJsonFile').set_input_files(str(target));p.wait_for_function("document.getElementById('projectLoadStatus').textContent.startsWith('Project settings restored')")
 restored=p.evaluate('zeProjectData()');assert restored['bulletSplitMode']=='blank' and restored['postJustifyMode']=='space' and restored['mediaSequence']==data['mediaSequence'];assert restored['videoTiming']['durationSeconds']==37 and restored['videoTiming']['paragraphs'][0]['mode']=='manual' and restored['videoTiming']['paragraphs'][0]['holdSeconds']==4.5
 assert p.locator('#mainDuration').input_value()=='37' and '37.00' in p.locator('#exportProgress').inner_text()
 p.reload();p.wait_for_function('assets.source&&state.stvLoaded');p.locator('#projectJsonFile').set_input_files(str(target));p.wait_for_function("document.getElementById('projectLoadStatus').textContent.startsWith('Project settings restored')");fresh=p.evaluate('zeProjectData()');assert fresh['mediaSequence']==data['mediaSequence'] and fresh['postMedia']['items']==data['postMedia']['items'] and fresh['videoTiming']['paragraphs'][0]['holdSeconds']==4.5;assert 'Reattach original media' in p.locator('#projectLoadStatus').inner_text()
 before=s.boxes();p.evaluate("()=>zeApplyProject({project:'Bad'}).catch(()=>{})");assert s.boxes()==before
 print('Actual JSON download/load, grouping/justification/sequence slots/transition, selected duration and manual hold round trip: passed')
