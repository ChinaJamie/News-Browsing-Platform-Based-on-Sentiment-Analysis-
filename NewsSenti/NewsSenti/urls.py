"""NewsSenti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from NewsSentimentAnalysis import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('report/',views.report),
    path('car/',views.car),
    path('echarts/',views.echarts),
    path('house/',views.house),
    path('index/',views.index),
    path('finance/',views.finance),
    path('news/',views.news),
    path('entertainment',views.entertainment),
    path('entertainment_list/',views.entertainment_list),
    path('sports',views.sports),
    path('sports_list/',views.sports_list),
    path('technology/',views.technology),

    path('login_action/',views.login_action),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
