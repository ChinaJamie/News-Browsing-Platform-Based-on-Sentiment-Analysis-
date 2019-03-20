from django.contrib import admin

# Register your models here.
from NewsSentimentAnalysis.models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
	search_fields=('Account','Password','EmailField')
	list_display=('Account','Password','EmailField')
	list_filter=('Account',)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['Date','Kind','Pos_news_num','Neu_news_num','Neg_news_num','Pos_comment_num','Neu_comment_num','Neg_comment_num']
    list_filter = ['Date','Kind']
    search_fields = ['Date','Kind']
#========================================HomeNews=====================================
class HomeNewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'url','Title','UrlState','Hcontent','Mcontent','Tcontent','Acontent','Date','fromWhere']
    list_filter = ['Date', 'fromWhere']
    search_fields = ['News_id','Title','fromWhere']
class HomeAnalysis_NewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['News_id',]
class HomeCommentAdmin(admin.ModelAdmin):
    list_display = ['News_id','Comment_id','Reply_Comment_id','NikeName','Comment','Date']
    list_filter = ['Date']
    search_fields = ['NikeName']
class HomeAnalysis_CommentAdmin(admin.ModelAdmin):
    list_display = ['Comment_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['Comment_id',]

#========================================EntertainmentNews=====================================
class EntertainmentNewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'url','Title','UrlState','Hcontent','Mcontent','Tcontent','Acontent','Date','fromWhere']
    list_filter = ['Date', 'fromWhere']
    search_fields = ['News_id','Title','fromWhere']
class EntertainmentAnalysis_NewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['News_id',]
class EntertainmentCommentAdmin(admin.ModelAdmin):
    list_display = ['News_id','Comment_id','Reply_Comment_id','NikeName','Comment','Date']
    list_filter = ['Date']
    search_fields = ['NikeName']
class EntertainmentAnalysis_CommentAdmin(admin.ModelAdmin):
    list_display = ['Comment_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['Comment_id',]
#==========================Sports===============================================
class SportsNewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'url','Title','UrlState','Hcontent','Mcontent','Tcontent','Acontent','Date','fromWhere']
    list_filter = ['Date', 'fromWhere']
    search_fields = ['News_id','Title','fromWhere']
class SportsAnalysis_NewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['News_id',]
class SportsCommentAdmin(admin.ModelAdmin):
    list_display = ['News_id','Comment_id','Reply_Comment_id','NikeName','Comment','Date']
    list_filter = ['Date']
    search_fields = ['NikeName']
class SportsAnalysis_CommentAdmin(admin.ModelAdmin):
    list_display = ['Comment_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['Comment_id',]
#==========================Finance===============================================
class FinanceNewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'url','Title','UrlState','Hcontent','Mcontent','Tcontent','Acontent','Date','fromWhere']
    list_filter = ['Date', 'fromWhere']
    search_fields = ['News_id','Title','fromWhere']
class FinanceAnalysis_NewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['News_id',]
class FinanceCommentAdmin(admin.ModelAdmin):
    list_display = ['News_id','Comment_id','Reply_Comment_id','NikeName','Comment','Date']
    list_filter = ['Date']
    search_fields = ['NikeName']
class FinanceAnalysis_CommentAdmin(admin.ModelAdmin):
    list_display = ['Comment_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['Comment_id',]
#==========================Technology===============================================
class TechnologyNewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'url','Title','UrlState','Hcontent','Mcontent','Tcontent','Acontent','Date','fromWhere']
    list_filter = ['Date', 'fromWhere']
    search_fields = ['News_id','Title','fromWhere']
class TechnologyAnalysis_NewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['News_id',]
class TechnologyCommentAdmin(admin.ModelAdmin):
    list_display = ['News_id','Comment_id','Reply_Comment_id','NikeName','Comment','Date']
    list_filter = ['Date']
    search_fields = ['NikeName']
