#-*-coding:utf8-*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from NewsSentimentAnalysis.models import User
from NewsSentimentAnalysis.models import HomeNews,HomeAnalysis_News,HomeComment,HomeAnalysis_Comment
from NewsSentimentAnalysis.models import EntertainmentNews,EntertainmentAnalysis_News,EntertainmentComment,EntertainmentAnalysis_Comment
from NewsSentimentAnalysis.models import SportsNews,SportsAnalysis_News,SportsComment,SportsAnalysis_Comment
from NewsSentimentAnalysis.models import FinanceNews,FinanceAnalysis_News,FinanceComment,FinanceAnalysis_Comment
from NewsSentimentAnalysis.models import TechnologyNews,TechnologyAnalysis_News,TechnologyComment,TechnologyAnalysis_Comment
from NewsSentimentAnalysis.models import CarNews,CarAnalysis_News,CarComment,CarAnalysis_Comment
from NewsSentimentAnalysis.models import HouseNews,HouseAnalysis_News,HouseComment,HouseAnalysis_Comment
from django.contrib.auth.decorators import login_required
import datetime
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import json
from django.db.models import Q

#获取当天日期
#nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
#pastTime = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')#过去一小时时间
#afterTomorrowTime = (datetime.datetime.now()+datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')#后天
Yesterday = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')#昨天

##################################################################################################################
#登陆操作和主页显示
def login(request):
	return render(request,'login.html')
def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username','')#输入的用户名
		password = request.POST.get('password','')#输入的密码 str
		pwd = User.objects.get(Account = username).Password
		if pwd == password:
			response = HttpResponseRedirect('/index')
			request.session['user'] = username
			return response
		else:
			return render(request, 'login.html', {'error': 'username or password error!'})

def index(request):
	News_Home=[]
	News_obj = HomeNews.objects.filter(Date =Yesterday)
	num = 0
	for news in News_obj:
		dic ={}
		dic['Title']=news.Title
		dic['News_id']=news.News_id
		dic['url']="/news_detail?theme=home&id="+str(news.News_id)
		dic['Date']=news.Date
		dic['Hcontent']=news.Tcontent[0:50]
		score = HomeAnalysis_News.objects.get(News_id=news.News_id)
		dic['Pos_Score']=score.Pos_Score
		dic['Neg_Score']=score.Neg_score
		dic['Sentiment']=score.Sentiment
		num +=1
		if num <=8:
			News_Home.append(dic)
		else:
			break
	return render(request,'index.html',locals())
########################################################################################################################
def getNewsWordCloudSrc(url):   #输入的是数据库中各个分类后的新闻的url字段
    News_Id = url.replace("$", "").replace("/", "").replace(":", "_").replace(".", "_")
    return "/static/images/WordCloud/"+News_Id+".png"

def news_list(request):
	theme = request.GET.get('theme')
	theme_trans ={
	'home':[HomeNews,HomeAnalysis_News,HomeComment,HomeAnalysis_Comment],
	'sports':[SportsNews,SportsAnalysis_News,SportsComment,SportsAnalysis_Comment],
	'entertainment':[EntertainmentNews,EntertainmentAnalysis_News,EntertainmentComment,EntertainmentAnalysis_Comment],
	'finance':[FinanceNews,FinanceAnalysis_News,FinanceComment,FinanceAnalysis_Comment],
	'technology':[TechnologyNews,TechnologyAnalysis_News,TechnologyComment,TechnologyAnalysis_Comment],
	'car':[CarNews,CarAnalysis_News,CarComment,CarAnalysis_Comment],
	'house':[HouseNews,HouseAnalysis_News,HouseComment,HouseAnalysis_Comment]
	}
	News_Obj=theme_trans[theme][0]
	Ana_Obj=theme_trans[theme][1]

	
	
	page,previous,last,News_page,previous_url,last_url = list_page(request,News_Obj,Ana_Obj,theme,10)
	Date,POS,NEG = list_chart(News_Obj,Ana_Obj)
	return render(request,'news_list.html',locals())

