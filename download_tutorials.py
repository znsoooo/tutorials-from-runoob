import io
import re
import gzip
import urllib.request

from lxml import etree


def getcontent(url):
    if not url.startswith('http:'):
        url = 'http:' + url

    mainpage = urllib.request.urlopen(url)
    type = mainpage.info().get('Content-Encoding')
    if type == 'gzip':
        mainpage = urllib.request.urlopen(url)
        tmp = io.StringIO.StringIO(mainpage.read())
        data = gzip.GzipFile(fileobj=tmp)
    else:
        data = mainpage
    return data


def gettutorial(title, url):
    print('[**]' + url)
    num = 0
    file = open(title + '.html', 'a')
    content = getcontent(url)
    html = etree.HTML(content.read())
    url = html.xpath('/html/body/div[3]/div/div[1]/div[2]/div//a/@href')
    pre = ''
    for item in url:
        mytest = item.split('/')
        if len(mytest) == 3:
            pre = mytest[1]
        elif len(mytest) == 1:
            item = '/' + pre + '/' + item
        else:
            continue
        item = 'http://www.runoob.com' + item
        print('[**]\t' + item)
        data = getcontent(item)

        # replace js/css/images
        if num == 0:
            for tmp in data.readlines()[:-1]:
                tmp = tmp.replace('/wp-content/themes/runoob/', './runoob/').replace('//cdn.bootcss.com/font-awesome/4.7.0/', './runoob/').replace('//cdn.bootcss.com/jquery/2.0.3', './runoob/')
                file.write(tmp)
        else:
            for tmp in data.readlines()[24:-1]:
                tmp = tmp.replace('/wp-content/themes/runoob/', './runoob/').replace('//cdn.bootcss.com/font-awesome/4.7.0/', './runoob/').replace('//cdn.bootcss.com/jquery/2.0.3', './runoob/')
                file.write(tmp)
        num += 1
    file.write('</html>')
    file.close()


data = getcontent('http://www.runoob.com')
html = etree.HTML(data.read())
theme = html.xpath('/html/body/div[4]/div/div[2]//a')
num = 0
for a in theme:
    title = theme[num].xpath('./h4/text()')[0].strip()
    title = re.sub('/', '-', title)
    suburl = theme[num].xpath('./@href')[0].strip()
    suburl = str(suburl)
    gettutorial(title, suburl)
    num += 1
