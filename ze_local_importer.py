"""ZE OS beta local helper for fetching publicly available social post metadata.

No account credentials, no cloud service, localhost only.
Social networks may deny anonymous capture; users can always import a screenshot manually.
Requires: Python 3, requests, beautifulsoup4. Optional: playwright + Chromium.
"""
from __future__ import annotations
import base64
import ipaddress
import json
import mimetypes
import os
from pathlib import Path
import re
import socket
import sys
import math
import shutil
import uuid
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urljoin
from html import unescape

ROOT=Path(__file__).resolve().parent
KNOWN=("x.com","twitter.com","facebook.com","fb.watch","instagram.com","t.me","telegram.me","threads.net")
IMAGE_HOSTS=("pbs.twimg.com","twimg.com","fbcdn.net","cdninstagram.com","cdninstagram.net","instagram.com","telegram.org","cdn-telegram.org","telesco.pe","telegram-cdn.org","t.me","scontent.cdninstagram.com")
VIDEO_HOSTS=("video.twimg.com","fbcdn.net","cdninstagram.com","cdninstagram.net","cdn-telegram.org","telegram-cdn.org","telesco.pe")
MEDIA_ROOT=ROOT/'.ze_media'


def video_data(url,kind='video'):
    """Cache a publicly downloadable MP4/WebM, with bounded size and validated redirects."""
    import requests
    url=public_url(url,VIDEO_HOSTS)
    for _ in range(4):
        response=requests.get(url,timeout=(8,20),stream=True,allow_redirects=False)
        if response.status_code in (301,302,303,307,308):
            location=response.headers.get('Location','');response.close()
            url=public_url(urljoin(url,location),VIDEO_HOSTS)
            continue
        break
    else: raise RuntimeError('Video redirected too many times')
    with response:
        if response.status_code!=200: raise RuntimeError(f'Video returned HTTP {response.status_code}')
        mime=response.headers.get('content-type','').split(';')[0].lower()
        extensions={'video/mp4':'.mp4','video/webm':'.webm'} if kind=='video' else {'audio/mpeg':'.mp3','audio/mp4':'.m4a','audio/ogg':'.ogg','audio/webm':'.webm','audio/wav':'.wav','audio/x-wav':'.wav'}
        if mime not in extensions: raise RuntimeError('No supported public '+kind+' file was provided')
        limit=40*1024*1024
        if int(response.headers.get('content-length','0'))>limit: raise RuntimeError('Video exceeds the 40 MiB import limit; add a trimmed file locally')
        MEDIA_ROOT.mkdir(exist_ok=True)
        path=MEDIA_ROOT/(uuid.uuid4().hex+extensions[mime])
        try:
            size=0
            with path.open('xb') as output:
                for chunk in response.iter_content(65536):
                    size+=len(chunk)
                    if size>limit: raise RuntimeError('Video exceeds the 40 MiB import limit; add a trimmed file locally')
                    output.write(chunk)
            if not size: raise RuntimeError('Video was empty')
        except Exception:
            path.unlink(missing_ok=True)
            raise
    return {'type':kind,'url':'/.ze_media/'+path.name,'mime':mime}


def attach_public_video(output,url):
    if not url: return
    try: output.setdefault('attachments',[]).append(video_data(url))
    except Exception as ex: output.setdefault('media_warnings',[]).append('Video unavailable: '+str(ex)[:160])


def allowed(host, patterns):
    host=(host or '').lower().strip('.')
    return any(host==d or host.endswith('.'+d) for d in patterns)


def public_url(url, patterns):
    p=urlparse(url)
    if p.scheme!='https' or p.username or p.password or p.port not in (None,443):
        raise ValueError('Only public HTTPS links are accepted')
    if not allowed(p.hostname,patterns):
        raise ValueError('Unsupported website domain')
    for r in socket.getaddrinfo(p.hostname,443,type=socket.SOCK_STREAM):
        addr=ipaddress.ip_address(r[4][0])
        if not addr.is_global:
            raise ValueError('Address is not publicly routable')
    return url


def image_data(url):
    if not url:return None
    try:
        import requests
        url=public_url(url,IMAGE_HOSTS)
        res=requests.get(url,timeout=7,headers={'User-Agent':'Mozilla/5.0'},allow_redirects=False)
        if res.status_code!=200 or len(res.content)>3_500_000:return None
        if not res.headers.get('content-type','').lower().startswith('image/'):return None
        return 'data:'+res.headers.get('content-type','image/jpeg').split(';')[0]+';base64,'+base64.b64encode(res.content).decode()
    except Exception:return None


