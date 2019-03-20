#-*-coding:utf8-*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from NewsSentimentAnalysis.models import User
from NewsSentimentAnalysis.models import HomeNews,HomeAnalysis_News
from NewsSentimentAnalysis.models import EntertainmentNews,EntertainmentAnalysis_News
from NewsSentimentAnalysis.models import SportsNews,SportsAnalysis_News
from django.contrib.auth.decorators import login_required
import datetime
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

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
@login_required
def index(request):
	News_Home_1=[]
	News_Home_2=[]
	News_obj = HomeNews.objects.filter(Date =Yesterday)
	num = 0
	for news in News_obj:
		dic ={}
		dic['Title']=news.Title
		dic['News_id']=news.News_id
		dic['url']=news.url
		dic['Date']=news.Date
		score = HomeAnalysis_News.objects.get(News_id=news.News_id)
		dic['Pos_Score']=score.Pos_Score
		dic['Neg_score']=score.Neg_score
		dic['Sentiment']=score.Sentiment
		num +=1
		if num <=5:
			News_Home_1.append(dic)
		elif num>5 and num <=10:
			News_Home_2.append(dic)
		else:
			break
	return render(request,'index.html',locals())
########################################################################################################################
def list_page(request,Obj,Ana_Obj,theme,page_num):
	##本函数是用entertainment_list函数进行测试，为了方便重用而封装起来的，基本都是一样的
	##用于查询新闻列表页面要显示的信息并传到前端页面使用，包括分页
	##特别注意：theme不能直接传，要以字符串传过去才可以，如，theme="sports"

	#Obj:传入的表对象
	#page_num:每页显示多少条
	#theme:新闻类别
	News_page=[] #每页的结果
	News_total=[]#所有的新闻结果

	Table_obj=Obj.objects.all().order_by('-Date') #按照日期逆序显示-Date是逆序
	for news in Table_obj:
		dic ={} #每条新闻一个字典，里面包含这条新闻的属性信息，再用News_total包起来，最后根据分页器给出的start和end索引，来切分每页显示第几条到第几条的新闻标题
		dic['Title']=news.Title #要显示文章的标题
		dic['News_id']=news.News_id #拿来拼接详情页URL
		Sem_obj = Ana_Obj.objects.get(News_id =news.News_id)#查询该newsid的新闻情感极性，要显示
		dic['Sentiment']=Sem_obj.Sentiment
		dic['Date']=news.Date #新闻标题右侧要显示日期
		dic['url']= "/"+str(theme)+"?id="+str(news.News_id) #详情页url，范例：/sports?id=新闻的Newsid
		News_total.append(dic) #都加入News_total
	#-------------------------------------------------------------------------------------
	#分页功能
	page_no = request.GET.get('page') #当前页号
	P = Paginator(Table_obj,page_num) 
	page = P.page(page_no)#当前第几页，共几页，返回前端进行显示
	#-------------------------------------------------------------------------------------
	previous =page.has_previous()#是否有上一页
	if page.has_previous():#是否有上一页: 
		previous_url = url_seg="/"+str(theme)+"_list?page="+str(page.previous_page_number())
	else:
		previous_url = False
	#-------------------------------------------------------------------------------------
	last =page.has_next()#是否有下一页，不能删，这个变量要传到前端页面判断是否显示下一页，下面同理
	if last:#如果有就拼接下一个的url
		last_url ="/"+str(theme)+"_list?page="+str(page.next_page_number())
	else:
		last_url = False
	#-------------------------------------------------------------------------------------
	start = page.start_index()#开始索引
	end = page.end_index()#结束索引
	News_page=News_total[(start-1):(end-1)] #该页号显示的部分新闻
	return page,previous,last,News_page,previous_url,last_url


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




########################################################################################################################################
from NewsSentimentAnalysis.WordCloud import Gen_WordCloud
#这个函数也是从entertainment函数提取出来的，可以为其他类新闻详情页所用
def detail_page(request,Obj,Ana_Obj):
	id = request.GET.get('id')
	News_obj=Obj.objects.get(News_id =id)
	Title = News_obj.Title
	Acontent = News_obj.Acontent
	Tcontent = News_obj.Tcontent
	image_path=Gen_WordCloud(Tcontent,News_obj.News_id) #生成词云，并返回该条新闻词云文件路径
	Sem_obj = Ana_Obj.objects.get(News_id =id)
	return Acontent,Sem_obj,image_path


@login_required
def entertainment(request):
	Acontent,Sem_obj,image_path = detail_page(request,EntertainmentNews,EntertainmentAnalysis_News)
	return render(request,'entertainment.html',locals())

@login_required
def sports(request):
	Acontent,Sem_obj,image_path = detail_page(request,SportsNews,SportsAnalysis_News)
	return render(request,'sports.html',locals())














###############################################################################################
#以下的未修改

@login_required
def report(request):
	return render(request,'report.html')
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



