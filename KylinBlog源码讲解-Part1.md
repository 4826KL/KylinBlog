# KylinBlog源码讲解-Part1

# 数据库模型的设计与建立

## models.py

- models.py是DjangoMVC设计模式中最为关键的“M”层面，实现了与数据库的模型交互以及数据表的设计建立
- 上层APP_NAME为`kblog`，因此所创建的数据表的前缀名称为`kblog_`
- 全部源码置于文后
- ![image-20221201081236242](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201081236242.png)
- ![image-20221201085353930](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085353930.png)

## 文章分类模型Category

- 对应数据表-kblog_Category
- 实现了文章分类这一功能

```python
class Category(models.Model):
    '''文章分类'''
    name = models.CharField(max_length=20, verbose_name='分类名称')
    index = models.IntegerField(default=1, verbose_name='分类排序')
    add_menu = models.BooleanField(default=False, verbose_name='添加到导航栏')
    icon = models.CharField(max_length=30, default='fas fa-home', verbose_name='导航图标')

    class Meta:
        verbose_name_plural = verbose_name = '分类'

    # 统计分类对应文章数,并放入后台
    def get_items(self):
        return len(self.article_set.all())

    get_items.short_description = '文章数'  # 设置后台显示表头

    # 后台图标预览
    def icon_data(self):  # 引入Font Awesome Free 5.11.1
        return format_html('<h1><i class="{}"></i></h1>', self.icon)  # 转化为<i class="{self.icon}"></i>

    icon_data.short_description = '图标预览'

    def __str__(self):
        return self.name
```

- 各有实际意义字段解释如下：
  - `name`:分类名称
  - `index`:分类排序
- 定义了统计函数`get_items()`和后台图标预览规格化HTML函数`icon_data()`
- ![image-20221201081957097](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201081957097.png)

![image-20221201085733431](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085733431.png)

![image-20221201085749544](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085749544.png)

## 文章标签模型Tag

- 对应 `kblog_tag`数据表

- ```python
  class Tag(models.Model):
      '''标签'''
      name = models.CharField(max_length=20, verbose_name='标签名称')
  
      class Meta:
          verbose_name = '标签'
          verbose_name_plural = verbose_name
  
      # 统计分类对应文章数,并放入后台
      def get_items(self):
          return len(self.article_set.all())
  
      get_items.short_description = '文章数'  # 设置后台显示表头
  
      def __str__(self):
          return self.name
  ```

- 只有一个字段 `name`-标签名称

- 实现了统计分类对应文章数函数`get_items()`

- ![image-20221201082238856](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201082238856.png)

![image-20221201085759849](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085759849.png)

## 文章模型Article

- 对应`kblog_article`数据表

- ```python
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

- `title`：文章标题 CharField

- `author`：文章作者 默认值为李欢欢 CharField

- `desc`：文章描述 CharField

- `cover`：文章封面 URLField预览

- `content`：文章详细内容 MDTextField 实现Markdown编写模式

- `click_count`：文章阅读量 活跃整型字段

- `is_recommend`是否为推荐文章 BooleanField

- `add_time`:文章创建时间 DateTimeField 默认取值为datetime.now

- `update_time`：文章最后更新时间

- `category`：文章对应分类名称 ForeignKey 对应 `kblog_category`

- `tag`:文章对应标签名称 ManyToManyField多对多字段 对应  `kblog_tag`

- ![image-20221201083131730](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201083131730.png)

![image-20221201085813412](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085813412.png)

## 公告栏目Notice

- 对应`kblog_notice`数据表

- ```python
  class Notice(models.Model):
      '''公告栏'''
      title = models.CharField(max_length=30, verbose_name='公告栏标题')
      content = models.TextField(max_length=500, verbose_name='公告内容')
      icon = models.CharField(default='far fa-lightbulb', max_length=50, verbose_name='公告图标')
  
      class Meta:
          verbose_name = verbose_name_plural = '公告栏'
  
      def icon_data(self):
          return format_html('<h1><i class="{}"></i></h1>', self.icon)  # 转化为<i class="{self.icon}"></i>
  
      icon_data.short_description = '图标预览'
  
      def __str__(self):
          return self.title
  ```

- `title`:公告栏标题 CharField

- `content`：公告内容 TextField

- `icon`：公告图标 CharField

- ![image-20221201083325725](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201083325725.png)

![image-20221201085828246](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085828246.png)

## 文章评论模型Valine

- 对应`kblog_valine`数据表

- 文章评论的功能通过使用`Valine`富文本评论库实现

- ![image-20221201083637720](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201083637720.png)

- ```python
  class Valine(models.Model):
      '''valine评论'''
      appid = models.CharField(max_length=100, verbose_name='appId')
      appkey = models.CharField(max_length=100, verbose_name='appKey')
      avatar = models.CharField(default='', blank=True, max_length=100, verbose_name='avatar')
      pagesize = models.IntegerField(default='10', verbose_name='pageSize')
      placeholder = models.CharField(max_length=100, verbose_name='placeholder')
  
      class Meta:
          verbose_name = 'valine评论'
          verbose_name_plural = verbose_name
  ```

- 分别对应配置申请好的`appid`和`appkey`

- ![image-20221201083733494](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201083733494.png)

- ![image-20221201085837433](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085837433.png)

​	

## 个人介绍模型About

```python
class About(models.Model):
    '''关于'''
    avatar = models.URLField(verbose_name='头像')
    career = models.CharField(max_length=50, verbose_name='事业')
    introduction = models.TextField(verbose_name='介绍')
    skill_title = models.CharField(default='技能', max_length=50, verbose_name='技能标题')

    class Meta:
        verbose_name_plural = verbose_name = '关于'

    def avatar_admin(self):
        return format_html('<img src="{}" width="50px" height="50px" style="border-radius: 50%;" />', self.avatar, )

    avatar_admin.short_description = '头像预览'
