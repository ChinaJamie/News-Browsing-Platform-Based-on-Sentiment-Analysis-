# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import BooleanField as _BooleanField

class BooleanField(_BooleanField):
	def get_prep_value(self, value):
		if value in ("0", "false", "False"):
			return False 
		elif value in ("1", "true", "True"):
			return True
		else:
			return super(BooleanField, self).get_prep_value(value)

Positive = 'POS'
Negative = 'NEG'
Neutral = 'NEU'
Sentiment_CHOICES = (
	(Positive, '积极'),
	(Negative, '消极'),
	(Neutral, '中性'),
	)

class User(models.Model):
	Account = models.CharField(max_length=50) #账号
	Password = models.CharField(max_length=200)	#密码
	EmailField = models.EmailField() #用户邮箱

class Statistics(models.Model):
	Date= models.DateField()	#日期
	Kind =models.CharField(max_length=100,default="") #新闻的类别
	Pos_news_num = models.IntegerField()	#积极新闻数
	Neu_news_num = models.IntegerField() #中性新闻数
	Neg_news_num = models.IntegerField()	#消极新闻数
	Pos_comment_num = models.IntegerField()	#积极评论数
	Neu_comment_num = models.IntegerField() #中性评论数
	Neg_comment_num = models.IntegerField()	#消极评论数

#==========================主页新闻===============================================

class HomeNews(models.Model):
	News_id=models.AutoField(primary_key=True)
	url = models.CharField(max_length=255)#URLUNIQUE
	Title=models.CharField(max_length=100)
	UrlState=models.BooleanField()
	Hcontent=models.TextField()
	Mcontent=models.TextField()
	Tcontent=models.TextField()
	Acontent=models.TextField()
	Date=models.DateField()
	fromWhere=models.CharField(max_length=100)
	class Meta:
		unique_together = ('url', 'Title',)
