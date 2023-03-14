#注册——将后台数据模型进行注册 显示到管理页面
from django.contrib import admin
from .models import Article, Category, Tag, Site, Notice, Valine, About, Skill
from import_export.admin import ImportExportModelAdmin
from django.db import models

# 修改后台管理页面头部显示内容和后台名称
admin.site.site_header = 'KylinBlog后台管理系统'
admin.site.site_title = 'KylinBlog | 后台'


# 在admin视图管理中注册kblog应用中的所有视图界面  装饰器

# 文章视图注册 装饰器
@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin):
    # 设置要显示在后台列表中的字段
    list_display = (
        'add_time', 'title', 'cover_preview', 'category', 'show_tag', 'is_recommend', 'click_count', 'update_time')
    list_per_page = 10  # 设置每页显示多少条记录，默认是100条
    list_editable = ['category', 'is_recommend']  # 设置默认可编辑字段，在列表里就可以编辑
    ordering = ('-add_time', 'is_recommend')  # 设置默认排序字段，负号表示降序排序
    list_display_links = ('title',)  # 设置哪些字段可以点击进入编辑界面
    search_fields = ('title', 'desc', 'content')  # 置哪些字段可以查询
    list_filter = ('title', 'add_time')  # 过滤器，按字段进行筛选
    date_hierarchy = 'add_time'  # 详细时间分层筛选　
    readonly_fields = ('cover_preview',)  # 只读字段，添加该字段才能在后台预览封面，否则报错
    fieldsets = (  # 后台文章编辑页面排版
        ('编辑文章', {
            'fields': ('title', 'author', 'cover', 'cover_preview', 'desc', 'content')
        }),
        ('其他设置', {
            'classes': ('collapse',),
            'fields': ('is_recommend', 'category', 'tag', 'add_time'),
        }),
    )

    # 在后台显示文章的所有tag标签
    def show_tag(self, obj):
        return [tags.name for tags in obj.tag.all()]

    show_tag.short_description = '标签'


# 分类视图注册

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'add_menu', 'get_items', 'icon', 'icon_data']
    list_editable = ['add_menu', 'icon']
    search_fields = ('name',)
    list_display_links = ('name',)  # 设置哪些字段可以点击进入编辑界面


# 标签
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_items']
    search_fields = ('name',)


# 公告栏
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'icon', 'icon_data']
    list_editable = ['icon']


# 网站设置
@admin.register(Site)
class SiteAdmin(ImportExportModelAdmin):
    list_display = ['site_name', 'logo_preview', 'keywords', 'desc', 'slogan', 'dynamic_slogan', 'bgcover_preview']


from django.forms import PasswordInput


# valine评论
@admin.register(Valine)
class ValineAdmin(admin.ModelAdmin):
    list_display = ['appid', 'appkey', 'avatar', 'pagesize', 'placeholder']


# 关于
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['avatar_admin', 'career', 'introduction', 'skill_title']
    list_display_links = ('career',)


# 技能
@admin.register(Skill)
class SocialAdmin(admin.ModelAdmin):
    list_display = ['skill_name', 'skill_precent']
