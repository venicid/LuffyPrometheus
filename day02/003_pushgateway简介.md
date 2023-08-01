> 项目地址 
- https://github.com/prometheus/pushgateway

> 什么情况下使用pushgateway
- https://prometheus.io/docs/practices/pushing/
- Pushgateway的唯一有效用例是捕获服务级别批处理作业的结果
- pull网络不通，但有[替代方案](https://github.com/prometheus-community/PushProx) 

> pushgateway 注意事项
- 不支持带时间戳上报，会被忽略
- 当通过单个Pushgateway监视多个实例时，Pushgateway既成为单个故障点，又成为潜在的瓶颈。
- Prometheus为每个采集的target生成的up指标无法使用
- Pushgateway永远不会删除推送到其中的系列，除非通过Pushgateway的API手动删除了这些系列，否则它们将永远暴露给Prometheus


> 下载pushgateway 
```shell script

wget -O /opt/tgzs/pushgateway-1.4.0.linux-amd64.tar.gz wget https://github.com/prometheus/pushgateway/releases/download/v1.4.0/pushgateway-1.4.0.linux-amd64.tar.gz
```

> 准备service文件

cat <<EOF >/opt/tgzs/pushgateway.service
[Unit]
Description=pushgateway server
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/opt/app/pushgateway/pushgateway
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=pushgateway
[Install]
WantedBy=default.target
EOF




> 使用ansible部署 mysql_exporter
```shell script

ansible-playbook -i host_file  service_deploy.yaml  -e "tgz=pushgateway-1.4.0.linux-amd64.tar.gz" -e "app=pushgateway"

```


> 使用prometheus python sdk向pushgateway推送数据

> 安装 sdk
```shell script
pip install prometheus_client
```

> 推送数据
```python
# coding:utf-8
import time

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Counter
import random

# 轮训推送间隔

# 初始化CollectorRegistry
r1 = CollectorRegistry()
# pushgateway api地址
push_addr = "172.20.70.205:9091"

# 初始化一个gauge对象
# labels要在设置时指定好
# 指标类型 gauge,counter,histogram,Summary

g1 = Gauge('kubelet_abc', 'Description of gauge', ['k1', 'k2'], registry=r1)
c1 = Counter('apiserver_abcd', 'HTTP Request', ['method', 'endpoint'], registry=r1)


# 业务埋点

def collect():
    # 设置gauge
    randvalue = random.randint(1, 100)
    g1.labels(k1='v1', k2='v2').set(randvalue)
    c1.labels(method='get', endpoint='/login').inc(10)


if __name__ == '__main__':
    step = 10
    while 1:
        # try:
        collect()
        # 将registry中的数据推送到pushgateway
        # 需要job label
        # 最终调用 put 或post http://pushgateway_addr/metrics/job/some_job
        # put是匹配所有tag相同替换.post是metric_name相同替换
        # res= push_to_gateway(push_addr1, job='2020_09_21_asome_job', registry=r1,handler=custom_handle)
        res = push_to_gateway(push_addr, job='test_job', registry=r1)
        print(res)
        time.sleep(step)

```

> 运行脚本，

> 检查数据 访问 `http://192.168.116.130:9091/ `  `http://192.168.116.130:9091/metrics`

> 将单个pushgateway加入prometheus采集job中

```yaml
[root@prome-master01 tgzs]# vim /opt/app/prometheus/prometheus.yml
  - job_name: 'pushgateway'
    honor_timestamps: true
    scrape_interval: 15s
    scrape_timeout: 10s
    metrics_path: /metrics
    scheme: http
    static_configs:
    - targets:
      - 192.168.116.130:9091
      - 192.168.116.131:9091
```
重新加载文件
curl -X POST http://localhost:9090/-/reload

在promethus上查看数据
http://192.168.116.130:9090/targets



> grafana 上配置pushgateway dashboard