class HomeAnalysis_News(models.Model):
	News_id=models.ForeignKey(HomeNews,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=50,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）

class HomeComment(models.Model):
	News_id=models.ForeignKey(HomeNews,on_delete=models.CASCADE)	#对应新闻的id
	Comment_id= models.IntegerField(primary_key=True)    #评论id
	Reply_Comment_id= models.IntegerField(null=True) #是否是回复别人的评论，如果不是则为空，是则填对应的评论id
	NikeName=models.CharField(max_length=100)  #昵称
	Comment=models.TextField()  #评论
	Date=models.DateField() #评论时间

class HomeAnalysis_Comment(models.Model):
	Comment_id=models.ForeignKey(HomeComment,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=50,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）


#==========================娱乐类新闻===============================================

class EntertainmentNews(models.Model):
	News_id=models.AutoField(primary_key=True)
	url = models.CharField(max_length=255)	#URL UNIQUE
	Title=models.CharField(max_length=100) #新闻标题
	UrlState=models.BooleanField()
	Hcontent=models.TextField()
	Mcontent=models.TextField()	
	Tcontent=models.TextField()
	Acontent=models.TextField()
	Date=models.DateField()
	fromWhere=models.CharField(max_length=100)
	class Meta:
		unique_together = ('url', 'Title',)
		ordering = ['News_id']
class EntertainmentAnalysis_News(models.Model):
	News_id=models.ForeignKey(EntertainmentNews,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=50,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）

class EntertainmentComment(models.Model):
	News_id=models.ForeignKey(EntertainmentNews,on_delete=models.CASCADE)	#对应新闻的id
	Comment_id= models.IntegerField(primary_key=True)    #评论id
	Reply_Comment_id= models.IntegerField(null=True) #是否是回复别人的评论，如果不是则为空，是则填对应的评论id
	NikeName=models.CharField(max_length=100)  #昵称
	Comment=models.TextField()  #评论
	Date=models.DateField() #评论时间

class EntertainmentAnalysis_Comment(models.Model):
	Comment_id=models.ForeignKey(EntertainmentComment,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=2,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）


#==========================运动类新闻===============================================

class SportsNews(models.Model):
	News_id=models.AutoField(primary_key=True)
	url = models.CharField(max_length=255)	#URL UNIQUE
	Title=models.CharField(max_length=100) #新闻标题
	UrlState=models.BooleanField()
	Hcontent=models.TextField()
	Mcontent=models.TextField()	
	Tcontent=models.TextField()
	Acontent=models.TextField()
	Date=models.DateField()
	fromWhere=models.CharField(max_length=100)
	class Meta:
		unique_together = ('url', 'Title',)
class SportsAnalysis_News(models.Model):
	News_id=models.ForeignKey(SportsNews,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=50,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）

class SportsComment(models.Model):
	News_id=models.ForeignKey(SportsNews,on_delete=models.CASCADE)	#对应新闻的id
	Comment_id= models.IntegerField(primary_key=True)    #评论id
	Reply_Comment_id= models.IntegerField(null=True) #是否是回复别人的评论，如果不是则为空，是则填对应的评论id
	NikeName=models.CharField(max_length=100)  #昵称
	Comment=models.TextField()  #评论
	Date=models.DateField() #评论时间

class SportsAnalysis_Comment(models.Model):
	Comment_id=models.ForeignKey(SportsComment,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=2,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）




#==========================财经类新闻===============================================

class FinanceNews(models.Model):
	News_id=models.AutoField(primary_key=True)
	url = models.CharField(max_length=255)	#URL UNIQUE
	Title=models.CharField(max_length=100) #新闻标题
	UrlState=models.BooleanField()
	Hcontent=models.TextField()
	Mcontent=models.TextField()	
	Tcontent=models.TextField()
	Acontent=models.TextField()
	Date=models.DateField()
	fromWhere=models.CharField(max_length=100)
	class Meta:
		unique_together = ('url', 'Title',)
class FinanceAnalysis_News(models.Model):
	News_id=models.ForeignKey(FinanceNews,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=50,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）

class FinanceComment(models.Model):
	News_id=models.ForeignKey(FinanceNews,on_delete=models.CASCADE)	#对应新闻的id
	Comment_id= models.IntegerField(primary_key=True)    #评论id
	Reply_Comment_id= models.IntegerField(null=True) #是否是回复别人的评论，如果不是则为空，是则填对应的评论id
	NikeName=models.CharField(max_length=100)  #昵称
	Comment=models.TextField()  #评论
	Date=models.DateField() #评论时间

class FinanceAnalysis_Comment(models.Model):
	Comment_id=models.ForeignKey(FinanceComment,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=2,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）



#==========================科技类新闻===============================================

class TechnologyNews(models.Model):
	News_id=models.AutoField(primary_key=True)
	url = models.CharField(max_length=255)	#URL UNIQUE
	Title=models.CharField(max_length=100) #新闻标题
	UrlState=models.BooleanField()
	Hcontent=models.TextField()
	Mcontent=models.TextField()	
	Tcontent=models.TextField()
	Acontent=models.TextField()
	Date=models.DateField()
	fromWhere=models.CharField(max_length=100)
	class Meta:
		unique_together = ('url', 'Title',)
class TechnologyAnalysis_News(models.Model):
	News_id=models.ForeignKey(TechnologyNews,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=50,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）

class TechnologyComment(models.Model):
	News_id=models.ForeignKey(TechnologyNews,on_delete=models.CASCADE)	#对应新闻的id
	Comment_id= models.IntegerField(primary_key=True)    #评论id
	Reply_Comment_id= models.IntegerField(null=True) #是否是回复别人的评论，如果不是则为空，是则填对应的评论id
	NikeName=models.CharField(max_length=100)  #昵称
	Comment=models.TextField()  #评论
	Date=models.DateField() #评论时间

class TechnologyAnalysis_Comment(models.Model):
	Comment_id=models.ForeignKey(TechnologyComment,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=2,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）



#==========================汽车类新闻===============================================

class CarNews(models.Model):
	News_id=models.AutoField(primary_key=True)
	url = models.CharField(max_length=255)	#URL UNIQUE
	Title=models.CharField(max_length=100) #新闻标题
	UrlState=models.BooleanField()
	Hcontent=models.TextField()
	Mcontent=models.TextField()	
	Tcontent=models.TextField()
	Acontent=models.TextField()
	Date=models.DateField()
	fromWhere=models.CharField(max_length=100)
	class Meta:
		unique_together = ('url', 'Title',)
class CarAnalysis_News(models.Model):
	News_id=models.ForeignKey(CarNews,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=50,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）

class CarComment(models.Model):
	News_id=models.ForeignKey(CarNews,on_delete=models.CASCADE)	#对应新闻的id
	Comment_id= models.IntegerField(primary_key=True)    #评论id
	Reply_Comment_id= models.IntegerField(null=True) #是否是回复别人的评论，如果不是则为空，是则填对应的评论id
	NikeName=models.CharField(max_length=100)  #昵称
	Comment=models.TextField()  #评论
	Date=models.DateField() #评论时间

class CarAnalysis_Comment(models.Model):
	Comment_id=models.ForeignKey(CarComment,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=2,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）

#==========================房产类新闻===============================================

class HouseNews(models.Model):
	News_id=models.AutoField(primary_key=True)
	url = models.CharField(max_length=255)	#URL UNIQUE
	Title=models.CharField(max_length=100) #新闻标题
	UrlState=models.BooleanField()
	Hcontent=models.TextField()
	Mcontent=models.TextField()	
	Tcontent=models.TextField()
	Acontent=models.TextField()
	Date=models.DateField()
	fromWhere=models.CharField(max_length=100)
	class Meta:
		unique_together = ('url', 'Title',)
class HouseAnalysis_News(models.Model):
	News_id=models.ForeignKey(HouseNews,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=50,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）

class HouseComment(models.Model):
	News_id=models.ForeignKey(HouseNews,on_delete=models.CASCADE)	#对应新闻的id
	Comment_id= models.IntegerField(primary_key=True)    #评论id
	Reply_Comment_id= models.IntegerField(null=True) #是否是回复别人的评论，如果不是则为空，是则填对应的评论id
	NikeName=models.CharField(max_length=100)  #昵称
	Comment=models.TextField()  #评论
	Date=models.DateField() #评论时间

class HouseAnalysis_Comment(models.Model):
	Comment_id=models.ForeignKey(HouseComment,on_delete=models.CASCADE)
	Pos_Score = models.FloatField() #积极分数
	Neg_score = models.FloatField() #消极分数
	Sentiment = models.CharField(
		max_length=2,
		choices=Sentiment_CHOICES,
		default = Neutral
	)	#情感极性（三个选一个的字段）