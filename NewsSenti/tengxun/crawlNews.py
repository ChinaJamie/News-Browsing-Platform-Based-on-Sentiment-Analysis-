import datetime
import multiprocessing
import os
import schedule
import time
  # todo 这个是汇总的，定时功能因为那儿打开
from DBcontrol import DB
from config import startTime
from everyDayTengxun import EveryTengxun


def worker_2(interval):
    print ("腾讯的子进程开始工作")
    everyDayTengxun = EveryTengxun()  # 先这样设置好来就可以了
    one = everyDayTengxun.getEveryTengxun()  #这样就行了对吧  #这儿就在执行这个函数了
    print ("腾讯的完成了今天的爬取")


class AutoRunAtTime:              #这儿应该是三个线程的
    def job(self,name):   #这个是主线程把
        dbhelper = DB()
        print("正在爬取今天的新闻内容")
        print('这里是进程: %sd   父进程ID：%s' % (os.getpid(), os.getppid()))
        # p1 = multiprocessing.Process(target=worker_1, args=(6,))
        p2 = multiprocessing.Process(target=worker_2, args=(3,))
        # p3 = multiprocessing.Process(target=worker_3, args=(4,))

        # p1.daemon = True
        p2.daemon = True

        # p1.start()
        p2.start()
        # p3.start()
        print("The number of CPU is:" + str(multiprocessing.cpu_count()))
        for p in multiprocessing.active_children():
            print("child   p.name:" + p.name + "\tp.id" + str(p.pid))

        p2.join()

        print("today work done ND!!!!!!!!!!!!!!!!!")  # 这是是主线程，如何让主线程等待子线程结束后才输出呢
        print("all over !")
        print("正在去重。。。")
        dbhelper.quchong()  # 执行去重的东西
        print("正在等待明天的到来，")
        dbhelper.getAllTitle()
        # time.sleep(60 * 60 * 24)  # 要加一个排错的东西


    def startAutoRun(self,timeSet):         #24小时制的时间输入，传入一个时间的字符串
        name = "hello"
        # schedule.every(10).minutes.do(job, name)
        # schedule.every().hour.do(job, name)
        schedule.every().day.at(timeSet).do(self.job, name)  # 应该也是24小时制的，记得  “输入24小时制的时间字符串
        # schedule.every(5).to(10).days.do(job, name)
        # schedule.every().monday.do(job, name)
        # schedule.every().wednesday.at("13:15").do(job, name)

        while True:
            schedule.run_pending()
            time.sleep(1)





if __name__=="__main__":
    autoRun = AutoRunAtTime()
    print(time.strftime('%Y.%m.%d', time.localtime(time.time())))
    print("现在的时间是")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #设置时间请去config中设置
    # autoRun.startAutoRun(startTime['time'])    #正式跑空这种读取配置文件
    autoRun.startAutoRun("19:55")    #测试直接这儿写运行时间比较方便








