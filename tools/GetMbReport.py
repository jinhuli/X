#coding=GBK
import queue
import threading
import urllib.request
import urllib.parse
import http.cookiejar
import re

import time
import re
from bs4 import *

pages = queue.Queue()

dlurl = 'http://www.hibor.com.cn/toplogin.asp?action=login'
url = 'http://www.hibor.com.cn/result.asp?lm=0&area=DocTitle&timess=13&key=&dtype=&page=1'
headers  = {
'Connection':' keep-alive',
'Upgrade-Insecure-Requests':' 1',
'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}



def hibor():
    dlurl =  'http://www.hibor.com.cn/toplogin.asp?action=login'
    url = 'http://www.hibor.com.cn/result.asp?lm=0&area=DocTitle&timess=13&key=&dtype=&page=1'

    datapost = {"name":"xuzhipeng8","pwd":'xuzhipeng8261426','tijiao.x':'12','tijiao.y':'2','checkbox': 'on'}
    postdata = urllib.parse.urlencode(datapost).encode("utf-8")
    req = urllib.request.Request(dlurl,postdata, headers=headers)
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    urllib.request.install_opener(opener)
    file =opener.open(req)
    data = file.read()


    writeindex = open('page.html', 'wb')
    writeindex.write(data)
    writeindex.close()
    get_request = urllib.request.Request(url,headers = headers)
    data2 = opener.open(get_request).read()

    writeindex2 = open('page3.html', 'wb')
    writeindex2.write(data2)
    writeindex2.close()

    soup =  BeautifulSoup(data2, "html5lib")
    soup1 = soup.find('div', {"class": "classbaogao_sousuonew"})
    soup2 = soup1.findAll('div', {"class": "classbaogao_sousuo_new_result"})
    outdatalist = []
    for i in range(len(soup2)):
        outdata =[]
        outdata[1] = soup2[i].find_all("span")[1].text
        outdata[2] =  soup2[i].find_all("span")[3].text
        outdata[3] = soup2[i].find_all("span")[5].text
        outdata[4] = soup2[i].find_all("span")[6].text
        outdata[5] = soup2[i].find_all("span")[7].text
        outdata[6] = soup2[i].find_all("span")[8].text






class ThreadUrl(threading.Thread):
    def __init__(self, pages):
        threading.Thread.__init__(self)
        self.conn = pymysql.connect("localhost","root","8261426","stock"
                                  ,use_unicode=True, charset="utf8")
        self.cursor =self.conn.cursor()
        self.pages = pages
        self.headers=['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36']
        self.postdata = urllib.parse.urlencode({"changeno":"1","namelogin":"xuzhipeng8","pwdlogin":"xuzhipeng8261426","checkboxlogin":"on","button":"%B5%C7++%C2%BC"}).encode("utf-8")
        req = urllib.request.Request(url,self.postdata)
        req.add_header(self.headers[0],self.headers[1])
        cjar =http.cookiejar.CookieJar()
        #使用 创建cookie处理器，并以其为参数构建opener对象
        opener =urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
        urllib.request.install_opener(req)
        file = opener.open(req)
        data = file.read()

    def run(self):

        while True:

            try:

                TotalAbstract = ''
                page = pages.get()
                try:
                    ie1.navigate(page)
                    chunk = ie1.getPageText()
                except:
                    try:
                        ie1.navigate(page)
                        chunk = ie1.getPageText()
                    except:
                        ie1.navigate(page)
                        chunk = ie1.getPageText()
                print('souping+' + page + '\n')

                soup = BeautifulSoup(chunk)
                soup1 = soup.find('div', {"class": "classbaogao_sousuonew"})
                chunks = soup1.findAll('td')
                stockName = chunks[1].find('b').string  # 股票名称
                if stockName == None:
                    stockName = str(stockName)
                print(stockName + '\n')
                reportAuthor = chunks[3].find('b').string  # 研究报告作者
                if reportAuthor == None:
                    reportAuthor = str(reportAuthor)
                print(reportAuthor + '\n')
                stockCode = chunks[6].find('b').string  # 股票代码
                if stockCode == None:
                    stockCode = str(stockCode)
                print(stockCode + '\n')
                reportBelongCompany = chunks[8].find('b').string  # 研究报告出处
                if reportBelongCompany == None:
                    reportBelongCompany = str(reportBelongCompany)
                print(reportBelongCompany + '\n')
                rateLevel = chunks[11].find('b').string  # 推荐评级
                if rateLevel == None:
                    rateLevel = str(rateLevel)
                print(rateLevel + '\n')
                reportType = chunks[13].find('b').string  # 研究报告栏目
                if reportType == None:
                    reportType = str(reportType)
                print(reportType + '\n')
                Title = soup.find('strong').string
                print(Title + '\n')
                time = chunks[18].find('b').string
                tmptimes = time.split(' ')
                time = tmptimes[0]
                timechunks = time.split('-')
                if len(timechunks) == 3:
                    if len(timechunks[1]) == 1:
                        timechunks[1] = '0' + timechunks[1]
                    if len(timechunks[2]) == 1:
                        timechunks[2] = '0' + timechunks[2]
                time = timechunks[0] + timechunks[1] + timechunks[2]
                Title = Title
                ContentAbstractArea = soup.find('div', {"class": "new_content"})
                if ContentAbstractArea != None:
                    tmp = ContentAbstractArea.find('td')
                    tmpStr = str(tmp)
                    abstract = tmpStr[34:-12].replace(
                        '<font style="DISPLAY:none;"><a href="http://www.microbell.com/">www.microbell.com</a>(\xe8\xbf\x88\xe5\x8d\x9a\xe6\xb1\x87\xe9\x87\x91)\xe3\x80\x82</font>',
                        '\n')
                    abstract = abstract.replace('&nbsp;', '')
                    abstract = abstract.replace('<br />', '')
                    abstract = abstract.replace('\n', '')
                    TotalAbstract = TotalAbstract + abstract + '\n'
                ##INSERT THE INFO TYPE:GBK
                print('#################################')
                try:
                    self.cursor.execute(
                        "insert into MBStrategy values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                        page, Title, TotalAbstract.decode('utf-8'), time, reportAuthor, stockCode, reportBelongCompany,
                        rateLevel, reportType))
                    self.conn.commit()
                except Exception as e:
                    print(e)

                print('************************************')
            except:
                writeindex = file('pagesErro.txt', 'a+')
                writeindex.write(page + '\n')
                writeindex.close()
                continue

def main():
    # oriUrl='http://www.microbell.com/result.asp?lm=0&area=DocTitle&timess=13&key=&page=1'
    oriUrl = 'http://www.hibor.com.cn/result.asp?lm=0&area=DocTitle&timess=13&key=&dtype=&page=1'

    for i in range(1, 80):
        hosts.put(oriUrl[:-1] + str(i))


    # spawn a pool of threads.
    for i in range(1):
        t = ThreadUrl(hosts, pages)
        t.setDaemon(True)
        t.start()

    for i in range(1):
        dt = ThreadUrlSecond(hosts, pages)
        dt.setDaemon(True)
        dt.start()
        print('bbbb')

    # wait on the queue until everything has been processed
    hosts.join()
    pages.join()


main()
filr2.close()
filr1.close()


