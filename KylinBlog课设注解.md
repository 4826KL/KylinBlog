# 基于Django与MySQL的博客管理系统

# STEP1：说项目名称并演示项目

# STEP2：运行项目、项目页面展示

# STEP3：文章详情、归类（雷达图）、

# 自我介绍、后台登录

# STEP4：添加新文章、级联删除展示

# STEP5：讲解代码（MVC）

## 技术框架

- 前端UI：BootStrap4（响应式设计）、JQuery（动效支持）、SimpleUI(后台管理页面支持)
- 后端：Django3.0
- 数据库：MySQL8.0（WAMP）

## 体系结构

![image-20221210150739501](https://happygoing.oss-cn-beijing.aliyuncs.com/image-20221210150739501.png)

## 技术讲解

Django使用MVC设计模式

- M-Model-模型-数据库模型-对应`models.py`文件
- V-View-视图-前端用户界面-对应`views.py`文件
- C-Controller-控制器（数据交互）-对应 `urls.py`文件



- 本项目核心为前端用户页面+后台管理界面
- 包含：博客首页、博客归档页（归类、标签整理及对应统计）、个人介绍页面、登录注册页面、文章详情页、评论功能、数据库表的可视化CURD功能
- 本项目使用MDEditor，支持Markdown格式编写博客
- 博客系统一般为个人博客，在课设中为练习数据库和Django相关操作，额外开发了注册登录功能

## Models举例

数据库模型

Django中的数据库数据模型使用类进行实现，models.py中的每一个类对应数据库中的一张数据表，

数据表名为 `app名_类名`，每个类的基类都是django.db.model.Model

编写配置各个字段（CharField小文本字段、MDField文档编辑字段、URLField地址字段等等）

以文章模型举例说明:

```python
'''
文章模型
'''


class Article(models.Model):
    '''文章'''
    title = models.CharField(max_length=50, verbose_name='文章标题')
    author = models.CharField(max_length=10, verbose_name='作者', default='李欢欢', blank=True, null=True)
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    cover = models.URLField(max_length=200, default='https://happygoing.oss-cn-beijing.aliyuncs.com/img/Apartment-rain.png',
                            verbose_name='文章封面')
    content = MDTextField(verbose_name='文章内容')
    click_count = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    # 文章创建时间。参数 default=datetime.now 指定其在创建数据时将默认写入当前的时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name='发布时间')
    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='文章分类', on_delete=models.CASCADE)  # 此处设置为一个文章只能属于一个类
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='文章标签')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)  # 以创建时间倒序排列

    def cover_preview(self):
        return format_html('<img src="{}" width="200px" height="150px"/>', self.cover, )

    cover_preview.short_description = '文章封面预览'

    def __str__(self):
        return self.title  # 将文章标题返回
```

在编写完成数据库模型或者对数据库模型有改动时，需要在项目终端执行以下命令：

```
python manage.py makemigrations  # 识别改动（翻译为sql，并暂存到migrations文件夹中）
python manage.py migrate  # 执行，将改动迁移到settings.py中配置好的对应数据库中
```

## Views举例



Django的视图(view)是处理业务逻辑的核心，它负责处理用户的请求并返回响应数据。

Django提供了两种编写视图的方式：基于函数的视图和基于类的视图。

在KylinBlog的编写过程中，我主要使用的是基于函数的视图。

以注册视图举例：

![image-20221210164804435](https://happygoing.oss-cn-beijing.aliyuncs.com/image-20221210164804435.png)

```python
# 手写注册视图view模型
def register(request):
    if request.method =='POST':   # POST
        user_name = request.POST.get('username', '')
        pass_word_1 = request.POST.get('password_1', '')
        pass_word_2 = request.POST.get('password_2', '')
        if User.objects.filter(username=user_name):
            return render(request, 'register.html', {'error': '用户已存在'})
        if pass_word_1 != pass_word_2:
            return render(request, 'register.html', {'errpr': '两次密码不一致'})
        user = User()
        user.username=user_name
        user.password=make_password(pass_word_1)
        user.is_staff=1
        user.is_superuser=1
        user.is_active=1
        user.save()
        return render(request,'index.html')
    return render(request,'register.html')
```

![image-20221210152016153](https://happygoing.oss-cn-beijing.aliyuncs.com/image-20221210152016153.png)

## Urls.py

**Django的项目文件夹和每个应用(app)目录下都有`urls.py`文件，它们构成了Django的路由配置系统(URLconf)。**

**服务器收到用户请求后，会根据用户请求的url地址和urls.py里配置的url-视图映射关系，去调用执行相应的视图函数或视图类，最后由视图返回给客户端数据。**

```python
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
    # 注册
    path('register/',views.register,name='register')
]
```

## 数据库

![image-20221210165210555](https://happygoing.oss-cn-beijing.aliyuncs.com/image-20221210165210555.png)

![image-20221210165313491](https://happygoing.oss-cn-beijing.aliyuncs.com/image-20221210165313491.png)

![image-20221210165319631](https://happygoing.oss-cn-beijing.aliyuncs.com/image-20221210165319631.png)