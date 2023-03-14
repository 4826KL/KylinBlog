from django.urls import path
from django.contrib import admin
from kblog import views
from django.contrib.staticfiles.views import serve
from django.views.generic.base import RedirectView

urlpatterns = [
    # 首页
    path('', views.index, name='index'),
    # 文章详情页
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    # 分类和标签页
    path('category_tag/', views.category_tag, name='category_tag'),
    # 文章分类详情页
    path('article_category/(?P<id>[0-9]+)$', views.article_category, name='article_category'),
    # 文章标签详情页
    path('article_tag/<int:id>', views.article_tag, name='article_tag'),
    # 关于
    path('about/', views.about, name='about'),
    # 登录
    path('admin/', admin.site.urls,name='login'),
    # 搜索
    path('search/',views.search,name='search'),
    # 注册
    path('register/',views.register,name='register')
]

# mkeditor配置
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
