"""Telegram widget extraction separates full post text, profile identity and actual media."""
from test_importer import m,response,PUBLIC
from unittest.mock import patch
import unittest
class TelegramTests(unittest.TestCase):
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_text_only_og_channel_photo_is_never_post_media(self,_):
  text='Original Telegram body '*300
  html='<meta property="og:image" content="https://cdn-telegram.org/avatar.jpg"><meta property="og:description" content="Truncated preview"><span class="tgme_widget_message_owner_name">Channel</span><div class="tgme_widget_message_text">'+text+'<br>Last line</div>'
  with patch('requests.get',side_effect=[response(html,kind='text/html'),response(b'avatar',kind='image/jpeg')]) as get:
   data=m.fetch_metadata('https://t.me/alichoeib1970/19404')
  self.assertIn('?embed=1',get.call_args_list[0].args[0]);self.assertEqual(data['text'],text+'\nLast line');self.assertEqual(data['name'],'Channel');self.assertTrue(data['avatar_data']);self.assertEqual(data['attachments'],[]);self.assertNotIn('media_data',data)
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_identity_photos_are_not_media_on_other_platforms(self,_):
  image='https://scontent.cdninstagram.com/profile.jpg'
  html='<meta property="og:description" content="Original post text"><meta property="og:image" content="'+image+'"><article><header><img alt="Account profile picture" src="'+image+'"></header></article>'
  for url in ['https://instagram.com/p/example','https://facebook.com/author/posts/123','https://threads.com/@author/post/example']:
   with self.subTest(url=url),patch('requests.get',side_effect=[response(html,kind='text/html'),response(b'profile-photo',kind='image/jpeg')]):
    data=m.fetch_metadata(url)
   self.assertTrue(data['avatar_data']);self.assertNotIn('media_data',data);self.assertEqual(data['text'],'Original post text')
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_nested_css_channel_profile_is_preserved(self,_):
  html="""<div class="tgme_widget_message_text">Original text</div><a class="tgme_widget_message_user_photo" style="display:block"><i style="background-image:url('https://cdn-telegram.org/profile.jpg')"></i></a>"""
  with patch('requests.get',side_effect=[response(html,kind='text/html'),response(b'channel-photo',kind='image/jpeg')]):data=m.fetch_metadata('https://t.me/channel/123')
  self.assertTrue(data['avatar_data']);self.assertEqual(data['attachments'],[])
 @patch.object(m.socket,'getaddrinfo',return_value=PUBLIC)
 def test_actual_photo_is_separate_from_channel_avatar(self,_):
  html='''<meta property="og:image" content="https://cdn-telegram.org/avatar.jpg"><a class="tgme_widget_message_user_photo"><img src="https://cdn-telegram.org/avatar.jpg"></a><div class="tgme_widget_message_text">Body</div><a class="tgme_widget_message_photo_wrap" style="background-image:url('https://cdn-telegram.org/post.jpg')"></a>'''
  with patch('requests.get',side_effect=[response(html,kind='text/html'),response(b'avatar',kind='image/jpeg'),response(b'post',kind='image/jpeg')]):data=m.fetch_metadata('https://t.me/channel/123')
  self.assertEqual(len(data['attachments']),1);self.assertNotEqual(data['attachments'][0]['data_url'],data['avatar_data'])
if __name__=='__main__':unittest.main()
