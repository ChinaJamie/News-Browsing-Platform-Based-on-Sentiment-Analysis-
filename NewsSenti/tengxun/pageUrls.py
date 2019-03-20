import gzip
import json
import random
import urllib.request
from urllib import parse
import time
import chardet
import requests
from pprint import pprint

from DBcontrol import DB
from TimeHelper import TimeHelper


class DateUrl:
    def __init__(self):
        self.dbhelper = DB()                #默认就给你创建好了，

    def getDateUrlList(self,startDate,endDate): #返回这两个日期区间的url,顺便就写入数据库了
        urlList =[]
        timehelper=TimeHelper()
        datelist = []
        if(startDate!=endDate):  #不相等的时候就算差值
            datelist = timehelper.getTimeList(startDate,endDate)
        else:
            datelist.append(startDate)
        for oneDay in datelist:      #这儿也设置了休眠的
            time.sleep(1.5) #500毫秒一次，那我设置成800毫秒请求一次
            onedatelist=[]
            try:
                onedatelist = self.getOneDayNewUrl(oneDay)
            except Exception:
                time.sleep(30)
                onedatelist = self.getOneDayNewUrl(oneDay)
            urlList = urlList+onedatelist

            # self.saveListToMysql(onedatelist,oneDay,"tengxun")  #存到数据库里面去，把每个都插入进去
        return urlList

    def getOneDayNewUrl(self, date):
        date = parse.quote_plus(""+date)
        oneDayUrlList = []
        print(str(date))
        # date = "2018-07-26"
        appid = "3639833dae924cb9efb6ba30e6c5a6fa"
        url = "https://api.shenjian.io/?appid=" + appid + "&date=" + date
        # print(url)
        request = urllib.request.Request(url,
        headers={
            "Accept-Encoding": "gzip",
        })

        response = urllib.request.urlopen(request)
        gzipFile = gzip.GzipFile(fileobj=response)
        # print(gzipFile.read().decode('UTF-8'))
        jsonResult = json.loads(str(gzipFile.read().decode('UTF-8')))
        if "data" in jsonResult:
            print (jsonResult['data'])
            print("共有多少个新闻" + str(len(jsonResult['data'])))
            if(len(jsonResult['data'])==4):
                oneDayUrlList.append(jsonResult['data']['url'])
                return oneDayUrlList
            else:
                for i in jsonResult['data']:
                    # print(i['url'])
                    oneDayUrlList.append(i['url'])
                return oneDayUrlList
        else :
            print("检测到腾讯的api 中无  data key 10分钟后再试")
            time.sleep(60*10)  #如果一下子那个api没有反应的话，那就这样操作咯，用进程把，多个cpu哦
            return self.getOneDayNewUrl(date)  #采用递归的方式来处理，，


