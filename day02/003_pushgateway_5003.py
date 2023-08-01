# coding:utf-8
import math
import time

import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Counter, Histogram, Summary
import random

# 轮训推送间隔

# 初始化CollectorRegistry
r1 = CollectorRegistry()
# pushgateway api地址
push_addr = "192.168.116.130:5003"
# push_addr = "localhost:5003"

# 初始化一个gauge对象
# labels要在设置时指定好
# 指标类型 gauge,counter,histogram,Summary

g1 = Gauge('test_gauge_01', 'Description of gauge', ['k1', 'k2'], registry=r1)
# 查看promql rate(test_counter_01_total[30s])
c1 = Counter('test_counter_01', 'HTTP Request', ['method', 'endpoint'], registry=r1)
# 默认的bucket DEFAULT_BUCKETS = (.005, .01, .025, .05, .075, .1, .25, .5, .75, 1.0, 2.5, 5.0, 7.5, 10.0, INF)
test_buckets = (-5, 0, 5)
#  查看promql histogram_quantile(0.90, sum(rate(test_histogram_01_bucket{}[30s])) by (le))
h1 = Histogram('test_histogram_01', 'test of histogram', buckets=test_buckets, registry=r1)
# python sdk 不支持 quantile  https://github.com/prometheus/client_python/issues/92
# 可以使用 _sum/_count = avg
s1 = Summary('test_summary_01', 'A summary', registry=r1)


# 业务埋点

def collect():
    # gauge设置值
    g1.labels(k1='v1', k2='v2').set(random.randint(1, 100))
    # counter递增
    c1.labels(method='get', endpoint='/login').inc(10)
    # histogram
    h1.observe(random.randint(-10, 10))
    # summary

    f(random.uniform(0, 1))
    # summary_time()
    # s1.labels('a', 'b').observe(10)
    # s1.collect()


@s1.time()
def f(t):
    time.sleep(t)

    # pass

def custom_handle(url, method, timeout, headers, data):
    def handle():
         h = {}
         for k, v in headers:
            h[k] = v
         if method == 'PUT':
            print(url)
            print(data)
            print(timeout)
            resp = requests.put(url, data=data, headers=h, timeout=timeout)
         elif method == 'POST':
            resp = requests.post(url, data=data, headers=h, timeout=timeout)
         elif method == 'DELETE':
            resp = requests.delete(url, data=data, headers=h, timeout=timeout)
         else:
            return
         if resp.status_code >= 400:
            raise IOError("error talking to pushgateway: {0} {1}".format(resp.status_code, resp.text))
    return handle

if __name__ == '__main__':
    step = 10
    while True:
        # try:
        for i in ["a", "b", "c", "d"]:
            collect()
            # 将registry中的数据推送到pushgateway
            # 需要job label
            # 最终调用 put 或post http://pushgateway_addr/metrics/job/some_job
            # put是匹配所有tag相同替换.post是metric_name相同替换
            # res= push_to_gateway(push_addr1, job='2020_09_21_asome_job', registry=r1,handler=custom_handle)
            try:
                res = push_to_gateway(push_addr, job='test_job_{}'.format(i), registry=r1, timeout=5, handler=custom_handle)
                print(res)
            except Exception as  e:
                print(e)


        time.sleep(step)
