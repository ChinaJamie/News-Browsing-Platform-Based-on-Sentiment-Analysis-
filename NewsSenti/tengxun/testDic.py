# -*- coding: utf-8 -*-
import requests
import re
import json
import codecs
import os
import datetime

# 爬取新闻评论id为commentid，日期为date，新闻id为newsID的所有评论
def crawlcomment(commentid,date,newsID):
    url1='http://coral.qq.com/article/'+commentid+'/comment/v2?callback=_articlecommentv2&orinum=30&oriorder=t&pageflag=1&cursor='
    url2='&orirepnum=10&_=1522383466213'
    # 一定要加头要不然无法访问
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }

    dir=os.getcwd();
    comments_file_path=dir+'/docs/tencent/' + date+'/'+newsID+'_comments.json'

    news_file = codecs.open(comments_file_path, 'a', 'utf-8')
    response=getHTMLText(url1+'0'+url2,headers)

    while 1:
        g=re.search("_articlecommentv2\\((.+)\\)", response)
        out=json.loads(g.group(1))
        if not out["data"]["last"]:
            news_file.close()
            print("finish！")
            break;
        for i in out["data"]["oriCommList"]:
            time=str(datetime.datetime.fromtimestamp(int(i["time"])))#将unix时间戳转化为正常时间
            line = json.dumps(time+':'+i["content"],ensure_ascii=False)+'\n'
            news_file.write(line)
            print(i["content"])

        url=url1+out["data"]["last"]+url2#得到下一个评论页面链接
        print(url)
        response=getHTMLText(url,headers)

def getHTMLText(url,headers):
    try:
        r=requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return "产生异常 "