```

![image-20221201083854994](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201083854994.png)

![image-20221201085849050](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085849050.png)

## 技能模型Skill

```python
class Skill(models.Model):
    """关于页技能"""
    skill_name = models.CharField(max_length=50, verbose_name='方向名')
    skill_precent = models.CharField(default='%', max_length=50, verbose_name='百分比')

    class Meta:
        verbose_name_plural = verbose_name = '技能'

    # 后台图标预览
    def icon_data(self):
        return format_html('<h1><i class="{}"></i></h1>', self.social_icon)

    icon_data.short_description = '图标预览'
```

![image-20221201083904807](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201083904807.png)

![image-20221201085939574](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085939574.png)

![image-20221201085933221](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085933221.png)

## 站点页面配置Site

```python
class Site(models.Model):
    """站点配置"""
    site_name = models.CharField(default='KylinBlog', max_length=30, verbose_name='网站名字')
    keywords = models.CharField(default='KeyWord', max_length=50, verbose_name='网站关键词')
    logo = models.URLField(default='https://jwt1399.top/favicon.png', max_length=100, verbose_name='网站logo')
    desc = models.CharField(max_length=50, verbose_name='网站描述')
    slogan = models.CharField(max_length=50, verbose_name='网站标语')
    dynamic_slogan = models.CharField(max_length=50, verbose_name='动态标语')
    bg_cover = models.URLField(default='http://119.23.243.154/image/Covteam-hack.jpg', max_length=100,
                               verbose_name='背景图片')

    class Meta:
        verbose_name = '网站设置'
        verbose_name_plural = verbose_name

    def logo_preview(self):  # logo预览
        return format_html('<img src="{}" width="40px" height="40px" alt="logo" />', self.logo)

    logo_preview.short_description = 'logo预览'

    def bgcover_preview(self):  # 背景图片预览
        return format_html('<img src="{}" width="100px" height="80px" alt="bgcover" />', self.bg_cover)

    bgcover_preview.short_description = '首页背景预览'

    def __str__(self):
        return self.site_name
```

![image-20221201090007013](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201090007013.png)

![image-20221201085948703](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221201085948703.png)

# ER图

![Diagram 1](https://happygoing.oss-cn-beijing.aliyuncs.com/img/Diagram 1.png)

# 完整源码

```python
from django.db import models
from datetime import datetime
from django.utils.html import format_html
from mdeditor.fields import MDTextField

# Create your models here.

'''
文章分类模型 Category
'''


class Category(models.Model):
    '''文章分类'''
    name = models.CharField(max_length=20, verbose_name='分类名称')
    index = models.IntegerField(default=1, verbose_name='分类排序')
    add_menu = models.BooleanField(default=False, verbose_name='添加到导航栏')
    icon = models.CharField(max_length=30, default='fas fa-home', verbose_name='导航图标')

    class Meta:
        verbose_name_plural = verbose_name = '分类'

    # 统计分类对应文章数,并放入后台
    def get_items(self):
        return len(self.article_set.all())

    get_items.short_description = '文章数'  # 设置后台显示表头

    # 后台图标预览
    def icon_data(self):  # 引入Font Awesome Free 5.11.1
        return format_html('<h1><i class="{}"></i></h1>', self.icon)  # 转化为<i class="{self.icon}"></i>

    icon_data.short_description = '图标预览'

    def __str__(self):
        return self.name


