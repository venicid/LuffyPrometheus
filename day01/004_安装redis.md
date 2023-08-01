> yum 安装redis 3.2
```shell script
yum -y install redis 
```






> 课程中
> 编译安装redis-6.2.1
- 文档 https://redis.io/download

```shell script
yum install -y gcc gcc-c++ tcl

wget  -O /opt/tgzs/redis-6.2.1.tar.gz https://download.redis.io/releases/redis-6.2.1.tar.gz
cd /opt/tgzs/


#解压redis
tar xf redis-6.2.1.tar.gz
#进入解压后的目录
cd redis-6.2.1
#分配器allocator，如果有MALLOC  这个 环境变量， 会有用这个环境变量的 去建立Redis。

#而且libc 并不是默认的分配器， 默认的是 jemalloc, 因为 jemalloc 被证明 有更少的 fragmentation problems 比libc。

#但是如果你又没有jemalloc而只有 libc 当然 make 出错。 所以加这么一个参数,运行如下命令：

make MALLOC=libc -j 20

#编译

# make -j 20
#创建redis安装目录，主要用于存放redis所需bin文件
mkdir -p /usr/local/redis
#安装redis并指定安装目录
make PREFIX=/usr/local/redis/ install

# 设置path，配置文件
vim /etc/profile
export PATH=$PATH:/usr/local/redis/bin
source /etc/profile

2. 设置两个实例

#复制默认配置文件到/etc
egrep -v  "^$|#" redis.conf   > redis_sample.conf
#修改配置文件监听IP为0.0.0.0，否则只能本地登录
sed -i s/bind\ 127.0.0.1/bind\ 0.0.0.0/g redis_sample.conf
#修改运行方式为后台运行
sed -i s/daemonize\ no/daemonize\ yes/g redis_sample.conf


/bin/cp -f redis_sample.conf /etc/redis_6379.conf 
/bin/cp -f redis_sample.conf /etc/redis_6479.conf 

#设置日志文件路径
sed -i s@logfile\ \"\"@logfile\ \"/opt/logs/redis_6379.log\"@g /etc/redis_6379.conf 
sed -i s@logfile\ \"\"@logfile\ \"/opt/logs/redis_6479.log\"@g /etc/redis_6479.conf 

#设置数据目录
sed -i s@dir\ \./@dir\ /var/lib/redis_6379@g /etc/redis_6379.conf 
sed -i s@dir\ \./@dir\ /var/lib/redis_6479@g /etc/redis_6479.conf 

# 修改port
sed -i 's/port 6379/port 6379/g' /etc/redis_6379.conf 
sed -i 's/port 6379/port 6479/g' /etc/redis_6479.conf 

mkdir  /var/lib/redis_6379
mkdir  /var/lib/redis_6479
mkdir  /opt/logs

cat <<EOF > /etc/systemd/system/redis_6379.service 
[Unit]
Description=The redis-server Process Manager
After=syslog.target network.target

[Service]
Type=forking
ExecStart=/usr/local/redis/bin/redis-server /etc/redis_6379.conf
#ExecStop=/usr/local/redis/bin/redis-shutdown

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > /etc/systemd/system/redis_6479.service 
[Unit]
Description=The redis-server Process Manager
After=syslog.target network.target

[Service]
Type=forking
ExecStart=/usr/local/redis/bin/redis-server /etc/redis_6479.conf
#ExecStop=/usr/local/redis/bin/redis-shutdown

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
#设置redis开机自启
systemctl enable redis_6379
systemctl enable redis_6479
#启动redis
systemctl restart redis_6379
systemctl restart redis_6479
#查看redis状态
systemctl status redis_6379
systemctl status redis_6479


3. 测试
[root@prome-master01 redis-6.2.1]# redis-cli 
127.0.0.1:6379> get name
(nil)
127.0.0.1:6379> set name alex
OK
127.0.0.1:6379> get name
"alex"

```



