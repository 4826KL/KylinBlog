# 本项目的全局配置文件
# 配置了项目中间插件（MD编辑器）、数据库参数配置、安装的app（kblog）、前台（用户浏览端）、后台admin（管理员操控数据端）参数配置

from pathlib import Path  # 路径库
import os  # 操作系统库 用于读取本机相关参数 比如操作系统版本

# 配置静态文件（样式文件、前端HTML文件、静态图片文件）  此句为Django默认配置好的
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 项目全球唯一的key 类似于个人的身份证号
SECRET_KEY = 'django-insecure-m25qfdfqgjplf8vux4z9y!r7kselu01dkxjysy-u@=8!s^-8zi'

# 是否开启Debug模式 如果开启的话 浏览过程中遇到错误会直接显示 关闭的话则会报错误 502bad gateway
DEBUG = True

ALLOWED_HOSTS = ['*']

# 安装的子app

INSTALLED_APPS = [
    'simpleui',  # 后台管理框架
    'django.contrib.admin',  # django自带管理框架
    'django.contrib.auth',  # django自带权限体系  用于区分前后台（用户、管理员、查看/操作CURD数据）
    'django.contrib.contenttypes',  # django自带内容类型 囊括各个字段 CharField
    'django.contrib.sessions',  # django自带会话层  存储用户状态（比如是否处于已经登录状态（
    'django.contrib.messages',  # django自带消息机制 类似于QT的消息-槽函数机制 前台给后台发送请求，后台反馈响应对应数据给前台
    'django.contrib.staticfiles',  # django自带静态文件管理体系
    'kblog.apps.KblogConfig',  # 博客应用 kblog
    'mdeditor',   # MD编辑器 MD Editor
    'import_export',  # 导入导出包（类似头文件）
    'django_extensions'  # django自带额外插件
]

# Django自带默认中间层配置 与上文INSTALLED_APPS相呼应 此处为默认 未进行更改
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'KylinBlog.urls'  # 根URL对应参数配置 此处为全局的URL路由配置

# 前端HTML文件模板 此处为Django默认配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'kblog.views.global_params',  # 自定义全局变量
            ],
        },
    },
]

WSGI_APPLICATION = 'KylinBlog.wsgi.application'  # 对应响应asgi.py

# 配置数据库引擎及用户密码等参数
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 引擎 -MySQL
        'NAME': 'kylina',  #数据库名-kylina
        'USER': 'root',   # 用户名
        'PASSWORD': 'Huan482670',  # 用户密码
        'HOST': '127.0.0.1',  # 服务器主机地址（本地回环localhost）
        'PORT': '3306',  # 端口号 MySQL默认端口号即为3306
        'OPTIONS': {'charset': 'utf8mb4'},  # 额外可选项 字符集-utf8mb4 支持中文及emoji
    }
}


# 密码验证机制 Django自带默认 未修改
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化配置 配置时区、语言
LANGUAGE_CODE ='zh-hans'
TIME_ZONE ='Asia/Shanghai'
USE_I18N =True #默认
USE_L10N =True #默认
USE_TZ =False #默认

# 日期格式
DATETIME_FORMAT = 'Y-m-d'

# Static files (CSS, JavaScript, Images) 静态文件本地相对路径
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

# SimpleUi后台设置 配置后台页面样式及规格
SIMPLEUI_LOGO = 'https://i.loli.net/2020/04/23/jGP8gQOYW75TSJp.png'  # 登录页和后台logo
SIMPLEUI_ANALYSIS = False  # 是否向SimpleUi收集分析信息
SIMPLEUI_LOADING = False  # 是否打开Loading遮罩层
SIMPLEUI_LOGIN_PARTICLES = True  # 登录页粒子动画
SIMPLEUI_STATIC_OFFLINE = True  # 是否以脱机模式加载静态资源，为True的时候将默认从本地读取所有资源，即使没有联网一样可以。适合内网项目，不填该项或者为False的时候，默认从第三方的cdn获取
SIMPLEUI_HOME_INFO = False  # 是否打开SimpleUi服务器信息
SIMPLEUI_DEFAULT_THEME = 'simpleui.css'  # 默认主题 https://simpleui.88cto.com/docs/simpleui/QUICK.html#%E9%BB%98%E8%AE%A4%E4%B8%BB%E9%A2%98
SIMPLEUI_HOME_QUICK = True  # 后台页面是否显示最近动作
# 自定义后台菜单
SIMPLEUI_CONFIG = {
    'system_keep': False,  # 去除系统模块
    'menus': [{
        'name': '文章管理',
        'icon': 'fas fa-book-open',
        'models': [{
            'name': '文章',
            'icon': 'fas fa-book-open',
            'url': '/admin/kblog/article/'
        }, {
            'name': '分类',
            'icon': 'fas fa-list',
            'url': '/admin/kblog/category/'
        }, {
            'name': '标签',
            'icon': 'fas fa-tags',
            'url': '/admin/kblog/tag/'
        }]
    }, {
        'name': '公告栏',
        'icon': 'fas fa-bullhorn',
        'url': '/admin/kblog/notice/'
    }, {
        'name': '关于设置',
        'icon': 'fas fa-address-card',
        'models': [{
            'name': '基本信息',
            'icon': 'far fa-file',
            'url': '/admin/kblog/about/'
        },{
            'name': '技能',
            'icon': 'fas fa-drafting-compass',
            'url': '/admin/kblog/skill/'
        }]
    }, {
        'name': '网站设置',
        'icon': 'fas fa-globe-americas',
        'url': '/admin/kblog/site/'
    }, {
        'name': 'valine评论',
        'icon': 'far fa-comments',
        'url': '/admin/kblog/valine/'
    }, {
        'app': 'auth',
        'name': '用户和授权',
        'icon': 'fas fa-user-shield',
        'models': [{
            'name': '用户',
            'icon': 'fa fa-user',
            'url': 'auth/user/'
        }, {
            'name': '权限组',
            'icon': 'fas fa-users-cog',
            'url': 'auth/group/'
        }]
    }, {
        'name': '网页预览',
        'icon': 'fas fa-paper-plane',
        'models': [{
            'name': 'HappyGoing',
            'url': 'https://www.happygoing.cc',
            'icon': 'fab fa-wolf-pack-battalion'
        }]
    }]
}

# mdeditor设置 配置MD编辑器
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'  # 你上传的文件和图片会默认存在/uploads/editor下
X_FRAME_OPTIONS = 'SAMEORIGIN'

# 日志记录_最近动作
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'mysite.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'blog': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # 默认排序方式 Django3.0版本后新增
