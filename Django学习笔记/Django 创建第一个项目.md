# Django 管理工具
安装 Django 之后，您现在应该已经有了可用的管理工具 django-admin.py。我们可以使用 django-admin.py 来创建一个项目:
我们可以来看下django-admin.py的命令介绍:
```
[root@solar ~]# django-admin.py
Usage: django-admin.py subcommand [options] [args]

Options:
  -v VERBOSITY, --verbosity=VERBOSITY
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings=SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath=PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on exception
  --version             show program's version number and exit
  -h, --help            show this help message and exit

Type 'django-admin.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[django]
    check
    cleanup
    compilemessages
    createcachetable
……省略部分……
```
# 创建第一个项目
进入代码存放目录，使用 django-admin.py 来创建 HelloWorld 项目：
```
django-admin.py startproject HelloWorld
```
创建完成后我们可以查看下项目的目录结构：
```
$ cd HelloWorld/
$ tree
.
|-- HelloWorld
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
`-- manage.py
```
目录说明：
- HelloWorld: 项目的容器。
- manage.py: 一个实用的命令行工具，可让你以各种方式与该 Django 项目进行交互。
- HelloWorld/__init__.py: 一个空文件，告诉 Python 该目录是一个 Python 包。
- HelloWorld/settings.py: 该 Django 项目的设置/配置。
- HelloWorld/urls.py: 该 Django 项目的 URL 声明; 一份由 Django 驱动的网站"目录"。
- HelloWorld/wsgi.py: 一个 WSGI 兼容的 Web 服务器的入口，以便运行你的项目。

接下来进入 HelloWorld 目录输入以下命令，启动服务器：
```
python manage.py runserver 0.0.0.0:8000
```
0.0.0.0 让其它电脑可连接到开发服务器，8000 为端口号。如果不说明，那么端口号默认为 8000。
在浏览器输入你服务器的ip及端口号，如果正常启动，输出结果如下：

![](http://www.runoob.com/wp-content/uploads/2015/01/8DFE291A-BE29-474F-BE3C-9A88FEBDE916.jpg)

# 视图和 URL 配置
在先前创建的 HelloWorld 目录下的 HelloWorld 目录新建一个 view.py 文件，并输入代码：
```
from django.http import HttpResponse
 
def hello(request):
    return HttpResponse("Hello world ! ")
```
接着，绑定 URL 与视图函数。打开 urls.py 文件，删除原来代码，将以下代码复制粘贴到 urls.py 文件中：
```
from django.conf.urls import url
 
from . import view
 
urlpatterns = [
    url(r'^$', view.hello),
]
```
整个目录结构如下：
```
$ tree
.
|-- HelloWorld
|   |-- __init__.py
|   |-- __init__.pyc
|   |-- settings.py
|   |-- settings.pyc
|   |-- urls.py              # url 配置
|   |-- urls.pyc
|   |-- view.py              # 添加的视图文件
|   |-- view.pyc             # 编译后的视图文件
|   |-- wsgi.py
|   `-- wsgi.pyc
`-- manage.py
```

完成后，启动 Django 开发服务器，并在浏览器访问打开浏览器并访问：
![](http://www.runoob.com/wp-content/uploads/2015/01/BD259D4C-2DBE-4657-8761-D8C3508E8A94.jpg)

我们也可以修改以下规则：
```
from django.conf.urls import url
 
from . import view
 
urlpatterns = [
    url(r'^hello$', view.hello),
]
```
通过浏览器打开 http://127.0.0.1:8000/hello，输出结果如下：
![](http://www.runoob.com/wp-content/uploads/2015/01/344A94C7-8D7D-4A69-9963-00D28A69CD56.jpg)

**注意：**
项目中如果代码有改动，服务器会自动监测代码的改动并自动重新载入，所以如果你已经启动了服务器则不需手动重启。

**url() 函数**
Django url() 可以接收四个参数，分别是两个必选参数：regex、view 和两个可选参数：kwargs、name，接下来详细介绍这四个参数。
- regex: 正则表达式，与之匹配的 URL 会执行对应的第二个参数 view。
- view: 用于执行与正则表达式匹配的 URL 请求。
- kwargs: 视图使用的字典类型的参数。
- name: 用来反向获取 URL。