class TechnologyAnalysis_CommentAdmin(admin.ModelAdmin):
    list_display = ['Comment_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['Comment_id',]
#==========================Car===============================================
class CarNewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'url','Title','UrlState','Hcontent','Mcontent','Tcontent','Acontent','Date','fromWhere']
    list_filter = ['Date', 'fromWhere']
    search_fields = ['News_id','Title','fromWhere']
class CarAnalysis_NewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['News_id',]
class CarCommentAdmin(admin.ModelAdmin):
    list_display = ['News_id','Comment_id','Reply_Comment_id','NikeName','Comment','Date']
    list_filter = ['Date']
    search_fields = ['NikeName']
class CarAnalysis_CommentAdmin(admin.ModelAdmin):
    list_display = ['Comment_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['Comment_id',]
#==========================House===============================================
class HouseNewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'url','Title','UrlState','Hcontent','Mcontent','Tcontent','Acontent','Date','fromWhere']
    list_filter = ['Date', 'fromWhere']
    search_fields = ['News_id','Title','fromWhere']
class HouseAnalysis_NewsAdmin(admin.ModelAdmin):
    list_display = ['News_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['News_id',]
class HouseCommentAdmin(admin.ModelAdmin):
    list_display = ['News_id','Comment_id','Reply_Comment_id','NikeName','Comment','Date']
    list_filter = ['Date']
    search_fields = ['NikeName']
class HouseAnalysis_CommentAdmin(admin.ModelAdmin):
    list_display = ['Comment_id', 'Pos_Score','Neg_score','Sentiment']
    list_filter = ['Sentiment']
    search_fields = ['Comment_id',]

admin.site.register(User,UserAdmin)
admin.site.register(Statistics,StatisticsAdmin)

admin.site.register(HomeNews,HomeNewsAdmin)
admin.site.register(HomeAnalysis_News,HomeAnalysis_NewsAdmin)
admin.site.register(HomeComment,HomeCommentAdmin)
admin.site.register(HomeAnalysis_Comment,HomeAnalysis_CommentAdmin)

admin.site.register(EntertainmentNews,EntertainmentNewsAdmin)
admin.site.register(EntertainmentAnalysis_News,EntertainmentAnalysis_NewsAdmin)
admin.site.register(EntertainmentComment,EntertainmentCommentAdmin)
admin.site.register(EntertainmentAnalysis_Comment,EntertainmentAnalysis_CommentAdmin)


admin.site.register(SportsNews,SportsNewsAdmin)
admin.site.register(SportsAnalysis_News,SportsAnalysis_NewsAdmin)
admin.site.register(SportsComment,SportsCommentAdmin)
admin.site.register(SportsAnalysis_Comment,SportsAnalysis_CommentAdmin)

admin.site.register(FinanceNews,FinanceNewsAdmin)
admin.site.register(FinanceAnalysis_News,FinanceAnalysis_NewsAdmin)
admin.site.register(FinanceComment,FinanceCommentAdmin)
admin.site.register(FinanceAnalysis_Comment,FinanceAnalysis_CommentAdmin)

admin.site.register(TechnologyNews,TechnologyNewsAdmin)
admin.site.register(TechnologyAnalysis_News,TechnologyAnalysis_NewsAdmin)
admin.site.register(TechnologyComment,TechnologyCommentAdmin)
admin.site.register(TechnologyAnalysis_Comment,TechnologyAnalysis_CommentAdmin)

admin.site.register(CarNews,CarNewsAdmin)
admin.site.register(CarAnalysis_News,CarAnalysis_NewsAdmin)
admin.site.register(CarComment,CarCommentAdmin)
admin.site.register(CarAnalysis_Comment,CarAnalysis_CommentAdmin)

admin.site.register(HouseNews,HouseNewsAdmin)
admin.site.register(HouseAnalysis_News,HouseAnalysis_NewsAdmin)
admin.site.register(HouseComment,HouseCommentAdmin)
admin.site.register(HouseAnalysis_Comment,HouseAnalysis_CommentAdmin)