def platform_for(url):
    h=urlparse(url).hostname.lower().removeprefix('www.')
    for platform,domains in [('X',('x.com','twitter.com')),('Facebook',('facebook.com','fb.watch')),('Instagram',('instagram.com',)),('Telegram',('t.me','telegram.me')),('Threads',('threads.net',))]:
        if allowed(h,domains):return platform
    return 'Unknown'


def tweet_token(tweet_id):
    # Public X syndication token; no login or account credentials.
    value = int(tweet_id) / 1e15 * math.pi
    whole = int(value)
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    digits = ''
    while whole:
        digits = alphabet[whole % 36] + digits
        whole //= 36
    fraction = value - int(value)
    for _ in range(12):
        fraction *= 36
        digit = int(fraction)
        digits += alphabet[digit]
        fraction -= digit
    return digits.replace('0', '')


def fetch_x_post(url):
    import requests
    match = re.search(r'/status/(\d{1,22})', url)
    if not match:
        raise ValueError('Use a link to a specific X post, including /status/…')
    tweet_id = match.group(1)
    endpoint = 'https://cdn.syndication.twimg.com/tweet-result'
    r = requests.get(endpoint, params={'id': tweet_id, 'lang': 'en', 'token': tweet_token(tweet_id)},
                     timeout=15, allow_redirects=False)
    if r.status_code != 200 or len(r.content) > 500000:
        raise RuntimeError(f'X public post service returned HTTP {r.status_code}')
    data = r.json()
    user = data.get('user') or {}
    if not data.get('text') and not user:
        raise RuntimeError('X did not expose this post publicly. Import its screenshot manually.')
    output = {'url': url, 'platform': 'X', 'handle': str(user.get('screen_name', ''))[:100],
              'name': str(user.get('name', ''))[:100], 'text': str(data.get('text', ''))[:12000],
              'status': 'partial'}
    profile = user.get('profile_image_url_https') or user.get('profile_image_url')
    if profile:
        output['avatar_data'] = image_data(profile)
    photos = data.get('photos') or []
    output['media_items'] = [pic for pic in (image_data(photo.get('url')) for photo in photos[:4]) if pic]
    if output['media_items']:
        output['media_data'] = output['media_items'][0]
    output['attachments']=[{'type':'image','data_url':item} for item in output['media_items']]
    video=data.get('video') or {}
    variants=video.get('variants') or []
    playable=[v for v in variants if v.get('type',v.get('content_type'))=='video/mp4' and (v.get('src') or v.get('url'))]
    if playable:
        chosen=min(playable,key=lambda v:abs((v.get('bitrate') or 1000000)-1500000))
        attach_public_video(output,chosen.get('src') or chosen.get('url'))
    elif video: output.setdefault('media_warnings',[]).append('The post has video but no publicly downloadable MP4. Add the original file locally.')
    return output


