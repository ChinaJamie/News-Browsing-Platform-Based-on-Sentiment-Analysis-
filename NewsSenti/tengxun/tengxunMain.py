#coding=utf-8
#
'''
1.这儿是整合起来跑的，首先是数据库提取出要爬取内容的网页的链接
2.然后就是把使用pageContent 这个东西提取出来，并且自动本地化图片
3.然后就是把文章的段落随机组合成不少于800字的一个文章


#只是用来填充基础库用的
'''
import time

# from pageContent import pageContent
from newsCrawl.tengxun.pageContent import pageContent

if __name__ == "__main__":
    datahelper = DB()

    URLandDate = datahelper.getLimitUrl(0,1000,"tengxun")  #到时候可以设定好一个确切的整数，然后再开始遍历划分
    print(URLandDate)  #这儿取出来后，之后又和一般的那个爬虫是一样的了，设置一定的频率
    page = pageContent()
    for url,date in URLandDate:
        print(url)
        title,Hcontent,Tcontent,Acontent = page.getPageContent(url)
        print(Acontent)
        if(title!="腾讯没找到标题"):
            datahelper.updateContent(url,title,Hcontent,Tcontent,Acontent)  #包括一整排你的完整文章还有拆分开来的两部分头尾
        # datahelper.i

        # time.sleep(0.5)
    print("写入100内容完毕")


    #这个之后才可以随机的组装出数据
    # mixP

