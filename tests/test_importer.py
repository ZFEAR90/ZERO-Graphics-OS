import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch,Mock,MagicMock
import tempfile
import json,socket,threading,urllib.request,urllib.error
spec=importlib.util.spec_from_file_location('importer',Path(__file__).parents[1]/'ze_local_importer.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
PUBLIC=[(socket.AF_INET,socket.SOCK_STREAM,6,'',('8.8.8.8',443))]
def response(body,status=200,kind='application/json'):
 r=Mock(status_code=status,content=body.encode() if isinstance(body,str) else body,headers={'content-type':kind})
 r.text=body if isinstance(body,str) else '';r.json=lambda:json.loads(r.text);return r
class ImportTests(unittest.TestCase):
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_x_post_before_blocked_website(self,_):
  post={'text':'Actual post text','user':{'name':'Real Author','screen_name':'real','profile_image_url_https':'https://pbs.twimg.com/profile.jpg'},'photos':[{'url':'https://pbs.twimg.com/one.jpg'},{'url':'https://pbs.twimg.com/two.jpg'}]}
  with patch('requests.get',side_effect=[response(json.dumps(post)),response(b'avatar',kind='image/jpeg'),response(b'first',kind='image/jpeg'),response(b'second',kind='image/jpeg')]) as get:
   data=m.fetch_metadata('https://x.com/real/status/123456789')
  self.assertEqual(data['name'],'Real Author');self.assertEqual(data['handle'],'real');self.assertTrue(data['avatar_data'].startswith('data:image/'));self.assertEqual(len(data['media_items']),2)
  self.assertEqual(get.call_args_list[0].args[0],'https://cdn.syndication.twimg.com/tweet-result')
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_telegram_real_author_and_avatar(self,_):
  html='''<meta property="og:description" content="Summary"><a class="tgme_widget_message_user_photo" style="background-image:url('https://cdn-telegram.org/avatar.jpg')"></a><span class="tgme_widget_message_owner_name">Actual Channel</span><div class="tgme_widget_message_text">Actual message</div>'''
  with patch('requests.get',side_effect=[response(html,kind='text/html'),response(b'avatar',kind='image/jpeg')]):data=m.fetch_metadata('https://t.me/s/channel/123')
  self.assertEqual(data['handle'],'channel');self.assertEqual(data['name'],'Actual Channel');self.assertEqual(data['text'],'Actual message');self.assertTrue(data['avatar_data'])
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_platform_denial_is_error(self,_):
  with patch('requests.get',return_value=response('denied',403)):
   with self.assertRaisesRegex(RuntimeError,'403'):m.fetch_metadata('https://instagram.com/p/example')
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_facebook_share_redirect_and_author(self,_):
  redirect=response('',302);redirect.headers['Location']='https://www.facebook.com/real.author/posts/123'
  html='<meta property="og:description" content="Actual post"><script type="application/ld+json">'+json.dumps({'author':{'name':'Real FB Author','image':'https://scontent.fbcdn.net/avatar.jpg'}})+'</script>'
  with patch('requests.get',side_effect=[redirect,response(html,kind='text/html'),response(b'avatar',kind='image/jpeg')]) as get:
   data=m.fetch_metadata('https://www.facebook.com/share/p/1Cuq9SFPGz/')
  self.assertEqual(data['name'],'Real FB Author');self.assertEqual(data['handle'],'real.author');self.assertTrue(data['avatar_data']);self.assertEqual(get.call_count,3)
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_redirect_does_not_escape_supported_hosts(self,_):
  redirect=response('',302);redirect.headers['Location']='https://evil.example/post'
  with patch('requests.get',return_value=redirect) as get:
   with self.assertRaises(ValueError):m.fetch_metadata('https://www.facebook.com/share/p/example/')
  self.assertEqual(get.call_count,1)
 def test_reject_unsupported_or_private_urls(self):
  for url in ['http://x.com/user/status/123','https://evil.example/post','https://user:pass@x.com/a','https://x.com:444/a']:
   with self.assertRaises(ValueError):m.public_url(url,m.KNOWN)
  with patch.object(m.socket,'getaddrinfo',return_value=[(socket.AF_INET,socket.SOCK_STREAM,6,'',('127.0.0.1',443))]):
   with self.assertRaises(ValueError):m.public_url('https://x.com/a',m.KNOWN)
 def test_local_api_file_origin(self):
  server=m.ThreadingHTTPServer(('127.0.0.1',0),m.Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
  try:
   req=urllib.request.Request(f'http://127.0.0.1:{server.server_port}/api/post?url=invalid',headers={'Origin':'null'})
   with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(req)
   self.assertEqual(error.exception.code,422);self.assertEqual(error.exception.headers['Access-Control-Allow-Origin'],'null');self.assertIn('error',json.loads(error.exception.read()))
  finally:server.shutdown();server.server_close()
 def test_health_identifies_importer_for_file_origin(self):
  server=m.ThreadingHTTPServer(('127.0.0.1',0),m.Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
  try:
   req=urllib.request.Request(f'http://127.0.0.1:{server.server_port}/api/health',headers={'Origin':'null'})
   with urllib.request.urlopen(req) as response:
    self.assertEqual(response.headers['Access-Control-Allow-Origin'],'null')
    self.assertEqual(json.load(response),{'service':'ze-os-importer','version':'0.7-beta2.7'})
  finally:server.shutdown();server.server_close()
 def test_capture_missing_browser_reports_cause(self):
  with patch.object(m,'launch_capture_browser',side_effect=m.CaptureUnavailable('Capture browser missing')):
   result=m.screenshot_public_post('https://www.facebook.com/share/p/example/')
  self.assertEqual(result,{'capture_error':'Capture browser missing'})
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_video_cache_preserves_original_bytes(self,_):
  reply=MagicMock(status_code=200,headers={'content-type':'video/mp4','content-length':'12'})
  reply.__enter__.return_value=reply;reply.iter_content.return_value=[b'original',b'media']
  with tempfile.TemporaryDirectory() as folder,patch.object(m,'MEDIA_ROOT',Path(folder)/'media'),patch('requests.get',return_value=reply):
   item=m.video_data('https://video.twimg.com/file.mp4')
   self.assertEqual(item['type'],'video');self.assertEqual((m.MEDIA_ROOT/Path(item['url']).name).read_bytes(),b'originalmedia')
 def test_cached_media_supports_seeking_ranges(self):
  with tempfile.TemporaryDirectory() as folder,patch.object(m,'MEDIA_ROOT',Path(folder)):
   filename='a'*32+'.mp4';(m.MEDIA_ROOT/filename).write_bytes(b'0123456789')
   server=m.ThreadingHTTPServer(('127.0.0.1',0),m.Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
   try:
    for requested,expected in [('bytes=2-5',b'2345'),('bytes=-3',b'789')]:
     request=urllib.request.Request(f'http://127.0.0.1:{server.server_port}/.ze_media/{filename}',headers={'Range':requested})
     with urllib.request.urlopen(request) as result:self.assertEqual(result.code,206);self.assertEqual(result.read(),expected);self.assertEqual(result.headers['Accept-Ranges'],'bytes')
    request=urllib.request.Request(f'http://127.0.0.1:{server.server_port}/.ze_media/{filename}',headers={'Range':'bytes=99-'})
    with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(request)
    self.assertEqual(error.exception.code,416)
   finally:server.shutdown();server.server_close()
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_video_cache_rejects_html_or_large_files(self,_):
  for headers in [{'content-type':'text/html'},{'content-type':'video/mp4','content-length':str(41*1024*1024)}]:
   reply=MagicMock(status_code=200,headers=headers);reply.__enter__.return_value=reply
   with tempfile.TemporaryDirectory() as folder,patch.object(m,'MEDIA_ROOT',Path(folder)/'media'),patch('requests.get',return_value=reply):
    with self.assertRaises(RuntimeError):m.video_data('https://video.twimg.com/file.mp4')
    self.assertFalse(m.MEDIA_ROOT.exists())
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_x_video_is_separate_from_photos(self,_):
  post={'text':'A video post','user':{'name':'Author'},'video':{'variants':[{'type':'video/mp4','bitrate':1000000,'src':'https://video.twimg.com/file.mp4'}]}}
  with patch('requests.get',return_value=response(json.dumps(post))),patch.object(m,'video_data',return_value={'type':'video','url':'/.ze_media/example.mp4'}):data=m.fetch_x_post('https://x.com/author/status/123')
  self.assertEqual(data['attachments'],[{'type':'video','url':'/.ze_media/example.mp4'}])
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_audio_metadata_returns_separate_attachment(self,_):
  html='<meta property="og:description" content="Actual post"><meta property="og:audio" content="https://scontent.fbcdn.net/voice.mp3">'
  with patch('requests.get',return_value=response(html)),patch.object(m,'video_data',return_value={'type':'audio','url':'/.ze_media/example.mp3'}) as cache:
   data=m.fetch_metadata('https://www.facebook.com/author/posts/123')
  self.assertEqual(data['attachments'][0]['type'],'audio');cache.assert_called_once_with('https://scontent.fbcdn.net/voice.mp3','audio')
 def test_api_retains_metadata_when_capture_fails(self):
  self.check_capture_response({'name':'Real author','text':'Actual post text','status':'partial'},None,200)
 def test_api_combines_platform_and_capture_errors(self):
  self.check_capture_response(None,RuntimeError('Platform returned HTTP 400'),422)
 def check_capture_response(self,metadata,failure,code):
  server=m.ThreadingHTTPServer(('127.0.0.1',0),m.Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
  try:
   with patch.object(m,'public_url',side_effect=lambda url,patterns:url),patch.object(m,'fetch_metadata',return_value=metadata,side_effect=failure),patch.object(m,'screenshot_public_post',return_value={'capture_error':'Capture browser missing'}):
    try:response=urllib.request.urlopen(f'http://127.0.0.1:{server.server_port}/api/post?url=https%3A%2F%2Fwww.facebook.com%2Fshare%2Fp%2Fexample%2F')
    except urllib.error.HTTPError as error:response=error
    with response:
     self.assertEqual(response.code,code);data=json.load(response)
    if code==200:
     self.assertEqual(data['text'],'Actual post text');self.assertEqual(data['status'],'partial');self.assertEqual(data['capture_warning'],'Capture browser missing');self.assertNotIn('screenshot_data',data)
    else:
     self.assertIn('HTTP 400',data['error']);self.assertIn('Capture browser missing',data['error'])
  finally:server.shutdown();server.server_close()
if __name__=='__main__':unittest.main()
