# coding:utf-8
import time

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Counter
import random

# 轮训推送间隔

# 初始化CollectorRegistry
r1 = CollectorRegistry()
# pushgateway api地址
push_addr = "192.168.116.130:9091"

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
