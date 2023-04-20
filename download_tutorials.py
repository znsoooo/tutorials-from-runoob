import io
import os
import re
import glob
import gzip
import urllib.request

from lxml import etree

HOME_PAGE = 'http://www.runoob.com'
errors = []


def SaveHtml(url, data):
    path = url.replace(HOME_PAGE, 'html')
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, 'w', encoding='u8') as f:
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
            data2 = GetContent(url2).decode()
            SaveHtml(url2, data2)
        except Exception:
            errors.append(url2)


def GetTutorial():
    url = HOME_PAGE + '/index.html'
    data = GetContent(url)
    SaveHtml(url, data.decode())
    html = etree.HTML(data)
    theme = html.xpath('/html/body/div[4]/div/div[2]/div/a')
    for a in theme:
        title = a.xpath('./h4/text()')[0].strip()
        title = re.sub('/', '-', title)
        url = 'http:' + a.xpath('./@href')[0].strip()
        GetSubTutorial(title, url)


if __name__ == '__main__':
    GetTutorial()
    print('errors:')
    print('\n'.join(errors))
