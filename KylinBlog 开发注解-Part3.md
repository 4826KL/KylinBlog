# KylinBlog 开发注解-Part3

## DJango中的ORM数据CURD接口

- Django中前台的表单数据是如何提交到后台呈现的？
- Django中前端页面所展示的数据是如何从后台获取的？

Django的对象关系映射系统(Object-Relational Mapper, ORM)提供了丰富的数据查询接口, 

无需使用原生SQL语句即可通过对模型的简单操作实现对数据库里的数据进行增删改查。

查询得到的结果叫查询集(QuerySet), 所以这个接口被称为QuerySet API。

以一个简要的Article模型为例来讲解，这里之讲解最基础的CURD方法

## 示例模型

```python
from django.db import models

class Article(models.Model):
    title = models.CharField('标题', max_length=200, unique=True)
    body = models.TextField('正文')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

## 增

对于新增数据，Django提供了 `save()`和 `create()`两种方法

### save()

```python
from .models import Article

article = Article(title="My first article", body="My first article body")
article.save()
```

注意，调用完Article（）方法后必须使用.save()，否则记录不会被添加到数据库中

### create()

```python
article = Article.objects.create(title="My first article", body="My first article body")
```

## 删

删即从数据表中删除一个已有条目。Django也允许同时删除一条或多条数据。

### 删除单条数据

```python
# 删除第5篇文章
Article.objects.get(pk=5).delete() 
```

### 删除部分数据

```python
# 删除标题含有python的文章
Article.objects.filter(title__icontains="python").delete() 
```

### 删除所有数据

```python
# 慎用
Article.objects.all().delete() 
```

## 查

查主要使用get, filter及exclude方法，而且这些方法是可以联用的。

### 查询所有数据

```python
# QuerySet类型，实例对象列表
Article.objects.all() 
# 字典列表
Article.objects.all().values() 
# 只获取title-字典形式
Article.objects.all().values('title') 
# 只获取title列表- 元组形式，只有value，没有key
Article.objects.all().values_list('title')
# 只获取title列表，只有value
Article.objects.all().values_list('title', flat=True)
```

### 查询单条数据

```python
article = Article.objects.get(id=11)
```

当上述查询有个问题，如果id不存在，会抛出错误。还有一种方式是使用`filter`方法, 这样即使id不存在也不会报错。

```python
article = Article.objects.filter(id=1).first()
```

一个更好的方式是使用Django提供的`get_object_or_404`方法，如下所示：

```python
from django.shortcuts import get_object_or_404 
article = get_object_or_404(Article, pk=1) 
```

### 查询多条数据

**按大于、小于及不等于查询**

```python
# gte：大于等于，lte：小于等于
articles = Article.objects.filter(id__gte=2).filter(id__lte=11)
# 不等于
articles = Article.objects.exclude(id=10)
```

**按范围查询**

```python
# 按范围查询，in或者range
articles = Article.objects.filter(id__range=[2, 11])
articles = Article.objects.filter(id__in=[3, 6,9])
```

## 改

改既可以用save方法，也可以用update方法。

其区别在于save方法不仅可以更新数据中现有对象数据，还可以创建新的对象。

而update方法只能用于更新已有对象数据。

一般来说，如果要同时更新多个对象数据，用update方法或bulk_update方法更合适。

### save方法

```python
article = Article.objects.get(id=1)
article.title = "New article title"
article.save()
```

### update方法更新单篇文章

```python
article = Article.objects.get(id=1).update(title='new title')
```

### update方法同时更新多篇文章

```python
# 更新所有文章标题
article = Article.objects.filter(title__icontains='python').update(title='Django')
```

## 实例演示

![image-20221127150344118](https://happygoing.oss-cn-beijing.aliyuncs.com/img/image-20221127150344118.png)