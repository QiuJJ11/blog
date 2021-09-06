## 华为云-ubuntu18.04 部署指南

### 购买地址

https://www.huaweicloud.com/pricing.html?shareListId=Tv8u38og8Dv8NQaBO8#/ecs

### SSH-工具-FinalShell下载

http://www.hostbuf.com/t/988.html



### apt更换国内源

```shell
mv /etc/apt/sources.list /etc/apt/sourses.list.bak
cd /etc/apt/
vim sources.list

#输入如下内容后保存退出

deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse


最后执行 apt-get update 更新最新源

```



### 系统组件安装

#### nginx 1.14.0 

```shell
sudo apt-get install nginx
安装完毕后 执行 nginx -v 
```

#### mysql-server 5.7 安装

```shell
apt-cache madison mysql-server - 查看mysql在线安装版本
sudo apt-get install mysql-server
安装完毕后 查看 cat /etc/mysql/debian.cnf 
根据文件中的用户名和密码进入mysql

修改root用户密码
1）更新密码和验证方式
   update mysql.user set authentication_string=password('123456'),plugin="mysql_native_password"  where user='root' and Host ='localhost';
2）刷新权限 
   flush privileges;
```

#### redis 4.0.9 安装

```shell
1，下载安装包
wget http://download.redis.io/releases/redis-4.0.9.tar.gz

2，解压
tar zxvf redis-4.0.9.tar.gz

3,安装
cd redis-4.0.9
make
make install

4,修改配置文件
cd redis-4.0.9
vim redis.conf
配置1 - 后台启动
	daemonize  yes
配置2 - 日志
	logfile "/var/log/redis/redis.log"
注意：日志路径需要提前创建 终端 mkdir /var/log/redis

5，复制配置文件
mkdir /etc/redis
cp redis.conf /etc/redis/redis.conf
	
6，配置启动脚本
cp redis-4.0.9/utils/redis_init_script   /etc/init.d/redis-server

```

### Python环境相关

#### pip3安装

**sudo apt-get install python3-pip**

```shell
mkdir ~/.pip
vim ~/.pip/pip.conf
# 然后将下面这两行复制进去
[global]
index-url = https://mirrors.aliyun.com/pypi/simple

国内其他pip源

    清华：https://pypi.tuna.tsinghua.edu.cn/simple
    中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
    华中理工大学：http://pypi.hustunique.com/
    山东理工大学：http://pypi.sdutlinux.org/
    豆瓣：http://pypi.douban.com/simple/
```

#### 第三方py库安装

```shell
pip3 install django==2.2.12
pip3 install django-cors-headers==3.0.2
pip3 install django-redis==4.10.0
pip3 install PyMySQL==0.9.3
pip3 install celery==4.3.0
pip3 install PyJWT==1.7.1
pip3 install uWSGI==2.0.18
pip3 install python-alipay-sdk==2.0.1
pip3 install Pillow
pip3 install gevent
pip3 install psutil

#mysqlclient安装
sudo apt-get install default-libmysqlclient-dev
pip3 install mysqlclient
```



### 前端部署

前端html和静态文件直接交由 nginx 处理

1）修改nginx启动 用户

vim /etc/nginx/nginx.conf

```shell
user root;  #修改nginx启动用户
```

2）修改nginx 80的默认配置

vim /etc/nginx/sites-enabled/default

```shell

root /root/blog_client/templates;   # 指定全局静态路径地址


location /static {

        root /root/blog_client;
}


location / {  # 路由设定
 		
		rewrite ^/(\w+)$  /$1.html break;
 		rewrite ^/(\w+)/info$  /about.html break;
 		rewrite ^/(\w+)/change_info$  /change_info.html break;
 		rewrite ^/(\w+)/topic/release$  /release.html break;
 		rewrite ^/(\w+)/topics$  /list.html break;
 		rewrite ^/(\w+)/topics/detail/(\d+)$  /detail.html break;
 		try_files $uri $uri/ =404;
 	}
```

**注意：前端页面里的ajax 的url需要改为公网地址**



### 后端部署

​	1） 可先以python3 manage.py runserver  0.0.0.0:8000 进行测试，保证前端没问题后，配置后端服务

​		注意：settings.py中 跨域白名单需开启，allowed_host需要开启，debug模式关闭

​	2）uwsgi配置添加

```shell
[uwsgi]
#http=0.0.0.0:8002
socket=127.0.0.1:8002
# 项目当前工作目录
chdir=/root/ddblog
# 项目中wsgi.py文件的目录,相对于当前工作目录
wsgi-file=ddblog/wsgi.py
# 进程个数
process=1
# 每个进程的线程个数
threads=2
#服务的pid记录文件
pidfile=uwsgi.pid
#服务的日志文件位置
daemonize=uwsgi.log
```

​	启动uwsgi 

进入到项目settings.py所在目录执行如下命令

命令： uwsgi --ini uwsgi.ini

​	3）nginx配置添加

​	新建nginx日志目录 ddblog

​	mkdir -p /var/log/ddblog/

​	cd /etc/nginx/conf.d

​    touch ddblog.conf

```nginx
server {
        listen   8001;
        server_name _;
        access_log /var/log/ddblog/access.log;
        error_log /var/log/ddblog/error.log;

        location / {
                include        uwsgi_params;
                uwsgi_pass     127.0.0.1:8002;
        }

        location /static {
               root /root/blog_static;
        }
    	location /media {
    		  root /root/ddblog;
   		}
}
```

修改前端ajax中的url - 如下命令慎用

```shell
sed -i "s/http:\/\/127.0.0.1:8000/http:\/\/122.9.35.178:8001/g" `grep http://127.0.0.1 -rl templates`
```

