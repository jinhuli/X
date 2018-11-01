#coding=GBK
import queue
import threading
import urllib.request
import urllib.parse
import http.cookiejar
import pandas as pd
from bs4 import *
from tools.toMysql import *
import re




url = 'http://www.hibor.com.cn/result.asp?lm=0&area=DocTitle&timess=13&key=&dtype=&page=21'
def hibor(url):

    headers = {
        'Connection': ' keep-alive',
        'Upgrade-Insecure-Requests': ' 1',
        'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    }



    dlurl =  'http://www.hibor.com.cn/toplogin.asp?action=login'
    datapost = {"name":"xuzhipeng8","pwd":'xuzhipeng8261426','tijiao.x':'12','tijiao.y':'2','checkbox': 'on'}
    postdata = urllib.parse.urlencode(datapost).encode("utf-8")
    req = urllib.request.Request(dlurl,postdata, headers=headers)
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    urllib.request.install_opener(opener)
    file =opener.open(req)
    #data = file.read()
    #file = open("pages.html", "wb")
    #file.write(data)
    #file.close()


    get_request = urllib.request.Request(url,headers = headers)
    data2 = opener.open(get_request).read()

    #handle = open("pages.html","wb")
    #handle.write(data2)
    #handle.close()

    soup =  BeautifulSoup(data2, "html5lib")
    soup1 = soup.find('div',{"class": "index_docmain"})
    soup2 = soup1.findAll('div', {"class": "classbaogao_sousuo_new_result"})

    pddata = pd.DataFrame([], columns=["券商", "标题", "日期", "类别", "作者", "评级", "页数"])
    for i in range(len(soup2)):
        if len(soup2[i].find_all("span"))<8:
            pass
        else:
            pddata.loc[i] = [
            soup2[i].find_all("span")[1].text[0:4],
            soup2[i].find_all("span")[1].text[5:],
            soup2[i].find_all("span")[3].text,
            soup2[i].find_all("span")[5].text[3:],
            soup2[i].find_all("span")[6].text[3:],
            soup2[i].find_all("span")[7].text[3:],
            soup2[i].find_all("span")[8].text[3:]]

    return pddata



class ThreadUrl(object):
    def __init__(self, pages):
        self.pages = pages
        self.con = MySQLAlchemy(report, "stock")
        self.headers = {
            'Connection': ' keep-alive',
            'Upgrade-Insecure-Requests': ' 1',
            'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }
        dlurl = 'http://www.hibor.com.cn/toplogin.asp?action=login'
        datapost = {"name": "xuzhipeng8", "pwd": 'xuzhipeng8261426', 'tijiao.x': '12', 'tijiao.y': '2',
                    'checkbox': 'on'}
        postdata = urllib.parse.urlencode(datapost).encode("utf-8")
        req = urllib.request.Request(dlurl, postdata, headers=self.headers)
        cjar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
        urllib.request.install_opener(self.opener)
        file=self.opener.open(req)
        data = file.read()
        file = open("pages.html", "wb")
        file.write(data)
        file.close()

    def run(self):

        while True:
            url = self.pages.get()
            print("爬取",url)
            get_request = urllib.request.Request(url, headers=self.headers)
            data2 = self.opener.open(get_request).read()
            soup = BeautifulSoup(data2, "html5lib")
            soup1 = soup.find('div', {"class": "index_docmain"})
            soup2 = soup1.findAll('div', {"class": "classbaogao_sousuo_new_result"})

            pddata = pd.DataFrame([], columns=["券商", "标题", "日期", "类别", "作者", "评级", "页数"])
            for i in range(len(soup2)):
                if len(soup2[i].find_all("span")) < 8:
                    pass
                else:
                    pddata.loc[i] = [
                        soup2[i].find_all("span")[1].text[0:4],
                        soup2[i].find_all("span")[1].text[5:],
                        soup2[i].find_all("span")[3].text,
                        soup2[i].find_all("span")[5].text[3:],
                        soup2[i].find_all("span")[6].text[3:],
                        soup2[i].find_all("span")[7].text[3:],
                        soup2[i].find_all("span")[8].text[3:]]
                    #print(soup2[i])
                    #error_data = str(soup2[i])
                    #error = open(".\error_data.txt", "r")
                    #error.write(error_data)
                    #error.write("\n")
                    #error.close()


            print(pddata.head())
            reports = [report(name=pddata["券商"][j], title=pddata["标题"][j], date=pddata["日期"][j], \
                             classes=pddata["类别"][j], author=pddata["作者"][j], score=pddata["评级"][j],\
                             pages=int(pddata["页数"][j][0])) for j in range(len(pddata))]
            self.con.insert(reports, 2)
            if self.pages.empty():
                break


def main():
    # oriUrl='http://www.microbell.com/result.asp?lm=0&area=DocTitle&timess=13&key=&page=1'
    oriUrl = 'http://www.hibor.com.cn/result.asp?lm=0&area=DocTitle&timess=13&key=&dtype=&page=21'
    pages =queue.Queue()
    for i in range(1, 51):
        pages.put(oriUrl[:-1] + str(i))


    t = ThreadUrl(pages)
    t.run()

if __name__ == '__main__':
    main()