def list_chart(News_Obj,Ana_Obj):
	Date =[]
	POS=[]
	NEG=[]
	
	for day in range(1,8):
		D = (datetime.datetime.now()-datetime.timedelta(days=day)).strftime('%Y-%m-%d')#昨天
		Date.append(D) #每一天的日期
		News = News_Obj.objects.filter(Date=D) #该天日期的所有News对象
		pos=0
		neg=0
		for n in News:
			Sem_obj = Ana_Obj.objects.get(News_id =n.News_id)#对于每一个对象，查询其情感极性
			if Sem_obj.Sentiment =='POS':
				pos+=1
			else:
				neg+=1
		POS.append(pos)
		NEG.append(neg)
	return Date,POS,NEG

def list_page(request,Obj,Ana_Obj,theme,page_num):
	##本函数是用entertainment_list函数进行测试，为了方便重用而封装起来的，基本都是一样的
	##用于查询新闻列表页面要显示的信息并传到前端页面使用，包括分页
	##特别注意：theme不能直接传，要以字符串传过去才可以，如，theme="sports"

	#Obj:传入的表对象
	#page_num:每页显示多少条
	#theme:新闻类别
	News_page=[] #每页的结果
	News_total=[]#所有的新闻结果

	Table_obj=Obj.objects.all().order_by('-Date')[0:100] #按照日期逆序显示-Date是逆序
	for news in Table_obj:
		dic ={} #每条新闻一个字典，里面包含这条新闻的属性信息，再用News_total包起来，最后根据分页器给出的start和end索引，来切分每页显示第几条到第几条的新闻标题
		dic['Title']=news.Title #要显示文章的标题
		dic['News_id']=news.News_id #拿来拼接详情页URL
		dic['Tcontent']=news.Tcontent[0:50]
		dic['image_path']=getNewsWordCloudSrc(news.url)
		Sem_obj = Ana_Obj.objects.get(News_id =news.News_id)#查询该newsid的新闻情感极性，要显示
		dic['Pos_Score']=Sem_obj.Pos_Score
		dic['Neg_Score']=Sem_obj.Neg_score
		dic['Sentiment']=Sem_obj.Sentiment
		dic['Date']=news.Date #新闻标题右侧要显示日期
		dic['url']= "/news_detail?theme="+str(theme)+"&id="+str(news.News_id) #详情页url，范例：/sports?id=新闻的Newsid
		News_total.append(dic) #都加入News_total
	#-------------------------------------------------------------------------------------
	#分页功能
	page_no = request.GET.get('page') #当前页号
	P = Paginator(Table_obj,page_num) 
	page = P.page(page_no)#当前第几页，共几页，返回前端进行显示
	#-------------------------------------------------------------------------------------
	previous =page.has_previous()#是否有上一页
	if page.has_previous():#是否有上一页: 
		previous_url = request.path+"?theme="+theme+"&page="+str(page.previous_page_number())
	else:
		previous_url = False
	#-------------------------------------------------------------------------------------
	last =page.has_next()#是否有下一页，不能删，这个变量要传到前端页面判断是否显示下一页，下面同理
	if last:#如果有就拼接下一个的url
		last_url =request.path+"?theme="+theme+"&page="+str(page.next_page_number())
	else:
		last_url = False
	#-------------------------------------------------------------------------------------
	start = page.start_index()#开始索引
	end = page.end_index()#结束索引
	News_page=News_total[(start-1):(end-1)] #该页号显示的部分新闻
	return page,previous,last,News_page,previous_url,last_url







