from django.urls import path

from . import views

# 在项目的url映射里设置命名空间,避免同名url
app_name = 'emoji'

urlpatterns = [
    # 表情搜索
    path('', views.index, name='index'),
    # 账号系统
    path('Login/', views.login, name='login'),
    path('Login/Validate/', views.validate, name='validate'),
    path('Register/', views.register, name='register'),
    path('Register/CreateUser/', views.createUser, name='createUser'),
    # 表情搜索
    path('Search/', views.search, name='search'),
    path('Ajax/', views.ajax, name='ajax'),
    # 颜文字搜索
    path('AsciiEmoji/<int:page>', views.asciiEmoji, name='asciiEmoji'),
    path('AsciiEmoji/Ajax/', views.asciiAjax, name='ajax'),
    path('AsciiEmoji/Search', views.asciiEmojiSearch, name='asciiEmojiSearch'),
    # 套图搜索
    path('EmojiSet/<int:page>/', views.emojiSet, name='emojiSet'),
    path('EmojiSet/detail/<str:series_name>/', views.detail, name='detail'),
    # 表情模板
    path('Template/<int:page>', views.templates, name='template'),
    path('Template/<str:img>', views.diy, name='diy'),
    path('Template/diy/', views.submitData, name='submit'),
    path('Template/diy/<str:material>/<str:text>/<str:font_size>/<str:color>/<str:font>/<str:email>',
         views.process_template,
         name='process_template'),
]
