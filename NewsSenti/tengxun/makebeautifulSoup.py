#coding=utf-8
import random
import time
import json
import chardet
import requests
import retrying
from bs4 import BeautifulSoup

class makeBS:
    @retrying.retry(stop_max_attempt_number=4)     #重试4次，每次等待多久呢
    def mobiResponse(self,requestURL):           #这个留着吧
        print(requestURL)
        rollLatest = "http://news.163.com/latest/"
        # requestURL = "http://news.163.com/special/0001220O/news_json.js?0.3699326344116929"
        # requests.get(requestURL)
        # rawReferer = '.qq.com/articleList/rolls/'  # 'http://news   前面还有这个东西
        my_headers = [  # 这边为了得到直接的手机端的页面代码返回，直接使用手机ua
            # 'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN',
            # 'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 Maxthon/3047',
            'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
            # 'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; STF-AL00 Build/HUAWEISTF-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36',
            # 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-C7000 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.2.948 Mobile Safari/537.36',
            # 'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080'
            ]
        headers = {"User-Agent": random.choice(my_headers), 'Referer':requestURL}  # 默认值
        try:
            rawhtml = requests.get(requestURL, headers=headers, allow_redirects=True,             #跳转怎么是false
                                   timeout=30)  # 一般提取文本的话，那就用text，如果是文件就content
            # print(rawhtml.headers)
            # print()
            # rawhtml.encoding = "GBK"  ##gbk>gb2312   使用这种方式尚且还有乱码的情况，部分乱码，那就是gbk可以修复
            # print(chardet.detect(rawhtml.content)['encoding'])

            if ("GB2312" == chardet.detect(rawhtml.content)['encoding']):
                rawhtml.encoding = "gbk"
            else:
                rawhtml.encoding = chardet.detect(rawhtml.content)['encoding']  # 这样应该就可以直接默认来编码了

            if rawhtml.status_code == 504:
                print(504)
                return
            print(rawhtml.url)
            print("状态码" + str(rawhtml.status_code))
            # print("页面的读取结果为")
            html = rawhtml.text
            return html          #返回了这个网页的html 文档，然后再解析一次就可以了
        except Exception as e:
            print(e)
            return


    def makesoup(self,url):  # 这儿是按页来打开的
        if url==None:
            return
        my_headers = [
            'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
            'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
            'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']

        headers = {"User-Agent": random.choice(my_headers)}  #默认值


        if(url.find("ifeng.com")!=-1):  #是凤凰的网址的话
            print("fenghuangNews")
            headers = {"User-Agent": random.choice(my_headers),
                       "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                       'Accept-Encoding':'gbk, utf-8',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       }

        if (url.find(".qq.com")!=-1):
            print("qqnews")
            headers = {
                          "User-Agent": random.choice(my_headers),
                          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                          'Accept-Encoding': 'gbk, utf-8',
                          'Accept-Language': 'zh-CN,zh;q=0.9',
                            'referer':url
            }

        """
        获取网站的soup对象，#看看还能不能增加代理的东西，进来
        有两个请求头的自定义，但是，为什么要分开来呢
        """
        # else:
        #     headers = {"User-Agent": random.choice(my_headers)}
        soup = None
        address  = "http://223.203.0.14:8000" #默就是用了代理，怎么还是失败呢
        # address = None  #访问页面的这个要使用代理才可以
        proxies = {'http': address, "https": address}  # , 'https': 'http://localhost:8888'，这儿现在就是没用代理的情况下

        try:
            rawhtml = requests.get(url, headers=headers, allow_redirects=True,timeout=60)  #一般提取文本的话，那就用text，如果是文件就content
            if url.find("ifeng")!=-1:
                # print(chardet.detect(rawhtml.content)['encoding'])   经常性的检测错误
                print(chardet.detect(rawhtml.content)['encoding'])
                if ("GB2312"== chardet.detect(rawhtml.content)['encoding']):
                    rawhtml.encoding = "gbk"
                else:
                    rawhtml.encoding = "utf-8"  # 这样应该就可以直接默认来编码了
                # print(rawhtml.history)
            else:
                rawhtml.encoding = chardet.detect(rawhtml.content)['encoding']  #这样应该就可以直接默认来编码了
            # print(rawhtml.status_code)
            # print(rawhtml.headers)

            soup = BeautifulSoup(rawhtml.text, 'lxml')
            return soup

        except Exception as e:  #如果超时的话就变成这样子
            print(e)
            # print(rawhtml.status_code)

            return soup  #没有的话就是返回空的在这儿的None



        # if(url.find("http://news.ifeng.com")!=-1): #凤凰的页面要转码
        #     rawhtml.encoding = 'utf-8'
        #
        # #html  =   # 不允许你跳转，就访问这个就是了，改成request后就是这个样子
        # try:
        #     soup = BeautifulSoup(rawhtml.text, 'lxml')
        # except Exception as e:
        #     print(url)
        #     print(e)
        #     time.sleep(1)
        #     rawhtml.encoding ="gbk"
        # soup = BeautifulSoup(rawhtml.text, 'lxml')
        # print(soup)
        # return soup

if __name__ == "__main__":  #这个就是url的东西
    # BS = makeBS.makesoup('https://xw.qq.com/news/20171230004716/NEW20171230004716.htm')  ##p=1

      # p=1
    # url = 'https://news.qq.com/a/20171230/002476.htm#p=6'
    # changerUrl = "https://xw.qq.com/news/20171230007278/NEW2017123000727800"
    # print(BS.find("span",attrs={"tatolNum"}))
    # print(BS)
    # for i in BS.find_all("img",attrs={"src":True,"alt":True}):
    #     print(i)
    # print(BS.find("title"))  #ddd

    # url = "http://c.m.163.com/nc/article/headline/T1348647853363/0-100.html"
    #
    # url = "http://sports.qq.com/a/20180925/013599.htm"
    # url = "http://sports.qq.com/a/20180925/013599.htm"
    # url = "http://sports.qq.com/a/20180925/013599.htm"
    # sporturl = "https://xw.qq.com/a/sports/20180925013599"  #直接通过这个组合成就可以了，这样生了一次请求
    # Sporturl = "https://xw.qq.com/c/sports/20180925013599"
    # entUrl ="https://xw.qq.com/a/news/20180925000977"
    # Cooker = makeBS()
    # BS = Cooker.makesoup(Sporturl)
    # # print(BS)
    #
    # dicString = BS.find("script",attrs={"async":False}).text
    # dic = dicString.replace("var globalConfig =","").replace(";","")
    # if dic.find("contents: ")!=-1:
    #     datalist = dic.split("contents: ")[1].split("ext_data")[0].replace("[","").replace("],","")
    #     dic = eval("("+datalist+")")
    # #     print(dic[0])
    #     for p in dic:
    # #         if type(p)=="<class 'tuple'>":
    #         if p['type']==1: #这个是一个句子，那就直接插进去就可以了
    #             #当成句子插入
    #             print(p['value'])
    #         if p['type']==2:
    #             print(p['value'].replace("\/","/"))
    #             print("这个是图片了")


    # todo 现在的进度是  ，有些链接直接使用本机？还是使用代理打不开，不知道是不是和本机电脑C盘不够有关
    # todo 提取到分类到了 ，科技的，可能打不开，页面
    # url="https://news.qq.com//a//20181004//007938.htm"
    url = "https://pl.ifeng.com/a/20181010/60101359_0.shtml"

    cooker = makeBS()
    # html = cooker.mobiResponse(url)
    html = cooker.makesoup(url)
    # print(html)
    # print(len(str(html)))



