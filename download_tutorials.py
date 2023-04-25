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


def GetContent(url, cache=True, save=True):
    path = re.sub(r'^https?://[^/]*?/', 'html/', url)
    if cache and os.path.exists(path) and os.path.getsize(path): # read from cache
        with open(path, 'rb') as f:
            return f.read()
    else:
        req = urllib.request.urlopen(url)
        if 'gzip' == req.info().get('Content-Encoding'):
            f = io.StringIO.StringIO(req.read())
            req = gzip.GzipFile(fileobj=f)
        data = req.read()
        if save:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                f.write(data)
        return data


def WalkHtmls(url):
    urls = [url]
    history = []
    while urls:
        url = urls.pop(0)
        print(f'Done: {len(history)}, Todo: {len(urls)}, Err: {len(errors)}, Url: {url}')
        try:
            data = GetContent(url)
            history.append(url)
        except Exception: # urllib.error.HTTPError:
            errors.append(url)
            continue
        for suburl in re.findall(b'''href=['"]([^'"]*?\.html)['"]''', data):
            suburl = urllib.parse.urljoin(url, suburl.decode())
            suburl = re.sub(r'^https?', 'http', suburl)
            if suburl.startswith(HOME_PAGE) and suburl not in urls + history + errors:
                urls.append(suburl)


def WashHtmls():
    for file in glob.glob('html/**/*.html', recursive=True):
        with open(file, 'rb') as f:
            text = f.read()

        # replace `PATH/NAME.css?PARMS` to `/0/NAME.css?PARMS`
        text = re.sub(rb'''(href=['"])[^'"]*?([^'"/]*?\.css)\b''', rb'\1/0/\2', text)

        # replace homepage to `/`
        # e.g. 'http://homepage/', 'https://homepage/', '//homepage/', 'homepage/'
        text = re.sub(rf'''(?<=href=['"])[^'"]*?{re.escape(WWW)}/'''.encode(), b'/', text)

        # replace `/` to relative path
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
