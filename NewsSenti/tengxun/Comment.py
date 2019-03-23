# 这个是收集评论的类
import json
import random
import time

import emoji
import requests

from DBcontrol import DB
from makebeautifulSoup import makeBS



class CommentCrawl(object):
    def __init__(self):
        self.dbHelper = DB()

    def changTimeToDate(self,dateString):
        timeStamp = dateString
        timeArray = time.localtime(timeStamp)
        print(timeArray)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        # print(otherStyleTime)
        return otherStyleTime


    def getNewsIdAndUrl(self):   #提取出新闻的id和url
        # dbHelper = DB()
        themeWord = ['car','technology','home','entertainment','house','finance','sports']  #类别新闻
        resultDic = {}
        sqlHead = "select News_id,url from newssentimentanalysis_"
        sqlTail = "news"
        # 插入
        for theme in themeWord:
            print(sqlHead+theme+sqlTail)
            resultDic[theme] = self.dbHelper.__query__(sqlHead+theme+sqlTail)# 返回
        return resultDic  #返回格式{'car':[{'id':xx,'url':xx},.....,'home'...]

    def getAwriteCommentJson(self,id,url):                                        #这个是评论专用的请求返回成字典的。
        time.sleep(1)
        cooker = makeBS()
        commentRawUrl = "http://coral.qq.com/article/"
        cmt_id = cooker.getCmt_id(url)  #去掉空格
        if cmt_id==None:
            return
        if cmt_id.find("'")!=-1:
            cmt_id = cmt_id.replace("'","")
        else :
            cmt_id = cmt_id.strip()

        # print(  cmt_id.strip()  )
        #这个用来拼接用到。
        try:
            allUrl = commentRawUrl + str(cmt_id) + "/comment/#"
            print(allUrl)
            responseDic = cooker.makeBSjson(allUrl)
            # if
            # print()
            print(responseDic)
            commentList = responseDic['data']['commentid']
            print(commentList)
            from pprint import pprint
            for comment in commentList:
                pprint(type(comment['id']))
                print(comment['id'])
                comment['content'] = emoji.demojize(comment['content'])      #过滤emoji
                comment['userinfo']['nick'] = emoji.demojize(comment['userinfo']['nick'])
                comment['time']=self.changTimeToDate(comment['time'])             #时间戳改成日期字符串
                print("新闻id "+ str(id))
                print("新闻的url是 "+ url)


                self.dbHelper.classifyDBComment(url=url,id=id,comment=comment)   #插入数据库。


                print("")
                #-----------------------这儿可以合成sql语句的话就可以执行插入的操作了。-----------------------
                # 通过url来合成插入的sql语句，DBcontrol的方法中来做这些东西
        except Exception as e:
            print("提取此条评论出错，正在跳过")
            print(e)


    def getCommentMain(self):
        resultDic = self.getNewsIdAndUrl()
        print(resultDic)
        from pprint import  pprint
        resultList = []
        count = 0
        for theme in resultDic:
            print("现在是",theme)
            for oneNews in resultDic[theme]:
                count+=1  #这个累加，然后如果是到了一定的数量那就休眠一下
                if count%100==0:  #每100条
                    time.sleep(60*2) #休息两分钟。
                print(oneNews)  #已经提取出来了
                self.getAwriteCommentJson(id=oneNews['News_id'],url=oneNews['url'])   #逐条插入，进行，这个不需要返回
                # resultList.append(oneNews)   # 添加进入
        print("finish comments crawl！")

if __name__ == '__main__':
    commentC  = CommentCrawl()
    # print(commentC.getNewsIdAndUrl())
    # print(commentC.getCommentJson("http:////sports.qq.com//a//20190315//000008.htm",55))  #测试单个

    commentC.getCommentMain()  #测试主题从url中提取，url又可以合成。


    # print(commentC.changTimeToDate(1553192258))
    # 1553192225