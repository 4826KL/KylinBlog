# 激活配置文件 为本项目激活链接settings.py

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KylinBlog.settings')

application = get_asgi_application()
