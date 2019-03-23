## -*- coding: utf-8 -*-


#2018/9/8 修改成使用连接池的方式来进行数据库的链接
import random
import traceback
from datetime import date, timedelta

import emoji
import pymysql as pymysql
import time
from DBUtils.PooledDB import PooledDB




#提取返回数据的全部变成了返回字典类型
#这个是连接数据库的东西,这次使用数据库连接池把，使用连接池可以避免反复的重新创建新连接
#todo 这儿有一个问题关于插入失败的，1.是插入的字符串中文gbk编码的，需要转换，2.就是可能会遇到emoji表情嘛？有可能的
#todo 还有一个问题就是就是api （腾讯）字典key突然读取为空，没有这个key出现错误，什么鬼，健壮性要搞一下
#todo 执行sql的时候就需要try catch 不然就崩溃了
from config import mysqlInfo
from senti_dict import Senti_Text


class DB:  #一个对象一个数据库连

    __pool = None   #这个也是静态的属性

    def __init__(self):
        # 构造函数，创建数据库连接、游标，默认创建一个对象就获得一个连接，用完后就关闭就可以了
        self.coon = DB.getmysqlconn()  #这个是默认创建出来的东西
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod   #这个是静态的方法可以直接调用的
    def getmysqlconn():  #从连接池里面获得一个连接
        if DB.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=2, maxcached=20, host=mysqlInfo['host'],
                                  user=mysqlInfo['user'], passwd=mysqlInfo['passwd'], db=mysqlInfo['db'],
                                  port=mysqlInfo['port'], charset=mysqlInfo['charset'])
            # print(__pool)

        return __pool.connection()

        # 释放资源
    def dispose(self): #这儿只能断默认初始化的那个连接
        self.coon.close()
        self.cur.close()





    # def refreshConnection(self):  #晚点再改成连接池的形式
    #     self.db = pymysql.connect(host="localhost", user="root", charset='utf8', password="Z123321#", db="caiji",port=3306)
    #     #再设置一次

    def __query__(self,sql):  #自定义查询,返回字典的类型
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)  #这儿这个选项是设置返回结果为字典的类型，如果默认的话，那就是列表i
        cur.execute(sql)
        URLs = cur.fetchall()   #返回数据的列表，可以设置返回的是字典
        cur.close()
        coon.close()
        return URLs

    def ifExists(self,webTitle):
        coon = DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "SELECT * FROM tengxun WHERE title='%s'and urlState='True';"
        #因为这儿没有加上try，catch，所以出问题
        try:
            cur.execute(sql%(webTitle))
        except Exception as e:
            print(e)
            print("函数ifExists出问题了，你检查一下")
            print(sql%(webTitle))
        rowNumber = cur.rowcount
        if rowNumber>0:
            return True
        else:
            return False




    def __randomP__(self):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # sql = "insert into tengxun (Acontent) values( '" + content + "') where url=%s;"% url
        sql = "SELECT * FROM simpleP WHERE id>= ((SELECT MAX(id) FROM simpleP )-(SELECT MIN(id) FROM simpleP )) * RAND() + (SELECT MIN(id) FROM simpleP ) LIMIT 10;"
        cur.execute(sql)
        URLs = cur.fetchall()
        allHtml = ""
        # print(URLs)
        for row in URLs:
            # print(row)
            # print(type(row))
            # print(type(row['oneP']))
            
            allHtml=allHtml+row['oneP']
        if (len(allHtml)<800):
            allHtml=allHtml+self.__randomP__()  #递归算法
        # print('共查找出', cur.rowcount, '条数据')
        # self.__close__()
        cur.close()
        coon.close()
        return allHtml

    def updateMixState(self,id):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        # print(url)  之前是这儿的语句错了嘛，还以为哪儿的问题
        # print(id)
        sql = "update tengxun set hadmix='True' where id = %d;" % int(id)   #就只是更新一下相应的url的状态就可以了
        # print(sql)
        try:  #像这样容易出问题的
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("更新hadmix失败，请检查updateMixState")
            print(e)
            coon.rollback()

        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            cur.close()
            coon.close()
        
    def updateState(self,id):   #混合过一个就用那个urlstate这个字段，这样不就不会重复了嘛，随机的是段落不是标题和开头
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # print(url)  之前是这儿的语句错了嘛，还以为哪儿的问题
        # print(id)
        sql = "update tengxun set urlState='True' where id = %d;" % int(id)   #就只是更新一下相应的url的状态就可以了
        # print(sql)
        try:  #像这样容易出问题的
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("更新失败，请检查updateState")
            print(e)
            coon.rollback()

        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            cur.close()
            coon.close()
        
        

    def __randomHandT__(self):   #这个是随机抽出一个标题，和开头可结
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        #lists = self.__query__("select * from tengxun where title!='' ;")
        #maxId = len(lists)
        #number = random.randint(1,maxId)
        # sql = "insert into tengxun (Acontent) values( '" + content + "') where url=%s;"% url
        #sql ="SELECT * FROM tengxun WHERE title!=''and id>= ((SELECT MAX(id) FROM tengxun where title!='' )-(SELECT MIN(id) FROM tengxun where title!='' )) * RAND() + (SELECT MIN(id) FROM tengxun where title!=''  )   LIMIT %d;" % 1
        #sql1 = "select * from tengxun where title!='' and id <=%d limit 1" % number
        #urlState 是有没有用过这个新闻的标题的东西来的，然后还要有开头段落
        sql1= "select * from tengxun  where title!='' and hadmix = 'False'  limit 0,1;"
        #这儿出了点问题，就是这个检测的这个其实是用来验证有没有生成mix

        cur.execute(sql1)
        lists = cur.fetchall()
        # print(lists[0])
        # print("查找到的结果有那么多哈")
        # print(cur.rowcount)
        if(cur.rowcount==1):
            # print("剩下的结果是1")
            # print(type(cur.fetchall()[0]))
            # print(lists[0]['title'])
            onePart = lists[0]['title'] #选出里面的一个元素

            # print(type(onePart[0]))
            # print(onePart)


            self.updateState(lists[0]['id'])  #更新这个状态的东西就可以了，所以才需要这个东西,这儿应该传的是id，list ，dic嵌套
            # print(onePart)

            # print(onePart[2],onePart[4],onePart[6])
            title,header,tail,id =lists[0]['title'],lists[0]['Hcontent'],lists[0]['Tcontent'],lists[0]['id']

            if(title==None):
                title =self.__randomHandT__()  #继续递归
            cur.close()
            coon.close()
            return title,header,tail,id
        else:
            cur.close()
            coon.close()
            return "","","",0



        # return db,cur #返回两个东西来接应它

    def saveListToMysql(self,urlList ,date,fromWhere):               #逐条调用把list写入数据库而已拉
        for url in urlList:
            # if self.checkWhetherInDB(url):   #如果没有这条数据，那么就写入，并且提取出页面
            self.insertTenxun(url,date,fromWhere)          #去重，不重复写入数据库
            # else:
            #     urlList.remove(url)          #删掉这个url元素，不用插入的话
        return urlList





    def insertTenxun(self,url,date,fromWhere): #这个是把网址先存到里面去url，这儿的意思是插入tengxun那个表
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        sql = "insert into tengxun (url,newdate,fromWhere) values( '" + url + "','" + date + "','"+fromWhere+"');"
        # print(sql)
        try:
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("数据表中已经有此url，跳过插入此")
            print(sql)
            print(e)
            coon.rollback()
        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            cur.close()
            coon.close()

            # self.__close__()

    def updateContent(self,url,title,Hcontent,Tcontent,Acontent):  #这三个都看成一部分，一次性的存进去好吧
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        Hcontent = str(Hcontent)
        Tcontent = str(Tcontent)
        Acontent = str(Acontent) #beautiful标签转制一下不然就是tag

        # print(url)  之前是这儿的语句错了嘛，还以为哪儿的问题
        sql = "update tengxun set  title='"+title+"' , Acontent = '" + Acontent + "' ,Hcontent = '"+Hcontent+"' , Tcontent = '"+Tcontent+"' ,hadmix='False',urlState="+"'True'"+"  where url='%s';"% url   #能填成功那就说明可以，可以用这个新的来合成新的混合文章
        # print(sql)
        flag=False  #返回的东
        try:
            cur.execute(sql)
            # 提交
            coon.commit()
            flag=True
        except Exception as e:
            # 错误回滚
            print("更新失败，请检查updateContent,标题或者 url已经存在了拉")
            print(sql)
            '''   上次的错误提示
            更新失败，请检查updateContent
            update tengxun set  title='习近平对政法工作作出重要指示' , Acontent = '' ,Hcontent = '视频：习近平对政法工作作出重要指示，时长约1分43秒' , Tcontent = '<p><iframe frameborder="0" src="https://v.qq.com/txp/iframe/player.html?vid=h0025szp8ya" allowFullScreen="true"></iframe></p>'   where url='http://news.qq.com/a/20180122/022335.htm';
            http://news.qq.com/a/20180122/022335.htm
            (1062, "Duplicate entry '习近平对政法工作作出重要指示' for key 'title'")
            '''
            print(url)  #url不同，但是呢，同样标题的新闻已经有了，获取，其实url也相同，那就把这个id删掉好了
            print(e)
            coon.rollback()
        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            # self.__close__()
            cur.close()
            coon.close()
            return flag   #更新成功，返回正


    def insertWangyi(self,url):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样
        sql = "insert into tengxun (url,newdate,fromWhere) values( '" + url + "','" + now_date + "','wangyi');"
        # print(sql)
        try:
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("插入wangyi出现问题")
            print(e)
            coon.rollback()
        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            cur.close()
            coon.close()



    def getLimitUrl(self,start,end,fromWhere):   #提取url然后进行提取段落处理
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # sql = "insert into tengxun (Acontent) values( '" + content + "') where url=%s;"% url
        sql = "SELECT url ,newdate FROM tengxun where fromWhere='"+fromWhere+"' and  isNull(title) LIMIT %d,%d;" % ( start ,end )  #只选出空的
        # print(sql)
        cur.execute(sql)
        URLs = cur.fetchall()
        for row in URLs:
            # print(row)
            print("url:%s  日期：%s" % ( row['url'],row['newdate']))
        print('共查找出', cur.rowcount, '条数据')
        # self.__close__()
        cur.close()
        coon.close()

        return URLs

    def checkWhetherInDB(self,url):
        # url = "http://news.ifeng.com/a/20180820/59909441_0.shtml"
        # url = "dadafdads"
        sql = "select * from tengxun where url='%s'"
        result = self.__query__(sql % url)
        if len(result)==0: #说明没有数据
            return True  # 可以插入：
        else:
            return False  #不用再插入进去了

        # return False

    def insertSimpleP(self,Pcontent):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        Pcontent = str(Pcontent)
        sql = "insert into simpleP (oneP,number) value( '" + Pcontent + "'," + str(len(Pcontent)) + ");"
        # print(sql)
        try:
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("插入simpleP出现问题")
            print(sql)
            print(e)
            coon.rollback()
        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            cur.close()
            coon.close()


    def insertMixP(self,title,mixP):


        if(title !="" and mixP !=""):
            coon = DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
            cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

            sql = "insert into c_title  ( title ,content,yuan_id,object_id,caiji_id ) values ( '" + title + "','" + mixP + "',1,0,1 );"
            # print(sql)
            try:
                cur.execute(sql)
                # 提交
                coon.commit()
            except Exception as e:
                # 错误回滚
                print("插入c_title出现问题")
                print(sql)
                print(e)
                coon.rollback()
            finally:
                # print("插入成功")
                coon.commit() #提交这个事务
                # self.__close__()
                cur.close()
                coon.close()
        else:
            print("插入的为空，跳过插入")
            pass

    def deleteUrl(self,url):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        sql = "delete from tengxun where url ='%s';" % url
        try:
            # 执行SQL语句
            cur.execute(sql)
            # 提交修改
            coon.commit()
            print("删除成功哈 "+url)
        except Exception as e:
            print(e)
            # 发生错误时回滚
            print("删除失败，查看deleteUrl")
            print(sql)
            coon.rollback()
        # 关闭连接
        finally:
            coon.commit()
            cur.close()
            coon.close()


    def quchong(self):  #这个是用来去重的，
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql ='DELETE FROM simpleP WHERE id NOT IN(SELECT * FROM(SELECT id FROM simpleP GROUP BY oneP )AS b);'
        # print(sql)
        try:
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("数据库取出url相同的重复，title相同的重复自动跳过")
            print(sql)
            print(e)
            coon.rollback()
        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            # self.__close__()
            cur.close()
            coon.close()

    def testDB(self):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # self.db.close()
        sql = "select * from tengxun ;"
        cur.execute(sql)
        URLs = cur.fetchall()
        for row in URLs:
            print("url:%s  日期：%s" % (row[0], row[1]))
        print('共查找出', cur.rowcount, '条数据')
        # self.__close__()
        cur.close()
        coon.close()
        return URLs

    def updateSimpleP(self,id,oneP):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "update simpleP set oneP ='%s' where  id =%d" % (oneP,id)
        try:
            cur.execute(sql)
            coon.commit()
        except Exception as e:
            # 错误回滚
            print(e)
            coon.rollback()
        finally:
            coon.commit()  # 提交这个事务
            cur.close()
            coon.close()

    def updateHTMA(self,id,h,t,A):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        # print(url)  之前是这儿的语句错了嘛，还以为哪儿的问题
        sql = "update tengxun set Hcontent ='%s' ,Tcontent='%s',Acontent='%s' where  id=%d ;" % (h,t,A,id)
        try:
            cur.execute(sql)
            coon.commit()
        except Exception as e:
            # 错误回滚
            print(e)
            coon.rollback()
        finally:
            coon.commit()  # 提交这个事务
            cur.close()
            coon.close()

    def updateCtitle(self,id,content):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        # print(url)  之前是这儿的语句错了嘛，还以为哪儿的问题
        sql = "update c_title set content ='%s'  where  id=%d ;" % (content,id)
        try:
            cur.execute(sql)
            coon.commit()
        except Exception as e:
            # 错误回滚
            print(e)
            coon.rollback()
        finally:
            coon.commit()  # 提交这个事务
            cur.close()
            coon.close()



    #这个几个是当时临时修改src用的
    def changeSrc(self):   #自动遍历这个东西，记得带上检查是否断开的东西,这个已经处理后就不用再管了
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "select * from tengxun  where title!='' and Hcontent!='' ;" #遍历这里面整个的数据库的东西

        print(sql)
        cur.execute(sql)
        URLs = cur.fetchall()
        for row in URLs:  #字段是 id - oneP  - 字数，就用第一个和第二个就可以了
            id =row[0]
            h = row[4]
            t = row[6]
            A = row[7]
            if(h.find('images/')!=-1):  #有这种的一定是路径来的
                print("找到了images需要修改")
                # src = "images/newsapp_bt_0_2636735713_641.jpg"
                h = h.replace('images/','''/images/''')
            if (t.find('images/') != -1):  # 有这种的一定是路径来的
                print("找到了images需要修改")
                    # src = "images/newsapp_bt_0_2636735713_641.jpg"
                t = t.replace('images/', '''/images/''')
                # self.updateHTMA(id, h, t, m, A)
            if (A.find('images/') != -1):  # 有这种的一定是路径来的
                print("找到了images需要修改")
                # src = "images/newsapp_bt_0_2636735713_641.jpg"
                A = A.replace('images/', '''/images/''')

            self.updateHTMA(id, h, t, A)
            print("修改后为： "+h,t,A)
        cur.close()
        coon.close()

        def changeSrc(self):  # 自动遍历这个东西，记得带上检查是否断开的东西
            coon = DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
            cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
            sql = "select * from tengxun  where title!='' and Hcontent!='' ;"  # 遍历这里面整个的数据库的东西

            print(sql)
            cur.execute(sql)
            URLs = cur.fetchall()
            for row in URLs:  # 字段是 id - oneP  - 字数，就用第一个和第二个就可以了
                id = row[0]
                h = row[4]
                t = row[6]
                A = row[7]
                if (h.find('images/') != -1):  # 有这种的一定是路径来的
                    print("找到了images需要修改")
                    # src = "images/newsapp_bt_0_2636735713_641.jpg"
                    h = h.replace('images/', '''/images/''')
                if (t.find('images/') != -1):  # 有这种的一定是路径来的
                    print("找到了images需要修改")
                    # src = "images/newsapp_bt_0_2636735713_641.jpg"
                    t = t.replace('images/', '''/images/''')
                    # self.updateHTMA(id, h, t, m, A)
                if (A.find('images/') != -1):  # 有这种的一定是路径来的
                    print("找到了images需要修改")
                    # src = "images/newsapp_bt_0_2636735713_641.jpg"
                    A = A.replace('images/', '''/images/''')

                self.updateHTMA(id, h, t, A)
                print("修改后为： " + h, t, A)
            cur.close()
            coon.close()


    def changCaiji(self):  # 自动遍历这个东西，记得带上检查是否断开的东西
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "select * from c_title ;"  # 遍历这里面整个的数据库的东西

        # print(sql)
        cur.execute(sql)
        URLs = cur.fetchall()
        for row in URLs:  # 字段是 id - oneP  - 字数，就用第一个和第二个就可以了
            id = row[0]
            content = row[2]
            # t = row[6]
            # A = row[7]
            if (content.find('images/') != -1):  # 有这种的一定是路径来的
                print("找到了images需要修改")
                # src = "images/newsapp_bt_0_2636735713_641.jpg"
                content = content.replace('images/', '''/images/''')

            self.updateCtitle(id,content)
            print("修改后为： " + content)
        cur.close()
        coon.close()



        print('共查找出', cur.rowcount, '条数据')
        print("数据库中的数据已经修改完毕，谢谢你的使用")
        # self.__close__()
        # return URLs

    def getAllTitle(self):  #查询这次爬取总共爬了多少条数据
        allTogether = ""
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # self.db.close()
        now_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期
        print(now_date)
        sql = "select * from tengxun where newdate='%s';"%now_date   #使用sql拼接是很不安全的啊。
        cur.execute(sql)
        URLs = cur.fetchall()
        for row in URLs:
            # print(row)
            print(row['title'])
            allTogether+=row['title']
            # print("url:%s  日期：%s" % (row[0], row[1]))
        print('共查找出', cur.rowcount, '条数据')
        # self.__close__()
        cur.close()
        coon.close()
        return allTogether



    #------------------------------------迭代时间2019-03-16 14:48 新增之后整理的函数--------------------------------------
    def saveDicToMysql(self, dictList, date, fromWhere):  #[{}]的嵌套的结构，这个是存如tengxun表中的，未整理前
        print("进入了saveDicToMysql")
        # print(dictList)
        for category in dictList:
            # print(category)
            for url in dictList[category]:   #每次插入一条url
                self.insertTengxunTheme(url,date,fromWhere,category)   #四个参数都有了这样。

        print("finish!good!")




    def insertTengxunTheme(self, url, date, fromWhere ,category):  #[{}]的嵌套的结构
        coon = DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        sql = "insert into tengxun (url,newdate,fromWhere,category) values( '" + url + "','" + date + "','" + fromWhere + "','" + category + "');"
        print(sql)
        try:
            cur.execute(sql)
                # 提交
            coon.commit()

        except Exception as e:
                # 错误回滚
            print("数据表中已经有此url，跳过插入此")
            print(sql)
            print(e)
            coon.rollback()
        finally:
                # print("插入成功")
            coon.commit()  # 提交这个事务
            cur.close()
            coon.close()

    def classifyDB(self): #todo 这个是根据传过来的数据分别进行分类，数据库的操作都写这儿来比较不容易乱。
        resultDic = self.__query__(  #todo 测试部分
            "select id,url,title,urlState,Hcontent,Mcontent,Tcontent,Acontent,newdate,fromWhere from tengxun where urlState='True' and hadmix='False'")
        print("开始分类整理")
        for rowDic in resultDic:
            # 插入分类新闻主表的sql
            sql = ""
            sqlHead = "insert into newssentimentanalysis_"
            sqlTail = "news (url,Title,UrlState,Hcontent,Mcontent,Tcontent,Acontent,Date,fromWhere) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            # 插入正文得分的sql
            sql2 = ""
            sql2Tail = "analysis_news(Pos_Score,Neg_score,Sentiment,News_id_id) values (%s,%s,%s,last_insert_id())"  # 这个是sql的

            # 这句就是更新tengxun表中的数据,用id
            updateSql = "update tengxun SET hadmix='True' where id='%s' "

            if rowDic['url'].find('auto') != -1:  # 找到这个就是汽车,中间是表名
                sql = sqlHead + "car" + sqlTail
                sql2 = sqlHead + "car" + sql2Tail
                pass
            if rowDic['url'].find('tech') != -1:  # 找到这个就是科技
                sql = sqlHead + "technology" + sqlTail
                sql2 = sqlHead + "technology" + sql2Tail

                pass
            if rowDic['url'].find('news') != -1:  # 找到这个就是默认新闻
                sql = sqlHead + "home" + sqlTail
                sql2 = sqlHead + "home" + sql2Tail

                pass
            if rowDic['url'].find('ent') != -1:  # 找到这个就是娱乐
                sql = sqlHead + "entertainment" + sqlTail
                sql2 = sqlHead + "entertainment" + sql2Tail

                pass
            if rowDic['url'].find('house') != -1:  # 找到这个就是房产
                sql = sqlHead + "house" + sqlTail
                sql2 = sqlHead + "house" + sql2Tail

                pass
            if rowDic['url'].find('finance') != -1:  # 找到这个就是经济
                sql = sqlHead + "finance" + sqlTail
                sql2 = sqlHead + "finance" + sql2Tail

                pass
            if rowDic['url'].find('sports') != -1:  # 找到这个就是运动
                sql = sqlHead + "sports" + sqlTail
                sql2 = sqlHead + "sports" + sql2Tail

                pass
            else:
                pass  # 未能分类,也放到默认的那儿去吗。
            
            #--------------------------------获取得分----------------------------------
            print("原文，我并没有打开url啊！")
            # print(rowDic['Tcontent'])
            print(type(rowDic['Tcontent']))
            print(len(rowDic['Tcontent']))
            print(rowDic)
            pos_score, neg_score, SentiResult = Senti_Text(rowDic['Tcontent'])  #这个是纯文本部分
            # print((pos_score.item()))

            # ---------------------------这边开始数据库插入相关操作-----------------------------

            coon = DB.getmysqlconn()                    # 每次都默认获得一个新连接来进行相关的操作
            cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

            try:                       #三个一起操作，很多麻烦事情的。
                cur.execute(sql,(rowDic['url'],rowDic['title'],True,rowDic['Hcontent'],'未提取',rowDic['Tcontent'],rowDic['Acontent'],rowDic['newdate'],rowDic['fromWhere']))  #插入指定的表（分类）

                print("插入成功才用得上这个的把。")#无法提取到这个的。在写一次查询把。
                # print(cur.lastrowid())      #上一个插入的id是，还真是有，那就直接返回过来就可以了
                # print(type(cur.lastrowid()))   #上一个插入的id是，还真是有，那就直接返回过来就可以了

                cur.execute(sql2,(float('%.3f' % pos_score.item()),float('%.3f' %neg_score.item()),SentiResult))  #插入评分   todo获得评分
                cur.execute(updateSql,(rowDic['id']))  # 更新tengxun hadmix,这个是可以工作的啊
                # 提交
                coon.commit()

            except Exception as e:
                # 错误回滚
                print("事务回滚，跳过插入")
                # print(rowDic['id'])
                print(sql%(rowDic['url'],rowDic['title'],True,rowDic['Hcontent'],'未使用',rowDic['Tcontent'],rowDic['Acontent'],rowDic['newdate'],rowDic['fromWhere']))
                print(e)
                coon.rollback()
                traceback.print_exc()

            finally:
                # print("插入成功")
                coon.commit()  # 提交这个事务
                cur.close()
                coon.close()
        print("今天的量分完了")

    def classifyDBComment(self,url,id,comment):  # 评论的数据库分类插入,传入新闻的url和id,commentDic <聚合的dic>
        print("开始分类整理")  #
        # print(comment['id'])
        sql = ""  #评论正文插入   m  nbvcbv
        sqlHead = "insert into newssentimentanalysis_"
        sqlTail = "comment  (NikeName,Comment,Date,News_id_id) values (%s,%s,%s,%s)"

        # 插入评论得分的sql
        sql2 = ""
        sql2Tail = "analysis_comment(Pos_Score,Neg_score,Sentiment,Comment_id_id) values (%s,%s,%s,last_insert_id())"  # 这个我也知道

            # 这句就是更新新闻表中的数据,用id  newssentimentanalysis_carcomment
        sqlNews = ""
        sqlNewsHead = "update newssentimentanalysis_"
        sqlNewsTail = "news SET Mcontent='已提取' where News_id=%s"  #id是数字

        # 插入正文得

        # updateSql = "update tengxun SET hadmix='True' where id='%s' "  #Mcontent，这个字段用来“未提取”-》“已提取

        if url.find('auto') != -1:  # 找到这个就是汽车,中间是表名
            sql = sqlHead + "car" + sqlTail
            sql2 = sqlHead + "car" + sql2Tail
            sqlNews =sqlNewsHead+ "car"+ sqlNewsTail
            pass
        if url.find('tech') != -1:  # 找到这个就是科技
            sql = sqlHead + "technology" + sqlTail
            sql2 = sqlHead + "technology" + sql2Tail
            sqlNews =sqlNewsHead+ "technology"+ sqlNewsTail

        if url.find('news') != -1:  # 找到这个就是默认新闻
            sql = sqlHead + "home" + sqlTail
            sql2 = sqlHead + "home" + sql2Tail
            sqlNews =sqlNewsHead+ "home"+ sqlNewsTail


        if url.find('ent') != -1:  # 找到这个就是娱乐
            sql = sqlHead + "entertainment" + sqlTail
            sql2 = sqlHead + "entertainment" + sql2Tail
            sqlNews =sqlNewsHead+ "entertainment"+ sqlNewsTail

        if url.find('house') != -1:  # 找到这个就是房产
            sql = sqlHead + "house" + sqlTail
            sql2 = sqlHead + "house" + sql2Tail
            sqlNews =sqlNewsHead+ "house"+ sqlNewsTail

        if url.find('finance') != -1:  # 找到这个就是经济
            sql = sqlHead + "finance" + sqlTail
            sql2 = sqlHead + "finance" + sql2Tail
            sqlNews =sqlNewsHead+ "finance"+ sqlNewsTail

        if url.find('sports') != -1:  # 找到这个就是运动
            sql = sqlHead + "sports" + sqlTail
            sql2 = sqlHead + "sports" + sql2Tail
            sqlNews =sqlNewsHead+ "sports"+ sqlNewsTail

        else:
            pass  # 未能分类,也放到默认的那儿去吗。

            # --------------------------------获取得分----------------------------------
        # print(type(comment['id']))
        print(comment['content'])
        print(emoji.demojize(comment['userinfo']['nick']))

        print(url,str(id))
        pos_score, neg_score, SentiResult = Senti_Text(comment['content'])  # 这个是纯文本部分
        if SentiResult.find("[")!=-1:
            SentiResult = SentiResult.replact("[","")
        if SentiResult.find("]")!=-1:
            SentiResult = SentiResult.replact("]","")
        print(SentiResult)
        # 中立的情况好像是返回直接是0
        print(pos_score)
            # ---------------------------这边开始数据库插入相关操作-----------------------------
        coon = DB.getmysqlconn()                                                          # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            cur.execute(sql, (
             comment['userinfo']['nick'], comment['content'],comment['time'], id)) # 插入指定的表（分类）
            if pos_score == 0:  #等于0 就直接输入进去
                pass
            else :
                pos_score = pos_score.item()
                neg_score = neg_score.item()

            cur.execute(sql2, (
            float('%.3f' % pos_score), float('%.3f' % neg_score), SentiResult))  # 插入评分   todo获得评分
            # print(sqlNews % int(id))
            id = str(id)

            cur.execute(sqlNews, (id))                                                   # 更新新闻的 Mcontent,这个是可以工作的啊

            coon.commit()
        except Exception as e:
                # 错误回滚
            print("事务回滚，跳过插入")
                # print(rowDic['id'])
            print(sql, (
            comment['userinfo']['nick'], comment['content'],comment['time'], id))

            print(id)
            print(type(id))
            print(sqlNews % (id))


            print(e)
            coon.rollback()
            traceback.print_exc()
        finally:
            coon.commit()  # 提交这个事务
            cur.close()
            coon.close()
            print("这条新闻的评论写入完毕")

    def findCommentByUrl (self,url): #输入url然后返回新闻,可能会返回多个怎么办
        resultIdDic = self.__query__("select id from tengxun where url='%s'"%(url))  #按字典返回这个结果的id
        # print(resultIdDic[0])
        if resultIdDic==None:  #没找到就返回空
            return "没有找到"
        if len(resultIdDic)==1:
            print(len(resultIdDic))
            return resultIdDic[0]['id']   #返回id
        else :
            return
        # if resultIdDic!None and len(resultIdDic)=1:  #多条重复的url




if __name__ == "__main__":  #下面都是用来测试用的。
    chak = DB()
    # chak.getAllTitle()
    # chak.saveDicToMysql(testDic,"2019-03-18","tengxun")
    # chak.insertTengxunTheme("www","2018-232","test","auto")  #todo 爬完再执行去重。
    # __query__

    chak.classifyDB()         #测试分类的。
    url = "http:////news.qq.com//a//20190317//004665.htm"
    # print(chak.findCommentByUrl(url))  #没返回值，所以输出为空

    print("DB finish!")