########################################################################################################################################
from NewsSentimentAnalysis.WordCloud import Gen_WordCloud
#这个函数也是从entertainment函数提取出来的，可以为其他类新闻详情页所用
def news_detail(request): 
	#新闻详情页
	theme = request.GET.get('theme')
	theme_trans ={
	'home':[HomeNews,HomeAnalysis_News,HomeComment,HomeAnalysis_Comment],
	'sports':[SportsNews,SportsAnalysis_News,SportsComment,SportsAnalysis_Comment],
	'entertainment':[EntertainmentNews,EntertainmentAnalysis_News,EntertainmentComment,EntertainmentAnalysis_Comment],
	'finance':[FinanceNews,FinanceAnalysis_News,FinanceComment,FinanceAnalysis_Comment],
	'technology':[TechnologyNews,TechnologyAnalysis_News,TechnologyComment,TechnologyAnalysis_Comment],
	'car':[CarNews,CarAnalysis_News,CarComment,CarAnalysis_Comment],
	'house':[HouseNews,HouseAnalysis_News,HouseComment,HouseAnalysis_Comment]
	}
	News_Obj=theme_trans[theme][0]
	Ana_Obj=theme_trans[theme][1]

	id = request.GET.get('id') #获取新闻id
	news_obj=News_Obj.objects.get(News_id =id)
	URL ="/news_list?theme="+theme+"&page=1"
	Title = news_obj.Title #新闻标题
	Date = news_obj.Date
	Acontent = news_obj.Acontent #新闻详情
	image_path=getNewsWordCloudSrc(news_obj.url) #词云
	Sem_obj = Ana_Obj.objects.get(News_id =id)
	Sem_data=[]
	Sem_POS={}
	Sem_NEG={}

	Pos_Score=Sem_obj.Pos_Score
	Neg_Score=Sem_obj.Neg_score

	Sem_POS['value']=float(Pos_Score)
	Sem_NEG['value']=float(Neg_Score)
	Sem_POS['name']="积极得分"
	Sem_NEG['name']="消极得分"
	Sem_data.append(Sem_POS)
	Sem_data.append(Sem_NEG) #只要用到这个字典整个传过去就行
	Sentiment=Sem_obj.Sentiment

	#处理评论
	Com_res = []
	Com_obj = theme_trans[theme][2]
	Sen_obj = theme_trans[theme][3]
	Comm = Com_obj.objects.filter(News_id =id) #所有的评论对象
	for obj in Comm: #每一个对象
		dic={}
		dic['NickName'] = obj.NikeName
		dic['Comment'] = obj.Comment
		dic['Date'] = obj.Date
		S = Sen_obj.objects.get(Comment_id=obj.Comment_id)
		dic['Pos_Score']=S.Pos_Score
		dic['Neg_score']=S.Neg_score
		dic['Sentiment']=S.Sentiment
		Com_res.append(dic)


	return render(request,'news_details.html',locals())





