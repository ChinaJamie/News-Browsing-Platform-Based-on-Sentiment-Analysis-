#下载到的一个路径中去，把图片下载下来，并且把新闻里面的
import os
import traceback
import requests ##导入requests

from config import downloadPath


class Download:
    def __init__(self,path): #先设置好下载的路径
        if(path==None):
            self.path=downloadPath['path']  #默认使用配置文件的地址
            print("是 None")
        else:
            self.path = path

    def downloadImg(self,img_url,imgName,referer,now_date):   #这个下载的模块是没有返回值的,
        headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",'Referer':referer}   ##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
        try:
            # int(shit)    #todo 图片可以不下载了
            img = requests.get(img_url, headers=headers)
            # print(img)
            # print(self.path)
            if(False==os.path.exists(os.path.join(self.path ,now_date))):  #不存在这个目录的话
                os.makedirs(self.path + '/'+now_date)
            dPath = os.path.join(self.path ,now_date, imgName+'.jpg')  #imgName传进来不需要带时间
            # print(dPath)
            print("图片的文件名"+self.path + '/'+now_date+"/"+imgName+'.jpg')
            f = open(dPath, 'ab')
            f.write(img.content)
            f.close()
            # print("下载成功")
        except Exception as e:
            print(e)
            traceback.print_exc()

if __name__=="__main__":
    #局部测试代码
    imgUrl = "http://inews.gtimg.com/newsapp_match/0/5403685404/0"
    downloadTool  = Download(None)  #todo 这儿有一个问题就是，这个图片的下载地址网页部分是带地址的，所以，最好的是网页部分不需要要再加上地址的文件夹，统一使用
    downloadTool. downloadImg ( img_url="http://inews.gtimg.com/newsapp_match/0/8158252661/0",imgName="zhangfei",referer=None,now_date="20190309")