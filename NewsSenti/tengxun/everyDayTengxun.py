#每日更新之腾讯，这里可以改成多线程的形式来进行操作
import time
from datetime import date, timedelta

# from WordCloud import Gen_WordCloud
# from Comment import CommentCrawl
# from DBcontrol import DB
# from pageContent import pageContent
# from pageUrls import DateUrl
from Comment import CommentCrawl
from DBcontrol import DB
from WordCloud import Gen_WordCloud
from pageContent import pageContent
from pageUrls import DateUrl



class EveryTengxun:
    def getEveryTengxun(self):
        dbhelper= DB()                     #处理数据库用
        pcontent = pageContent()           #处理页面详情用

        now_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期
        print("昨天的日期是"+now_date+"现在正在爬取昨天的新闻!d😀")  #应该是获得昨天才对

        #------------------------------------------------爬取昨晚的-----------------------------------------------------
        print("开始执行写入所有的url")
        dateUrl = DateUrl()  # 2018-09-27 日编辑  todo 这儿区分开来，不用通过这儿返回的，另外那儿只需要把那些urlState="False"的提取出来就可以
        dateUrl.pageUrlMain(now_date)   #获得今天的，并且写入数据库  ，所以这儿返回什么都没关系，不需要返回都可以的

        #-------------------------------------------------打开内容------------------------------------------------------
        print("开始执行读取页面")
        todayNewUrl = dbhelper.__query__("select url from tengxun where urlState='False' and fromWhere='tengxun'")
        print("读取出 "+str(len(todayNewUrl))+" 条")
        print("")

        #每100个就休息1分钟，慢是有原因的#每两百个休息2分钟好了
        count = 1
        delCount = 0
        for dic in todayNewUrl:
            url = dic['url']
            if count%200==0:
                time.sleep(60*2)
                print("休息2分钟")
            count+=1

            # 爬取的当前时间写入进去。
            title,Hcontent,Tcontent,Acontent=pcontent.getPageContentMain(url,now_date)  #这儿漏了更新到url中去  ,自动转换成xw的然后再下载
            time.sleep(1)

            if (title !="腾讯没找到标题" and title!=None and Hcontent!="" ):  #有内容的时候就更新这条数据

                # todo 这儿加上生成云图保存本地，并且把路径合并成src生成字符串合并到Acontent就可以了。
                # 生成img标签
                News_Id = url.replace("$","").replace("/","").replace(":","_").replace(".","_")

                imgTag = "<img src="+Gen_WordCloud(Newsid=News_Id,text=Acontent)+" />"  #不能使用单引号，否则会让sql语句中断开的
                print(imgTag)
                Acontent = imgTag+Acontent
                print("更新的结果有")
                print(title)
                print(Tcontent)
                print(url)
                print(Acontent)
                print("显示完毕")



                resultState = dbhelper.updateContent(url,title,Hcontent,Tcontent,Acontent)  #要删除的是更新失败的那个
                if resultState==False:  #更新成功
                    print("更新失败，正在删除这个url不同，但是标题相同的新闻")
                    print(url)
                    dbhelper.deleteUrl(url)  #删除提取失败的那些
                    print()
                else:
                    pass #更新成功什么都不干
            else:
                delCount +=1
                print("打开页面提取失败,可能是页面为404腾讯，删除这条url")   #为空的话，那么就删除这条把
                dbhelper.deleteUrl(url)  #按url把这条记录删除掉咯
        dbhelper.classifyDB()  # 执行完了后就进行分类到django的数据库

        comment = CommentCrawl()
        comment = CommentCrawl()
        comment.getCommentMain() #执行了爬取评论并且分类到django数据库
        print("共删除了  "+ str(delCount))
        print("原来有  "+str(len(todayNewUrl))+" 条")
        print("今天爬取完毕，蟹蟹使用")

if __name__=="__main__":
    everydayTengxun = EveryTengxun()
    everydayTengxun.getEveryTengxun()
    print("腾讯昨日爬取完成。")
    # quchong  DB中的去重，就是用这个。