'''
文章标签模型
'''


class Tag(models.Model):
    '''标签'''
    name = models.CharField(max_length=20, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    # 统计分类对应文章数,并放入后台
    def get_items(self):
        return len(self.article_set.all())

    get_items.short_description = '文章数'  # 设置后台显示表头

    def __str__(self):
        return self.name


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


'''
公告栏目
'''


class Notice(models.Model):
    '''公告栏'''
    title = models.CharField(max_length=30, verbose_name='公告栏标题')
    content = models.TextField(max_length=500, verbose_name='公告内容')
    icon = models.CharField(default='far fa-lightbulb', max_length=50, verbose_name='公告图标')

    class Meta:
        verbose_name = verbose_name_plural = '公告栏'

    def icon_data(self):
        return format_html('<h1><i class="{}"></i></h1>', self.icon)  # 转化为<i class="{self.icon}"></i>

    icon_data.short_description = '图标预览'

    def __str__(self):
        return self.title


'''
评论模型  使用valine系统框架
'''

# 评论模型的实现  使用valine系统调度完成
# 在后台配置Valine的appkey和appid

class Valine(models.Model):
    '''valine评论'''
    appid = models.CharField(max_length=100, verbose_name='appId')
    appkey = models.CharField(max_length=100, verbose_name='appKey')
    avatar = models.CharField(default='', blank=True, max_length=100, verbose_name='avatar')
    pagesize = models.IntegerField(default='10', verbose_name='pageSize')
    placeholder = models.CharField(max_length=100, verbose_name='placeholder')

    class Meta:
        verbose_name = 'valine评论'
        verbose_name_plural = verbose_name


'''
作者介绍
'''


class About(models.Model):
    '''关于'''
    avatar = models.URLField(verbose_name='头像')
    career = models.CharField(max_length=50, verbose_name='事业')
    introduction = models.TextField(verbose_name='介绍')
    skill_title = models.CharField(default='技能', max_length=50, verbose_name='技能标题')

    class Meta:
        verbose_name_plural = verbose_name = '关于'

    def avatar_admin(self):
        return format_html('<img src="{}" width="50px" height="50px" style="border-radius: 50%;" />', self.avatar, )

    avatar_admin.short_description = '头像预览'


'''
技能模型
'''


class Skill(models.Model):
    """关于页技能"""
    skill_name = models.CharField(max_length=50, verbose_name='方向名')
    skill_precent = models.CharField(default='%', max_length=50, verbose_name='百分比')

    class Meta:
        verbose_name_plural = verbose_name = '技能'

    # 后台图标预览
    def icon_data(self):
        return format_html('<h1><i class="{}"></i></h1>', self.social_icon)

    icon_data.short_description = '图标预览'


'''
站点页面配置数据表模型
'''


class Site(models.Model):
    """站点配置"""
    site_name = models.CharField(default='KylinBlog', max_length=30, verbose_name='网站名字')
    keywords = models.CharField(default='KeyWord', max_length=50, verbose_name='网站关键词')
    logo = models.URLField(default='https://jwt1399.top/favicon.png', max_length=100, verbose_name='网站logo')
    desc = models.CharField(max_length=50, verbose_name='网站描述')
    slogan = models.CharField(max_length=50, verbose_name='网站标语')
    dynamic_slogan = models.CharField(max_length=50, verbose_name='动态标语')
    bg_cover = models.URLField(default='http://119.23.243.154/image/Covteam-hack.jpg', max_length=100,
                               verbose_name='背景图片')

    class Meta:
        verbose_name = '网站设置'
        verbose_name_plural = verbose_name

    def logo_preview(self):  # logo预览
        return format_html('<img src="{}" width="40px" height="40px" alt="logo" />', self.logo)

    logo_preview.short_description = 'logo预览'

    def bgcover_preview(self):  # 背景图片预览
        return format_html('<img src="{}" width="100px" height="80px" alt="bgcover" />', self.bg_cover)

    bgcover_preview.short_description = '首页背景预览'

    def __str__(self):
        return self.site_name

```