def report(request): #统计页面
	POS_NUM = {
    "娱乐": 0,
    "体育": 0,
    "财经": 0,
    "科技": 0,
    "汽车": 0,
    "房产": 0,
    "热点": 0
  }
	NEG_NUM = {
    "娱乐": 0,
    "体育": 0,
    "财经": 0,
    "科技": 0,
    "汽车": 0,
    "房产": 0,
    "热点": 0
  }
	TOTAL = {
    "娱乐": 0,
    "体育": 0,
    "财经": 0,
    "科技": 0,
    "汽车": 0,
    "房产": 0,
    "热点": 0
  }
	COMMENT_NUM = {
  "积极评论": 0,
  "消极评论": 0,
  
}
	Date =[]
	for day in range(1,8):
		D = (datetime.datetime.now()-datetime.timedelta(days=day)).strftime('%Y-%m-%d')#昨天
		Date.append(D) #每一天的日期
	#先统计评论数
	HomeNews_POS ,HomeNews_NEG , HomeComm_POS , HomeComm_NEG = calc_news('home',Date)
	EntertainmentNews_POS ,EntertainmentNews_NEG , EntertainmentComm_POS , EntertainmentComm_NEG = calc_news('entertainment',Date)
	SportsNews_POS ,SportsNews_NEG , SportsComm_POS , SportsComm_NEG = calc_news('sports',Date)
	FinanceNews_POS ,FinanceNews_NEG , FinanceComm_POS , FinanceComm_NEG = calc_news('finance',Date)
	TechnologyNews_POS ,TechnologyNews_NEG , TechnologyComm_POS , TechnologyComm_NEG = calc_news('technology',Date)
	CarNews_POS ,CarNews_NEG , CarComm_POS , CarComm_NEG = calc_news('car',Date)
	HouseNews_POS ,HouseNews_NEG , HouseComm_POS , HouseComm_NEG = calc_news('house',Date)

	COMMENT_NUM["积极评论"]=HomeComm_POS+EntertainmentComm_POS+SportsComm_POS+FinanceComm_POS+TechnologyComm_POS+CarComm_POS+HouseComm_POS
	COMMENT_NUM["消极评论"]=HomeComm_NEG+EntertainmentComm_NEG+SportsComm_NEG+FinanceComm_NEG+TechnologyComm_NEG+CarComm_NEG+HouseComm_NEG

	POS_NUM["体育"] = SportsNews_POS
	NEG_NUM["体育"] = SportsNews_NEG
	TOTAL["体育"]=SportsNews_POS+SportsNews_NEG

	POS_NUM["财经"] = FinanceNews_POS
	NEG_NUM["财经"] = FinanceNews_NEG
	TOTAL["财经"]=FinanceNews_POS+FinanceNews_NEG

	POS_NUM["科技"] = TechnologyNews_POS
	NEG_NUM["科技"] = TechnologyNews_NEG
	TOTAL["科技"]=TechnologyNews_POS+TechnologyNews_NEG

	POS_NUM["汽车"] = CarNews_POS
	NEG_NUM["汽车"] = CarNews_NEG
	TOTAL["汽车"]=CarNews_POS+CarNews_NEG

	POS_NUM["房产"] = HouseNews_POS
	NEG_NUM["房产"] = HouseNews_NEG
	TOTAL["房产"]=HouseNews_POS+HouseNews_NEG

	POS_NUM["娱乐"] = EntertainmentNews_POS
	NEG_NUM["娱乐"] = EntertainmentNews_NEG
	TOTAL["娱乐"]=EntertainmentNews_POS+EntertainmentNews_NEG

	POS_NUM["热点"] = HomeNews_POS
	NEG_NUM["热点"] = HomeNews_NEG
	TOTAL["热点"]=HomeNews_POS+HomeNews_NEG

	ALL=TOTAL["体育"]+TOTAL["财经"]+TOTAL["科技"]+TOTAL["汽车"]+TOTAL["房产"]+TOTAL["娱乐"]+TOTAL["热点"]

	return render(request,'report.html',locals())

