> 下载prometheus 组件最新版本包
>
> 如果本地有的话，直接上传
```shell script
# 地址
# https://github.com/prometheus/prometheus/releases/tag/v2.25.2
# prometheus 
wget -O /opt/tgzs/prometheus-2.25.2.linux-amd64.tar.gz  https://github.com/prometheus/prometheus/releases/download/v2.25.2/prometheus-2.25.2.linux-amd64.tar.gz

# node_exporter
wget -O /opt/tgzs/node_exporter-1.1.2.linux-amd64.tar.gz https://github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.linux-amd64.tar.gz

# alertmanager
wget -O /opt/tgzs/alertmanager-0.21.0.linux-amd64.tar.gz https://github.com/prometheus/alertmanager/releases/download/v0.21.0/alertmanager-0.21.0.linux-amd64.tar.gz

# pushgateway
wget -O  /opt/tgzs/pushgateway-1.4.0.linux-amd64.tar.gz https://github.com/prometheus/pushgateway/releases/download/v1.4.0/pushgateway-1.4.0.linux-amd64.tar.gz

# process-exporter
wget -O  /opt/tgzs/process-exporter-0.7.5.linux-amd64.tar.gz https://github.com/ncabatoff/process-exporter/releases/download/v0.7.5/process-exporter-0.7.5.linux-amd64.tar.gz

# blackbox_exporter
wget -O  /opt/tgzs/blackbox_exporter-0.18.0.linux-amd64.tar.gz https://github.com/prometheus/blackbox_exporter/releases/download/v0.18.0/blackbox_exporter-0.18.0.linux-amd64.tar.gz

# redis_exporter
wget -O  /opt/tgzs/redis_exporter-v1.20.0.linux-amd64.tar.gz https://github.com/oliver006/redis_exporter/releases/download/v1.20.0/redis_exporter-v1.20.0.linux-amd64.tar.gz

# mysql_exporter
wget -O  /opt/tgzs/mysqld_exporter-0.12.1.linux-amd64.tar.gz https://github.com/prometheus/mysqld_exporter/releases/download/v0.12.1/mysqld_exporter-0.12.1.linux-amd64.tar.gz


```



