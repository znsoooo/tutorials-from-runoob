import io
import os
import re
import glob
import gzip
import urllib.request

from lxml import etree

WWW       = 'www.runoob.com'
HOME_PAGE = 'http://' + WWW

errors = []


def SaveHtml(url, data):
    path = url.replace(HOME_PAGE, 'html')
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)


def GetContent(url):
    path = url.replace(HOME_PAGE, 'html')
    if os.path.exists(path) and os.path.getsize(path): # read from cache
        with open(path, 'rb') as f:
            return f.read()
    else:
        req = urllib.request.urlopen(url)
        if 'gzip' == req.info().get('Content-Encoding'):
            f = io.StringIO.StringIO(req.read())
            req = gzip.GzipFile(fileobj=f)
        return req.read()


def GetSubTutorial(title, url):
    print('- ' + url)
    data = GetContent(url)
    html = etree.HTML(data)
    urls = html.xpath('/html/body/div[4]/div/div/div/div[2]/div/a/@href')
    base = os.path.dirname(url) + '/'
    for url2 in urls:
        url2 = HOME_PAGE + url2 if '/' in url2 else base + url2
        print('| - ' + url2)
        try:
            data2 = GetContent(url2)
            SaveHtml(url2, data2)
        except Exception:
            errors.append(url2)


def GetTutorial():
    url = HOME_PAGE + '/index.html'
    data = GetContent(url)
    SaveHtml(url, data)
    html = etree.HTML(data)
    theme = html.xpath('/html/body/div[4]/div/div[2]/div/a')
    for a in theme:
        title = a.xpath('./h4/text()')[0].strip()
        title = re.sub('/', '-', title)
        url = 'http:' + a.xpath('./@href')[0].strip()
        GetSubTutorial(title, url)


def WashHtmls():
    for file in glob.glob('html/**/*.html', recursive=True):
        with open(file, 'rb') as f:
            text = f.read()

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
    GetTutorial()
    WashHtmls()
    print('errors:')
    print('\n'.join(errors))
