# urls.py 配置网站项目的URL路由规则
from django.contrib import admin
from django.urls import path, include
from kblog import views   # 导入子应用kblog中的views视图层
from django.contrib.staticfiles.views import serve
from django.views.generic.base import RedirectView


# URL 模式 路由规则
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kblog.urls')),
    path('mdeditor/', include('mdeditor.urls')),
]
