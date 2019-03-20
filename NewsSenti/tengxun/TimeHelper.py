
import time
print (time.time())
print(time.strftime('%Y-%m-%d',time.localtime(time.time())))

import datetime

class TimeHelper:
    def getTimeList(self,start,end):
        # start = start
        # end = end
        dateList = []
        datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
        while datestart < dateend:
            datestart += datetime.timedelta(days=1)
            # print(datestart.strftime('%Y-%m-%d'))
            dateList.append(datestart.strftime('%Y-%m-%d'))
        return dateList
