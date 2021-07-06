## News-Browsing-Platform-Based-on-Sentiment-Analysis-
This project is mainly divided into three modules:            
1. Climbing module: Climbing news data and commentary data of Tencent and Sina platforms regularly every day.  

2. Emotional Analysis Module: At present, the Sentiment algorithm based on pattern matching will be updated to the algorithm based on Deep learning.    

3. Web Framework: This project is built by Django, which is maintainable. 

## Dependence:


bs4==0.0.1


DBUtils==1.3


Django==2.1.7

decorator==4.1.2

h5py==2.7.0

jieba==0.39

lxml==4.2.5

matplotlib==2.1.1

numpy==1.15.4

pandas==0.20.3

PyMySQL==0.9.3

requests==2.18.4

retrying==1.3.3

tensorflow==1.1.0

wordcloud==1.5.0

## Usage
# 1、tengxun：爬虫目录，每天定时爬取腾讯新闻。

config.py：配置每日更新时间、爬虫保存数据库

everyDayTengxun.py：爬虫主要爬取模块

# 2、NewsSentimentAnalysis：Web框架

manage.py：入口文件


## Project Todo
1. After login into the home page,the Menu bar above can show the logined user name .

