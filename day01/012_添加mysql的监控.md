> 在mysql的机器上部署 mysql_exporter
- 项目地址 https://github.com/prometheus/mysqld_exporter 


> 使用ansible部署 mysql_exporter
```shell script

ansible-playbook -i host_file  service_deploy.yaml  -e "tgz=mysqld_exporter-0.12.1.linux-amd64.tar.gz" -e "app=mysqld_exporter"

```

> 部署后发现服务未启动 ，报错如下
```shell script
# 访问
http://192.168.116.130:9104/metrics
mysql_up 0

# tail -f /opt/logs/mysqld_exporter.log 
Jun 13 23:59:30 prome-master01 mysqld_exporter: time="2023-06-13T23:59

Mar 30 10:41:10 prome_master_01 mysqld_exporter[30089]: time="2021-03-30T10:41:10+08:00" level=fatal msg="failed reading ini file: open .my.cnf: no such file or directory" source="mysqld_exporter.go:264"



```

> 创建采集用户，并授权
```shell script
mysql -uroot -p123123

CREATE USER 'exporter'@'%' IDENTIFIED BY '123123' ;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'%';
FLUSH PRIVILEGES;



```

> 方式一：在mysqld_exporter的service 文件中使用环境变量 DATA_SOURCE_NAME
```shell script
# 代表localhost
# 生效位置
# vim /etc/systemd/system/mysqld_exporter.service
[Service]
Environment=DATA_SOURCE_NAME=exporter:123123@tcp/
ExecStart=/opt/app/mysqld_exporter/mysqld_exporter
```

> 重启mysqld_exporter服务
```shell script
systemctl daemon-reload
systemctl restart mysqld_exporter

```

> 查看mysqld_exporter日志
```shell script
[root@prome_master_01 logs]# systemctl status mysqld_exporter -l
● mysqld_exporter.service - mysqld_exporter Exporter
   Loaded: loaded (/etc/systemd/system/mysqld_exporter.service; enabled; vendor preset: disabled)
   Active: active (running) since Tue 2021-03-30 10:53:08 CST; 11min ago
 Main PID: 30158 (mysqld_exporter)
   CGroup: /system.slice/mysqld_exporter.service
           └─30158 /opt/app/mysqld_exporter/mysqld_exporter

Mar 30 10:53:08 prome_master_01 mysqld_exporter[30158]: time="2021-03-30T10:53:08+08:00" level=info msg="Starting mysqld_exporter (version=0.12.1, branch=HEAD, revision=48667bf7c3b438b5e93b259f3d17b70a7c9aff96)" source="mysqld_exporter.go:257"
Mar 30 10:53:08 prome_master_01 mysqld_exporter[30158]: time="2021-03-30T10:53:08+08:00" level=info msg="Build context (go=go1.12.7, user=root@0b3e56a7bc0a, date=20190729-12:35:58)" source="mysqld_exporter.go:258"
Mar 30 10:53:08 prome_master_01 mysqld_exporter[30158]: time="2021-03-30T10:53:08+08:00" level=info msg="Enabled scrapers:" source="mysqld_exporter.go:269"
Mar 30 10:53:08 prome_master_01 mysqld_exporter[30158]: time="2021-03-30T10:53:08+08:00" level=info msg=" --collect.global_status" source="mysqld_exporter.go:273"
Mar 30 10:53:08 prome_master_01 mysqld_exporter[30158]: time="2021-03-30T10:53:08+08:00" level=info msg=" --collect.global_variables" source="mysqld_exporter.go:273"
Mar 30 10:53:08 prome_master_01 mysqld_exporter[30158]: time="2021-03-30T10:53:08+08:00" level=info msg=" --collect.slave_status" source="mysqld_exporter.go:273"
Mar 30 10:53:08 prome_master_01 mysqld_exporter[30158]: time="2021-03-30T10:53:08+08:00" level=info msg=" --collect.info_schema.innodb_cmp" source="mysqld_exporter.go:273"
Mar 30 10:53:08 prome_master_01 mysqld_exporter[30158]: time="2021-03-30T10:53:08+08:00" level=info msg=" --collect.info_schema.innodb_cmpmem" source="mysqld_exporter.go:273"
Mar 30 10:53:08 prome_master_01 mysqld_exporter[30158]: time="2021-03-30T10:53:08+08:00" level=info msg=" --collect.info_schema.query_response_time" source="mysqld_exporter.go:273"
Mar 30 10:53:08 prome_master_01 mysqld_exporter[30158]: time="2021-03-30T10:53:08+08:00" level=info msg="Listening on :9104" source="mysqld_exporter.go:283"
```


> 方式二：使用my.cnf启动服务
```shell script
Environment=DATA_SOURCE_NAME='exporter:123123@(localhost:3306)/'
```
> 将mysqld_exporter 采集加入的采集池中 
```shell script
# vim /opt/app/prometheus/prometheus.yml
  - job_name: mysqld_exporter
    honor_timestamps: true
    scrape_interval: 15s
    scrape_timeout: 10s
    metrics_path: /metrics
    scheme: http
    static_configs:
    - targets:
      - 192.168.116.130:9104

# reload
curl -vv -X POST localhost:9090/-/reload
```

> prometheus界面搜索mysql

```
# http://192.168.116.130:9090

mysql_exporter_scrapes_total
```



> grafana 上导入mysqld-dashboard

- 地址 https://grafana.com/grafana/dashboards/11323

> 按需启动采集项



```
#查看mysql的数据
mysql> select *from dashboard limit 2;
```