# -----------------------------------------------------下面开始是新的提取出页面的url的-----------------------------------

    def returnThemeCode(self,theme):  #这个是有用的，用来组合主题代码url的
        ent_Theme = 1537876288634
        sport_Theme = 1537877689177
        finance_Theme = 1537878365483
        tech_Theme = 1537879684280
        auto_Theme = 1537887032223
        house_Theme = 1537887128904
        news_Theme = 1537874915062
        if theme == 'news':
            return news_Theme
        if theme == 'ent':
            return ent_Theme
        if theme == 'sports':
            return sport_Theme
        if theme == 'tech':
            return tech_Theme
        if theme == 'auto':
            return auto_Theme
        if theme == 'house':
            return house_Theme
        if theme == 'finance':
            return finance_Theme


    def getThemeUrl(self,theme, today, pageNumber):
        rawUrl = "http://roll.news.qq.com/interface/cpcroll.php"
        rawReferer = '.qq.com/articleList/rolls/'  # 'http://news   前面还有这个东西
        my_headers = [
            'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
            'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
            'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']
        headers = {"User-Agent": random.choice(my_headers), 'Referer': 'http://' + theme + rawReferer}  # 默认值
        rawUrl = rawUrl + "?callback=rollback&mode=1&cata=&_=" + str(self.returnThemeCode(theme)) + "&site=" + theme + "&page=" + str(pageNumber) + "&date=" + today
        try:
            rawhtml = requests.get(rawUrl, headers=headers, allow_redirects=False,
                                   timeout=30)  # 一般提取文本的话，那就用text，如果是文件就content
            rawhtml.encoding = chardet.detect(rawhtml.content)['encoding']
            # print(rawhtml.url)
            print("状态码" + str(rawhtml.status_code))
            if rawhtml.status_code == 504:
                print(504)
                return
            print("页面的读取结果为")
            # print(rawhtml.text)
            if rawhtml.text.find('rollback') == 0:
                jsonString = rawhtml.text.split("rollback")[1]  # 把js提取出来就可以了
            else:
                jsonString = rawhtml.text
            print(jsonString)
            dicData = eval(jsonString)
            print(type(jsonString))
            print(jsonString)
            # print(dicData['data']['article_info'])
            print(len(dicData['data']['article_info']))
            if dicData['data'] == "":
                print("超过了最大页数了，跳出了就可以了")
                return
            urllist = []
            for one in dicData['data']['article_info']:
                # print(one['url'])
                print(one['url'].replace("\\", "/"))  # 还需要检查一下这个和之前的那种野蛮是不是一样的
                urllist.append(one['url'].replace("\\", "/"))
            return urllist
        except Exception as e:
            # print(e)
            return []

    def pageUrlMain(self,date): # 写入url进入数据库，并且写入分类
        # url    ="http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=news&mode=1&cata=&date=2018-09-25&page=1&_=1537850539512"

        urlNew = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=news&mode=1&cata=&date=2018-09-25&page=1&_=1537874915062"

        urlEnt = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=ent&mode=1&cata=&date=2018-09-25&page=1&_=1537876288634"  # referer = http://ent.qq.com/articleList/rolls/

        urlSport = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=sports&mode=1&cata=&date=2018-09-25&page=1&_=1537877689177"  # r这个好像而是动态加载出来的，真是的

        urlFinance = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=finance&mode=1&cata=&date=2018-09-25&page=1&_=1537878365483"

        urlTech = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=tech&mode=1&cata=&date=2018-09-25&page=2&_=1537879684280"

        urlAuto = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=auto&mode=1&cata=&date=2018-09-25&page=1&_=1537887032223"

        urlHouse = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=house&mode=1&cata=&date=2018-09-25&page=1&_=1537887128904"

        resultUrlDic = {}     #写入数据库使用这个
        tempList = []
        themeList = ['news', 'ent', 'tech', 'auto', 'house', 'finance', 'sports']   #一共有7个主题，其实不止这7个的


        for theme in themeList:
            print("第一个主题是")
            tempDList = []
            for i in range(1, 12):  # 一般是10页就很多的了。10页以内
                print("第" + str(i) + "页")
                responseList = self.getThemeUrl(theme, date, i)
                if len(responseList) == 0:
                    print("最大页数为" + str(i - 1) + "页")
                    break
                else:
                    tempList = tempList+responseList
                    tempDList +=responseList
            resultUrlDic[theme]=tempDList
            print(resultUrlDic)
        tempList = set(tempList)
        count = 0
        print("列表的url数量有："+str(len(tempList)))
        for key in resultUrlDic:
            count+=len(resultUrlDic[key])
        print("url总共有"+ str(count))

        print("这个是PageUrls内的提取到的url")
        pprint(resultUrlDic)
        print(len(resultUrlDic))

        print("这个开始是list类型的结果")
        print(tempList)

        self.dbhelper.saveDicToMysql(resultUrlDic,date,"tengxun")   #参数，字典结果集，时间，分类
        return tempList   #直接这儿去重后



#提取到的url先存到数据库里面去
if __name__ == "__main__":
    newUrl = DateUrl()
    print(newUrl.pageUrlMain("2019-03-17"))   #直接测试今天的量，因为测试的时候写成这样了。
    pass
