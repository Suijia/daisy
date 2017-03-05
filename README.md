# 服务名称: daisy
[网站地址](http://pudding.space)

[意见反馈](http://pudding.space/feedback)

一个科幻迷收藏私货的地方

## 发布方法

sh script/deploy_remote.sh online


## 查看网站数据

[点击查看](http://new.cnzz.com/v1/login.php?siteid=1260133967)
查看密码：pudding

## 安装依赖
~~~shell
sudo yum install python-devel
sudo yum install gcc
pip install tornado
pip install torndb
pip install MySQL-python
pip install pytz

yum install libxslt-devel libxml2-deve
pip install lxml

pip install apscheduler
~~~

## 安装 mysql
~~~shell
brew install mysql
export PATH=$PATH:/usr/local/mysql/bin
pip install MySQL-Python
~~~
可能需要执行

~~~
sudo install_name_tool -change libmysqlclient.18.dylib /usr/local/mysql/lib/libmysqlclient.18.dylib /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/_mysql.so

requests https
pip install pyopenssl ndg-httpsclient pyasn1
~~~


