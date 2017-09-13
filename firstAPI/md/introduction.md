# 初识Django—Python API接口编程入门

## 一、WEB架构的简单介绍
Django是什么？

Django是一个开放源代码的Web应用框架，由Python写成。我们的目标是用Python语言，基于Django框架，利用MVC模型，实现后台方面的针对数据库的API开发。先了解一下互联网的WEB架构，
![](https://oss.aliyuncs.com/yqfiles/d27e41fff3633e18ac653d96da08ef6b44a517a9.jpeg)

如上图：

互联网的WEB架构大致分为三层，web层、app层和数据库层。Web层：如apache网站服务器；app层主要是应用业务；DB指后台数据库。随着互联网的高速发展，网站访问量的增长、数据的累积、负载的过高，应用和数据库的设计也面临了更多的挑战。业务的拆分、数据库的切分已不是什么新名词。为了方便日后系统的平滑扩展，我们在系统设计的时候就需要规划好APP业务实现模式。在这里，我们设计的APP也分为前台和后台，前台主要是展现，如界面、FORM等，后台为API接口，用来联系前台界面和数据库的交互，本文只涉及到APP设计中的后台API接口设计和用Python实现的部分。

当然一个项目的开发离不开团队的合作，我们用GitLab来做开发代码的版本管理，关于git的安装和使用本文不以说明。

## 二、开发环境搭建
1、安装Python2.8

2、安装Django模块

3、Python开发编辑器PyCharm

有了以上环境，我们就可以开工了，数据库可以直接用Sqlite，如果用mysql的话要安装mysqldb模块。


## 三、模块设计要求
新人报道，先到项目组领个接口开发任务吧。

项目组分配任务：完成XX数据模型的接口设计

涉及到的表有：XX_TAB

涉及到的API接口有：

1、list，获取XX_TAB表数据，传入参数XX_ID，从数据库中列出XX_ID相同的行。

2、add，删除XX_TAB表一行数据，传入PK_ID、XX_ID

3、update，更新XX_TAB表一行数据，传入PK_ID、XX_ID

4、delete，删除XX_TAB表一行数据，传入PK_ID、XX_ID

说白了就是在应用层实现对XX_TAB标的查询和增删改操作，以用于前台APP的调用，前台APP不直接针对数据库做任何操作，由调用API接口来实现对数据库的查询、增删改。这样设计的目的是降低业务模块间的耦合性，提高APP和数据库的灵活性，便于以后业务的升级变更，也是考虑到今后数据库数据量的增长而便于数据库的拆分和平滑扩展。

## 四、实际开发
### 1、Django基本格式介绍
前面已经说过，我们是团队开发的，先将同学们在git上已写得代码pull下来，第一次下载代码，我是用git clone的命令复制到本地的，如下：

git clone http://git.xxx.cn/xxxtest/xxx.git

cd xxxtest  #cd到项目目录下

python manage.py runserver 127.0.0.1:8000  #启动项目

注意：我是用git下载的代码，不是自己新建的project。如果同学们是新建项目的话，还需按部就班从django-admin.py startproject [project_name]开始。

创建完项目后，Django框架会自动生成一些文件和文件夹，注意settings.py文件，关于数据库设置处，默认如下代码：
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
在命令行下运行python manage.py runserver命令后，在项目文件下会自动生成一个db.sqlite3数据文件，Django默认数据库为sqlite，可改成MySQL、Oracle、PG等，具体设置如MySQL如下：
```

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'test',

        'USER': 'test',

        'PASSWORD': 'test123',

        'HOST':'localhost',

        'PORT':'3306',

    }

}
```
了解了数据库的配置，我们还需要了解一下项目目录下的主要几个文件：

- PROJECT_NAME: 项目的容器。

- manage.py: 一个实用的命令行工具，可让你以各种方式与该 Django 项目进行交互。

- [PROJECT_NAME]/__init__.py: 一个空文件，告诉 Python 该目录是一个 Python 包。

- [PROJECT_NAME]/settings.py: 该 Django 项目的设置/配置。

- [PROJECT_NAME]/urls.py: 该 Django 项目的 URL 声明; 一份由 Django 驱动的网站"目录"。

- [PROJECT_NAME]/wsgi.py: 一个 WSGI 兼容的 Web 服务器的入口，以便运行你的项目。

上面是每个项目的通用介绍，回到实际的开发中来。
### 2、新建app和表定义
我们现在已经有了项目，我要做的是某个表的api接口，于是我在项目下新建了一个app，新建app用以下命令：

django-admin startapp  xx_tab

这样我们就新建了一个xx_tab命名的app，我们要做一些修改：

#### 1、还是打开settings.py文件，找到INSTALLED_APPS参数，在最后面加入xx_tab的app名，如下：
```
INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    'rest_framework_swagger',

    'rest_framework',

    'rest_framework_jwt',

    'xx_tab’,

]
```

#### 2、修改xx_tab目录下得而models.py文件，定义我们需要建的表
```
# Create your models here.
class Xx_Tab(models.Model):

    pk_id = models.AutoField(primary_key=True)

    xx_id = models.IntegerField()

    xx_name = models.CharField(max_length=200)
```
####  3、修改url
完成数据库表的定义后，考虑到使用http来访问数据库的，那就离不开http的url地址。前面在文件介绍中说过用django-admin.py startproject [project_name]命令生成项目后，在项目层目录下会有url的python文件，在每个项目下用django-admin startapp  xx_tab命令生成的app中也会有url的python文件，url好比是网站网页的目录，是用来在web界面上访问的地址。一般，url会对于view，view好比是网页，url指向view。

项目rul、app rul和app view之间的调用关系，如下图：
![](https://oss.aliyuncs.com/yqfiles/cae1c916053e3adf13ceb821d2e9e8f228639ccd.jpeg)

Project rul格式：
```

# 几个测试接口
router = routers.DefaultRouter()

urlpatterns = [
url('^hello/$', hello),

url('^simple/$', Simple.as_view()),

url( r'/log/', include(xx_tab.urls')),
]
```

App rul格式
```

urlpatterns = [

    url(r'list/$', views.get_xx_tabs,),

    url(r'detail/([0-9]+)$', views.get_xx_tab),

    url(r'delete/([0-9]+)$', views.delete_xx_tab),

    url(r'update/([0-9]+)$', views.update_xx_tab),

    url(r'add/$', views.add_xx_tab),

]
```


以上是两层url调用举例：

url在浏览器中的完整写法应该如下：

http://127.0.0.1/xx_tab/list/?xx_id=1

### 4、用Django生成数据库中的表
完成了在Django框架models.py文件中定义了xx_tab表的相关信息，我们就可以用django命令来生成表。

python manage.py makemigrations xx_tab

注意：xx_tab是app名，此命令会在xx_tab app下migrations目录下生成一个0001_initial.py文件，此文件定义了建表信息，如果发现表定义有问题，在修改models.py中的定义后，需要删除0001_initial.py文件，重跑python manage.py makemigrations xx_tab，重新生成0001_initial.py。

执行python manage.py migrate xx_tab，在数据库中生成xx_tab表。

打开Sqlite数据库，在windows下可用

d:\dt\sqlite\sqlite3.exe db.sqlite3 打开当前的数据库，sqlite3.exe可在网上下载。

.table可查看当前的表。

.schema tab_name 可查看表结构定义。
### 5、API接口，实现ADD单行数据
我们要模拟从前台发出一个get或post请求，调用要写的api接口实现插入数据库的功能，

如下界面，模拟前台调用
![](https://oss.aliyuncs.com/yqfiles/7955079d429c22c3e050aacea0de733d9c8bc0d7.jpeg)

上面是一个插入演示页面，post相关表字段值，完成对数据库的一行数据插入。

完成这已插入过程的逻辑关系如下：

View.py主要是接收前台post过来的数据，并在完成处理、存储后返回相关信息。

Service.py主要处理数据，格式化数据

数据库接口层主要处理对数据库的数据存储和访问。

view.py

开头，以下这几行是必不可少的
```
# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
```
因为在urls.py中我们定义的是url(r'add/$', views.add_xx_tab)

add指向views.add_xx_tab

所以我们在views中需要定义add_xx_tab函数

```
@api_view(['POST', 'GET'])
def xx_tab_add(request, *args):
          #1、接收request数据
 #2、处理数据

#3、返回结果
```

基于django rest_framework，在处理client http request时需要用到@api_view修饰。

同时，我们也需要弄清楚对于从client端GET或POST过来的数据我们怎么处理。
1、接收request数据
```
if request.method == 'GET':

    do_something()

elif request.method == 'POST':

    do_something_else()
```
如果是GET，需要处理request .query_params；如果是post需要处理request .data
```
if request.method == 'GET':

for k in request .query_params:

   dict[k] = request .query_params[k]

return dict

elif request.method == 'POST':

for k in request.data

dict[k] = request .data [k]

return dict
```
2、处理数据

首先要判断get或post过来的数据是否满足我们的要求，例如缺少字段、类型错误等。

如果数据没有问题，再存入数据库。

主要是对上面dict的处理，主要都是python语句实现，不涉及Django，此处省略。

逻辑过程：

1、判断传入的request是否缺少相应的字段

2、判断传入的request是否有类型错误

方法：

例如雇员表，add一行需要有以下信息，先定义一个list，用来和传入数据作对比即可

emp = ["empno:int","ename:str","job:str","mgr:int","hiredate:str","sal:int",

"comm:int","deptno:int"]

如果

#3、返回结果

直接返回插入成功即可。