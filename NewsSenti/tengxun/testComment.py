import time
import traceback


from bs4 import BeautifulSoup
from pprint import pprint

from newsCrawl.tengxun.makebeautifulSoup import makeBS

Cooker = makeBS()


commentRawUrl = "http://coral.qq.com/"   # id附在上面就可以读取出来的了。
cmt_id = 2326922651
# response = requests.get(commentRawUrl+str(cmt_id))
BS = Cooker.makesoup(commentRawUrl+str(cmt_id))  # 传进来是微信的才可以一

pprint(BS)
"http://coral.qq.com/article/2326922651/comment/#"  #把id塞到这个链接可以返回50条评论。json格式。