def calc_news(theme,Date):
	#爬取每一类新闻和评论并返回对应的统计值
	theme_trans ={
	'home':[HomeNews,HomeAnalysis_News,HomeComment,HomeAnalysis_Comment],
	'sports':[SportsNews,SportsAnalysis_News,SportsComment,SportsAnalysis_Comment],
	'entertainment':[EntertainmentNews,EntertainmentAnalysis_News,EntertainmentComment,EntertainmentAnalysis_Comment],
	'finance':[FinanceNews,FinanceAnalysis_News,FinanceComment,FinanceAnalysis_Comment],
	'technology':[TechnologyNews,TechnologyAnalysis_News,TechnologyComment,TechnologyAnalysis_Comment],
	'car':[CarNews,CarAnalysis_News,CarComment,CarAnalysis_Comment],
	'house':[HouseNews,HouseAnalysis_News,HouseComment,HouseAnalysis_Comment]
	}
	News_Obj=theme_trans[theme][0]
	NewsAna_Obj=theme_trans[theme][1]
	Comm_Obj=theme_trans[theme][2]
	CommAna_Obj=theme_trans[theme][3]

	Pos_news_num = 0 
	Neg_news_num = 0
	Pos_comm_num = 0
	Neg_comm_num = 0
	Neu_news_num = 0
	Neu_comm_num = 0
	
	for day in Date:
		D_news=News_Obj.objects.filter(Date=day) #七天每天的新闻 集合
		for d in D_news: #每条新闻
			if len(NewsAna_Obj.objects.filter(Q(News_id=d.News_id)&Q(Sentiment='POS')))!=0:
				Pos_news_num += 1
			elif len(NewsAna_Obj.objects.filter(Q(News_id=d.News_id)&Q(Sentiment='NEG')))!=0:
				Neg_news_num += 1
			else:
				Neu_news_num +=1
	'''
	for day in Date:
		D_comm=Comm_Obj.objects.filter(Date=day) #七天每天的评论 集合
		for c in D_comm:
			if len(CommAna_Obj.objects.filter(Q(Comment_id=c.Comment_id)&Q(Sentiment='POS')))!=0:
				Pos_comm_num += 1
			elif len(CommAna_Obj.objects.filter(Q(Comment_id=c.Comment_id)&Q(Sentiment='NEG')))!=0:
				Neg_comm_num += 1
			else:
				Neu_comm_num +=1
	return Pos_news_num,Neg_news_num,Pos_comm_num,Neg_comm_num
	'''
	#######################################################################################
	#评论集合统计
	
	P_comm = CommAna_Obj.objects.filter(Sentiment='POS')
	Pos_comm_num = len(P_comm)
	N_comm = NewsAna_Obj.objects.filter(Sentiment='NEG')
	Neg_comm_num = len(N_comm)
	return Pos_news_num,Neg_news_num,Pos_comm_num,Neg_comm_num
	
	######################################################################################
	#每日的评论统计
	'''
	D_comm=Comm_Obj.objects.filter(Date = Yesterday)#该条新闻所有评论
	for c in D_comm:#每条评论进行判断
		if len(CommAna_Obj.objects.filter(Q(Comment_id=c.Comment_id)&Q(Sentiment='POS')))!=0:
			Pos_comm_num += 1
		elif len(CommAna_Obj.objects.filter(Q(Comment_id=c.Comment_id)&Q(Sentiment='NEG')))!=0:
			Neg_comm_num += 1
		else:
				Neu_comm_num +=1
	
	return Pos_news_num,Neg_news_num,Pos_comm_num,Neg_comm_num
	'''
	

		












###############################################################################################
#以下的未使用



@login_required
def car(request):
	return render(request,'car.html')
@login_required
def echarts(request):
	return render(request,'echarts.html')
@login_required
def house(request):
	return render(request,'house.html')
@login_required
def finance(request):
	return render(request,'finance.html')
@login_required
def news(request):
	return render(request,'news.html')
@login_required
def technology(request):
	return render(request,'technology.html')


@login_required
def entertainment_list(request):
	theme = "entertainment"
	page,previous,last,News_page,previous_url,last_url = list_page(request,EntertainmentNews,EntertainmentAnalysis_News,theme,10)
	return render(request,'entertainment_list.html',locals())
#下面是调用到该函数的页面，都是新闻标题列表页
@login_required
def sports_list(request):
	theme="sports"
	page,previous,last,News_page,previous_url,last_url = list_page(request,SportsNews,SportsAnalysis_News,theme,10)
	return render(request,'sports_list.html',locals())

@login_required
def entertainment(request):
	Acontent,Sem_obj,image_path = detail_page(request,EntertainmentNews,EntertainmentAnalysis_News)
	return render(request,'entertainment.html',locals())

@login_required
def sports(request):
	Acontent,Sem_obj,image_path = detail_page(request,SportsNews,SportsAnalysis_News)
	return render(request,'sports.html',locals())
def detail_page(request,Obj,Ana_Obj):
	id = request.GET.get('id')
	News_obj=Obj.objects.get(News_id =id)
	Title = News_obj.Title #新闻标题
	Acontent = News_obj.Acontent #新闻详情
	image_path=getNewsWordCloudSrc(News_obj.url) #词云
	Sem_obj = Ana_Obj.objects.get(News_id =id)

	return Acontent,Sem_obj,image_path


