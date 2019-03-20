#这个是用来分类整理进入django的数据库的。
# newssentimentanalysis_homenews   这个是示范的名字，分发到不同的表里面就可以了
from newsCrawl.tengxun.DBcontrol import DB

chak = DB()
# chak.getAllTitle()
# chak.saveDicToMysql(testDic,"2019-03-18","tengxun")
# chak.insertTengxunTheme("www", "2018-232", "test", "auto")  # todo 爬完再执行去重。
resultDic = chak.__query__("select url,title,urlState,Hcontent,Mcontent,Tcontent,Acontent,newdate,fromWhere from tengxun where urlState='True'")
print(resultDic)
print(len(resultDic))
#这次我并没有更新他们，更新他们之前是在everyday那儿进行处理的，把信息和urlstarte一起更新进去
print("开始分类整理")
for rowDic in resultDic:
    print(rowDic)  #七个分类 newssentimentanalysis_caranalysis_comment
    sql =""
    sqlHead  ="insert into newssentimentanalysis_"    #插入分类新闻主表的sql
    sqlTail = "news (url,Title,UrlState,Hcontent,Mcontent,Tcontent,Acontent,Date,fromWhere)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    sql2=""
    # sql2Head ="insert into newssentimentanalysis_"   #插入新闻正文评分表的sql
    sql2Tail ="analysis_news(Pos_Score,Neg_score,Sentiment,News_id_id)values (%s,%s,%s,%s)"  #这个是sql的
    if rowDic['url'].find('auto')!=-1:  #找到这个就是汽车,中间是表名  newssentimentanalysis_entertainmentanalysis_news
        sql =sqlHead+"car"+sqlTail
        sql2 =sqlHead+ "car"+sql2Tail
        pass
    if rowDic['url'].find('tech')!=-1:  #找到这个就是科技
        sql =sqlHead+"technology"+sqlTail
        sql2 = sqlHead+"technology"+sql2Tail

        pass
    if rowDic['url'].find('news')!=-1:  #找到这个就是默认新闻
        sql =sqlHead+"home"+sqlTail
        sql2 = sqlHead+"home"+sql2Tail

        pass
    if rowDic['url'].find('ent')!=-1:  #找到这个就是娱乐
        sql =sqlHead+"entertainment"+sqlTail
        sql2 = sqlHead+"entertainment"+sql2Tail

        pass
    if rowDic['url'].find('house')!=-1:  #找到这个就是房产
        sql =sqlHead+"house"+sqlTail
        sql2 = sqlHead+"house"+sql2Tail

        pass
    if rowDic['url'].find('finance')!=-1:  #找到这个就是经济
        sql =sqlHead+"finance"+sqlTail
        sql2 = sqlHead+"finance"+sql2Tail

        pass
    if rowDic['url'].find('sports')!=-1:  #找到这个就是运动
        sql =sqlHead+"sports"+sqlTail
        sql2 = sqlHead+"sports"+sql2Tail

        pass
    else:
        pass  #未能分类,也放到默认的那儿去吗。
    #------------------------------------------------这边开始数据库插入相关操作----------------------------------------------

    print("分完了")


print("DB finish!")