def fetch_metadata(url):
    import requests
    from bs4 import BeautifulSoup
    url=public_url(url,KNOWN)
    # Try the public post service before the website; x.com often returns a login wall.
    if platform_for(url) == 'X':
        try:
            return fetch_x_post(url)
        except Exception as ex:
            x_failure = str(ex)
    h={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36','Accept-Language':'en-US,en;q=0.9'}
    # Facebook share links redirect to the real post. Validate every hop before fetching.
    for _ in range(6):
        r=requests.get(url,timeout=12,headers=h,allow_redirects=False)
        if r.status_code not in (301,302,303,307,308): break
        url=public_url(urljoin(url,r.headers.get('Location','')),KNOWN)
    else: raise RuntimeError('Too many post-link redirects')
    if r.status_code not in (200,206): raise RuntimeError(f'Platform returned HTTP {r.status_code}. '+(x_failure if platform_for(url)=='X' else 'Use a public post or import its screenshot.'))
    if len(r.content)>2_500_000:raise RuntimeError('Page is too large for beta extraction')
    html=r.text
    doc=BeautifulSoup(html,'html.parser')
    def meta(*keys):
        for key in keys:
            node=doc.find('meta',attrs={'property':key}) or doc.find('meta',attrs={'name':key})
            if node and node.get('content'):return unescape(node.get('content')).strip()
        return ''
    title=meta('og:title','twitter:title')
    description=meta('og:description','twitter:description','description')
    if urlparse(url).path.rstrip('/') in ('/login','/login.php','/accounts/login') or title.lower() in ('log into facebook','log in to facebook','login • instagram'):
        raise RuntimeError('This post requires login; use a public post or upload its screenshot.')
    image=meta('og:image','twitter:image')
    author=meta('author','article:author')
    if author.startswith(('http://','https://')): author=''
    avatar = ''
    # Some public pages expose the actual post author in structured data.
    def find_author(value):
        if isinstance(value, list):
            for item in value:
                found = find_author(item)
                if found: return found
        elif isinstance(value, dict):
            person = value.get('author')
            if isinstance(person, list): person = person[0] if person else None
            if isinstance(person, dict): return person
            for item in value.values():
                if isinstance(item, (dict, list)):
                    found = find_author(item)
                    if found: return found
        return None
    for script in doc.select('script[type="application/ld+json"]'):
        try:
            person = find_author(json.loads(script.string or script.get_text()))
            if person:
                author = str(person.get('name') or author)
                image_value = person.get('image')
                avatar = image_value.get('url', '') if isinstance(image_value, dict) else (image_value if isinstance(image_value, str) else '')
                break
        except (ValueError, TypeError): pass
    platform=platform_for(url)
    seg=[x for x in urlparse(url).path.split('/') if x]
    handle=seg[1] if platform=='Telegram' and len(seg)>1 and seg[0]=='s' else (seg[0] if seg else '')
    if platform=='Facebook' and handle in ('posts','watch','reel','permalink.php','share','photo.php','story.php','login','login.php'):handle=''
    name=author or (title.split(' on X:')[0] if platform=='X' else '') or handle
    if platform=='Facebook' and not author and title and title.lower() not in ('facebook','log into facebook','log in to facebook'):
        name=title.removesuffix(' | Facebook').strip()[:100]
    # A public OG image is often article media, not a profile avatar. Never claim it is the profile photo.
    output={'url':url,'platform':platform,'handle':handle,'name':name[:100],'text':description[:4000], 'title':title[:240], 'status':'partial'}
    if avatar: output['avatar_data'] = image_data(avatar)
    if platform=='X' and not description:
        raise RuntimeError(x_failure)
    if image:
        output['media_data']=image_data(image)
    if output.get('media_data'):
        output['attachments']=[{'type':'image','data_url':output['media_data']}]
    video_url=meta('og:video:secure_url','og:video:url','og:video')
    if video_url:
        output['attachments']=[]  # OG image is the video's poster, not a separate photo.
        attach_public_video(output,video_url)
    audio_url=meta('og:audio:secure_url','og:audio')
    if audio_url:
        try: output.setdefault('attachments',[]).append(video_data(audio_url,'audio'))
        except Exception as ex: output.setdefault('media_warnings',[]).append('Audio unavailable: '+str(ex)[:160])
    og_icon=meta('twitter:creator')
    if og_icon and not output['handle']: output['handle']=og_icon.lstrip('@')
    # For Telegram publicly rendered posts, the sender avatar is directly accessible as CSS background.
    if platform=='Telegram':
        node=doc.select_one('.tgme_widget_message_user_photo img, .tgme_widget_message_user_photo')
        if node and node.get('src'):output['avatar_data']=image_data(node['src'])
        elif node:
            avatar_match = re.search(r"url\(['\"]?(https://[^)'\"]+)", node.get('style', ''))
            if avatar_match: output['avatar_data'] = image_data(avatar_match.group(1))
        author_node = doc.select_one('.tgme_widget_message_author .tgme_widget_message_author_name, .tgme_widget_message_owner_name')
        if author_node: output['name'] = author_node.get_text(' ', strip=True)[:100]
        content=doc.select_one('.tgme_widget_message_text')
        if content:output['text']=content.get_text(' ',strip=True)[:4000]
    return output


class CaptureUnavailable(RuntimeError):
    pass


def launch_capture_browser(playwright):
    executable = shutil.which('chromium') or shutil.which('google-chrome')
    candidates = ([{'executable_path': executable}] if executable else []) + [{}, {'channel': 'chrome'}, {'channel': 'msedge'}]
    for options in candidates:
        try:
            return playwright.chromium.launch(headless=True, args=['--no-sandbox'], **options)
        except Exception:
            continue
    raise CaptureUnavailable('No working capture browser. Close the helper and run the updated START_ZE_OS.bat to install Chromium.')


def screenshot_public_post(url):
    """Capture an actual public post, reporting why capture could not complete."""
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as BrowserTimeout
    except ImportError:
        return {'capture_error': 'Playwright is missing. Run the updated START_ZE_OS.bat.'}
    try:
        with sync_playwright() as p:
            browser = launch_capture_browser(p)
            try:
                page = browser.new_page(viewport={'width': 1140, 'height': 1380}, device_scale_factor=1)
                response = page.goto(url, wait_until='domcontentloaded', timeout=18000)
                final_path = urlparse(page.url).path.rstrip('/')
                if final_path in ('/login', '/login.php', '/accounts/login'):
                    return {'capture_error': 'The platform redirected the capture browser to login. Use a post available without signing in or import its screenshot.'}
                if response and response.status >= 400:
                    return {'capture_error': f'The platform returned HTTP {response.status} to the capture browser.'}
                platform = platform_for(url)
                selectors = {'X': 'article[data-testid="tweet"]', 'Telegram': '.tgme_widget_message_wrap, .tgme_widget_message', 'Facebook': '[role="article"]', 'Instagram': 'article', 'Threads': 'article'}
                loc = page.locator(selectors[platform]).first
                try:
                    loc.wait_for(state='visible', timeout=7000)
                except BrowserTimeout:
                    return {'capture_error': 'No visible public post appeared in the capture browser. The page may require login or may use an unsupported layout. For a Facebook share link, open it in your browser, click the post date/time, and try that direct post URL.'}
                box = loc.bounding_box()
                if not box or box['width'] <= 250 or box['height'] <= 85:
                    return {'capture_error': 'The visible post was too small to capture reliably.'}
                # Wait for actual post images instead of capturing an unfinished loading state.
                loc.evaluate('(el)=>Promise.all(Array.from(el.querySelectorAll("img")).map(im=>im.complete?Promise.resolve():new Promise(resolve=>{im.addEventListener("load",resolve,{once:true});im.addEventListener("error",resolve,{once:true});setTimeout(resolve,2500)})))')
                pic = loc.screenshot(type='png', timeout=4500, animations='disabled')
                if len(pic) >= 4_000_000:
                    return {'capture_error': 'The post screenshot is too large. Import a cropped screenshot manually.'}
                extracted = {'screenshot_data': 'data:image/png;base64,'+base64.b64encode(pic).decode()}
                # Keep attachments separate from the flattened screenshot where the page exposes them.
                extracted['attachments']=[]
                image_urls=loc.locator('img').evaluate_all('(nodes)=>nodes.filter(im=>im.naturalWidth>=240 && im.naturalHeight>=120 && !im.closest("header,h2,h3")).map(im=>im.currentSrc||im.src).slice(0,8)')
                for media_url in dict.fromkeys(image_urls):
                    image=image_data(media_url)
                    if image: extracted['attachments'].append({'type':'image','data_url':image})
                videos=loc.locator('video').evaluate_all('(nodes)=>nodes.map(v=>v.currentSrc||v.src||v.querySelector("source")?.src||"").slice(0,2)')
                for media_url in dict.fromkeys(videos):
                    if media_url.startswith('https://'): attach_public_video(extracted,media_url)
                    else: extracted.setdefault('media_warnings',[]).append('Video is visible but its original file is not publicly downloadable. Add it locally.')
                # Missing author information must not discard an otherwise valid post screenshot.
                try:
                    author_selectors = {'X': '[data-testid="User-Name"] a', 'Facebook': 'h2 a, h3 a, strong a', 'Instagram': 'header a', 'Telegram': '.tgme_widget_message_author_name', 'Threads': 'header a'}
                    avatar_selectors = {'X': '[data-testid="Tweet-User-Avatar"] img', 'Facebook': 'svg image', 'Instagram': 'header img', 'Telegram': '.tgme_widget_message_user_photo img', 'Threads': 'header img'}
                    author = loc.locator(author_selectors[platform]).first
                    if author.count(): extracted['name'] = author.inner_text(timeout=1000).strip()[:100]
                    avatar = loc.locator(avatar_selectors[platform]).first
                    if avatar.count():
                        avatar_url = avatar.evaluate('(el)=>el.currentSrc || el.src || el.getAttribute("href") || el.getAttribute("xlink:href")')
                        if avatar_url: extracted['avatar_data'] = image_data(avatar_url)
                except Exception:
                    pass
                return extracted
            finally:
                browser.close()
    except CaptureUnavailable as ex:
        return {'capture_error': str(ex)}
    except BrowserTimeout:
        return {'capture_error': 'The capture browser timed out while opening the public post.'}
    except Exception as ex:
        return {'capture_error': f'Capture browser failed ({type(ex).__name__}). Check the helper window and try a direct public post URL.'}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
    def _send_media(self,path):
        if not path.is_file():self.send_error(404);return
        size=path.stat().st_size;start=0;end=size-1;partial=False
        requested=self.headers.get('Range')
        if requested:
            match=re.fullmatch(r'bytes=(\d*)-(\d*)',requested)
            if not match or not any(match.groups()):self.send_error(416);return
            first,last=match.groups()
            if first:start=int(first);end=min(int(last),end) if last else end
            else:start=max(0,size-int(last))
            if start>=size or end<start:
                self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();return
            partial=True
        self.send_response(206 if partial else 200)
        self.send_header('Content-Type',mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        self.send_header('Accept-Ranges','bytes')
        self.send_header('Content-Length',str(end-start+1))
        if partial:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.end_headers()
        try:
            with path.open('rb') as source:
                source.seek(start);remaining=end-start+1
                while remaining:
                    chunk=source.read(min(65536,remaining))
                    if not chunk:break
                    self.wfile.write(chunk);remaining-=len(chunk)
        except (BrokenPipeError,ConnectionResetError):pass
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Methods','GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
    def do_GET(self):
        media_path=urlparse(self.path).path
        if media_path.startswith('/.ze_media/'):
            filename=media_path.removeprefix('/.ze_media/')
            if not re.fullmatch(r'[a-f0-9]{32}\.(mp4|webm|mp3|m4a|ogg|wav)',filename):self.send_error(404);return
            return self._send_media(MEDIA_ROOT/filename)
        if urlparse(self.path).path == '/api/health':
            payload=json.dumps({'service':'ze-os-importer','version':'0.7-beta2.7.4'}).encode()
            self.send_response(200)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(payload)))
            self.send_header('Cache-Control','no-store')
            self.end_headers();self.wfile.write(payload)
            return
        if not self.path.startswith('/api/post?'):return super().do_GET()
        try:
            q=parse_qs(urlparse(self.path).query)
            url=q.get('url',[''])[0]
            public_url(url,KNOWN)
            failure=None
            try: data=fetch_metadata(url)
            except Exception as ex:
                failure=ex
                data={'url':url,'platform':platform_for(url),'status':'partial'}
            screen=screenshot_public_post(url)
            if screen and screen.get('screenshot_data'):
                attachments=data.get('attachments',[])
                warnings=data.get('media_warnings',[])
                data.update({key:value for key,value in screen.items() if value and key not in ('attachments','media_warnings')})
                # Prefer real post attachments found in the browser over an OG thumbnail.
                data['attachments']=screen.get('attachments') or attachments
                data['media_warnings']=warnings+screen.get('media_warnings',[])
                data['status']='captured'
            elif failure:
                detail=(screen or {}).get('capture_error','Capture did not return a screenshot.')
                raise RuntimeError(str(failure)+' Screenshot capture: '+detail)
            elif screen and screen.get('capture_error'):
                data['capture_warning']=screen['capture_error']
            payload=json.dumps(data,ensure_ascii=False).encode('utf-8');code=200
        except Exception as e:
            code=422
            payload=json.dumps({'error':str(e)[:1200]},ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(payload)))
        self.send_header('Cache-Control','no-store')
        self.end_headers();self.wfile.write(payload)

    def end_headers(self):
        origin = self.headers.get('Origin', '')
        p = urlparse(origin)
        if origin == 'null' or (p.scheme == 'http' and p.hostname in ('127.0.0.1', 'localhost')):
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Access-Control-Allow-Private-Network','true')
            self.send_header('Vary', 'Origin')
        super().end_headers()

if __name__=='__main__':
    if '--check-browser' in sys.argv:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser=launch_capture_browser(p);browser.close()
            print('Capture browser is ready.');sys.exit(0)
        except Exception as ex:
            print('Capture browser is not ready:',str(ex)[:300]);sys.exit(1)
    import webbrowser
    port=int(os.environ.get('ZE_OS_PORT','8765'))
    try:server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    except OSError as ex:
        print('Unable to start ZE OS local importer:',ex);sys.exit(1)
    url=f'http://127.0.0.1:{port}/ZE_OS_Mouwajaha_V07.html'
    print('ZE OS Mouwajaha V0.7:',url)
    print('Local importer listens on this computer only. Press Ctrl+C to stop.')
    webbrowser.open(url)
    try:server.serve_forever()
    except KeyboardInterrupt:server.shutdown()
