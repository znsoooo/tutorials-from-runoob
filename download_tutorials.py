import io
import os
import re
import glob
import gzip
import urllib.parse
import urllib.request

WWW       = 'www.runoob.com'
HOME_PAGE = 'http://' + WWW

errors = []


def SaveHtml(url, data):
    path = re.sub(r'^https?://[^/]*?/', 'html/', url)
    if path.endswith('/'):
        path += 'index.html'
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)


def GetContent(url, cache=True, save=True):
    path = re.sub(r'^https?://[^/]*?/', 'html/', url)
    if cache and os.path.exists(path) and os.path.getsize(path): # read from cache
        with open(path, 'rb') as f:
            data = f.read()
    else:
        req = urllib.request.urlopen(url)
        data = req.read()
        save and SaveHtml(url, data) # save to reltive path
        url = req.geturl() # get real url
        save and SaveHtml(url, data) # save to real path
    return url, data


def WalkHtmls(url):
    todo = [url]
    done = []
    cnt = 0
    while todo:
        url = todo.pop(0)
        cnt += 1
        if cnt % 100 == 1:
            print(f'Done: {len(done)}, Todo: {len(todo)}, Err: {len(errors)}, Url: {url}')
        try:
            realurl, data = GetContent(url)
            done.append(url)
            url = realurl # for `urljoin` get correct suburl
        except Exception as e: # urllib.error.HTTPError:
            print(f'Error: {e}, Url: {url}')
            errors.append(url)
            continue
        for suburl in re.findall(b'''href=['"]([^'"]*?\.html)['"]''', data):
            suburl = urllib.parse.urljoin(url, suburl.decode())
            suburl = re.sub(r'^https?', 'http', suburl)
            if suburl.startswith(HOME_PAGE) and suburl not in todo + done + errors:
                todo.append(suburl)


def WashHtmls():
    for cnt, file in enumerate(glob.glob('html/**/*.html', recursive=True)):
        if cnt % 1000 == 0:
            print(f'Wash: {cnt + 1}, File: {file}')

        with open(file, 'rb') as f:
            text = f.read()

        # replace 'PATH/NAME.css?PARMS' to '/0/NAME.css?PARMS'
        text = re.sub(rb'''(href=['"])[^'"]*?([^'"/]*?\.css)\b''', rb'\1/0/\2', text)

        # replace 'PATH/NAME.js?PARMS' to ''
        text = re.sub(rb'''(?<=src=['"])[^'"]*?\.js(?:\?[^'"]*?)?(?=['"])''', b'', text)

        # replace homepage to '/'
        # e.g. 'http://homepage/', 'https://homepage/', '//homepage/', 'homepage/'
        text = re.sub(rf'''(?<=href=['"])[^'"]*?{re.escape(WWW)}/'''.encode(), b'/', text)

        # replace '/' to relative path
        level = file.count('\\') - 1
        rel = '../' * level or './'
        text = re.sub(rb'''(?<=href=['"])/''', rel.encode(), text)

        with open(file, 'wb') as f:
            f.write(text)


if __name__ == '__main__':
    WalkHtmls(HOME_PAGE + '/index.html')
    WashHtmls()
    print('errors:')
    print('\n'.join(errors))
