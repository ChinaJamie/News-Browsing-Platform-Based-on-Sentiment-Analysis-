#这个是配置文件
'''
目前有需要的设置
1.数据库的配置设置
2.定时爬取的时间
3.下载路径设置 （请设置到  项目名字/static/image  ，使用绝对路径，移动了django项目路径后请记得修改下载路径。

'''

mysqlInfo = {
    "host": '127.0.0.1',
    "user": 'root',
    "passwd": 'aptx4869',
    "db": 'news',   #改同一个数据库了。
    "port": 3306,
    "charset": 'utf8'  #这个是数据库的配置文件
}

                #时间测试的时候请直接在
startTime ={   #设定的运行时间，测试的话请输入大于你当前计算机时间的1分钟，如16：53-》16:54
    "time":"19:38"  #请用24小时制的字符串，win下如 '01:10'表示每天1点10分开始；如果是linux，'1:10'这样都可以
}

downloadPath = {   #这个路径设置到项目图片的根目录上个,例如下面这样。
    "path":r"..\static\images"
}