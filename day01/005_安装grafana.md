> rpm 安装grafana 7
```shell script

# 地址 https://grafana.com/grafana/download
# 如果本地存在，直接上传
wget -O /opt/tgzs/grafana-7.5.1-1.x86_64.rpm https://dl.grafana.com/oss/release/grafana-7.5.1-1.x86_64.rpm

sudo yum install grafana-7.5.1-1.x86_64.rpm


```

> mysql中创建数据库
```shell script
CREATE DATABASE IF NOT EXISTS grafana DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

> 修改配置文件 填写mysql路径等
```shell script
# Ctrl + d  down
# ctrl + u  up
vim /etc/grafana/grafana.ini

type = mysql
host = 127.0.0.1:3306
name = grafana
user = root
password = 123123


```

> 启动服务 
```shell script
systemctl start grafana-server
systemctl enable grafana-server
systemctl status grafana-server
```

> 查看日志 有无报错
```shell script
tail -f /var/log/grafana/grafana.log
```

> 查看ip和端口

```
netstat -nltp
ip ad
```





> 笔记本设置硬解

```shell script
# windows 
C:\Windows\System32\drivers\etc\hosts
192.168.0.111 grafana.prome.me

```

> 笔记本浏览器访问
```shell script
http://grafana.prome.me:3000/?orgId=1

# ip直接访问
http://192.168.116.130:3000/login

默认 用户密码 ：admin/admin

修改密码：admin/123123
```

> 谷歌浏览器不能编辑问题
- issue https://github.com/grafana/grafana/issues/31374
