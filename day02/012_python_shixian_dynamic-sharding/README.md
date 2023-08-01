# 使用

## 修改yml文件
```yaml

# consul api 地址
host: 192.168.116.130
port:  8500
  
# pushgateway 信息
pushgateway:
  # 端口号
  port: 9091
  # pushgateway ip列表
  servers:
    - 192.168.116.130
    - 192.168.116.131

```

## 运行
```yaml
python3 flask_dynamic-sharding.py

2023-07-04 13:31:14 WARNING _internal.py [func:_log] [line:225]: * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
2023-07-04 13:31:14 INFO _internal.py [func:_log] [line:225]: * Running on http://192.168.116.130:5003/ (Press CTRL+C to quit)
```


## pushgateway打点
```yaml
# 重启pushgateway，清除数据
systemctl restart pushgateway

# 修改day02/003_pushgateway_5003.py文件
# pushgateway地址修改
push_addr = "192.168.116.130:5003"

# 运行，查看日志
2023-07-04 13:33:57 INFO flask_dynamic-sharding.py [func:push_metrics_redirect] [line:51]:[req_path:/metrics/job/test_job_a][target_node:192.168.116.130:9091][next_url:http://192.168.116.130:9091/metrics/job/test_job_a]
2023-07-04 13:33:57 INFO _internal.py [func:_log] [line:225]:192.168.116.1 - - [04/Jul/2023 13:33:57] "PUT /metrics/job/test_job_a HTTP/1.1" 307 -
2023-07-04 13:33:57 INFO flask_dynamic-sharding.py [func:push_metrics_redirect] [line:51]:[req_path:/metrics/job/test_job_b][target_node:192.168.116.130:9091][next_url:http://192.168.116.130:9091/metrics/job/test_job_b]
2023-07-04 13:33:57 INFO _internal.py [func:_log] [line:225]:192.168.116.1 - - [04/Jul/2023 13:33:57] "PUT /metrics/job/test_job_b HTTP/1.1" 307 -
2023-07-04 13:33:57 INFO flask_dynamic-sharding.py [func:push_metrics_redirect] [line:51]:[req_path:/metrics/job/test_job_c][target_node:192.168.116.131:9091][next_url:http://192.168.116.131:9091/metrics/job/test_job_c]
2023-07-04 13:33:57 INFO _internal.py [func:_log] [line:225]:192.168.116.1 - - [04/Jul/2023 13:33:57] "PUT /metrics/job/test_job_c HTTP/1.1" 307 -
2023-07-04 13:33:58 INFO flask_dynamic-sharding.py [func:push_metrics_redirect] [line:51]:[req_path:/metrics/job/test_job_d][target_node:192.168.116.130:9091][next_url:http://192.168.116.130:9091/metrics/job/test_job_d]
2023-07-04 13:33:58 INFO _internal.py [func:_log] [line:225]:192.168.116.1 - - [04/Jul/2023 13:33:58] "PUT /metrics/job/test_job_d HTTP/1.1" 307 -


# 查看网页数据
http://192.168.116.130:9091/#
http://192.168.116.131:9091/#
```

## 说明
```yaml
# 302 与307 问题
https://blog.csdn.net/LeechengLove/article/details/109022792

# 自定义handler，客户端
res = push_to_gateway(push_addr, job='test_job_{}'.format(i), registry=r1, timeout=5, handler=custom_handle)
```

## 测试，停止一个pushgateway
```yaml

# node2停止
[root@prome-node01 ~]# systemctl stop pushgateway


# 查看日志, test_job全部打到节点一
2023-07-04 23:52:29 INFO flask_dynamic-sharding.py [func:push_metrics_redirect] [line:51]:[req_path:/metrics/job/test_job_d][target_node:192.168.116.130][next_url:http://192.168.116.130/metrics/job/test_job_d]
2023-07-04 23:52:29 INFO _internal.py [func:_log] [line:225]:192.168.116.1 - - [04/Jul/2023 23:52:29] "PUT /metrics/job/test_job_d HTTP/1.1" 307 -
2023-07-04 23:52:42 INFO flask_dynamic-sharding.py [func:push_metrics_redirect] [line:51]:[req_path:/metrics/job/test_job_a][target_node:192.168.116.130][next_url:http://192.168.116.130/metrics/job/test_job_a]
2023-07-04 23:52:42 INFO _internal.py [func:_log] [line:225]:192.168.116.1 - - [04/Jul/2023 23:52:42] "PUT /metrics/job/test_job_a HTTP/1.1" 307 -
2023-07-04 23:52:45 INFO flask_dynamic-sharding.py [func:push_metrics_redirect] [line:51]:[req_path:/metrics/job/test_job_b][target_node:192.168.116.130][next_url:http://192.168.116.130/metrics/job/test_job_b]
2023-07-04 23:52:45 INFO _internal.py [func:_log] [line:225]:192.168.116.1 - - [04/Jul/2023 23:52:45] "PUT /metrics/job/test_job_b HTTP/1.1" 307 -
2023-07-04 23:52:47 INFO flask_dynamic-sharding.py [func:push_metrics_redirect] [line:51]:[req_path:/metrics/job/test_job_c][target_node:192.168.116.130][next_url:http://192.168.116.130/metrics/job/test_job_c]
2023-07-04 23:52:47 INFO _internal.py [func:_log] [line:225]:192.168.116.1 - - [04/Jul/2023 23:52:47] "PUT /metrics/job/test_job_c HTTP/1.1" 307 -

# 注意
1. 需要添加异常捕获，pushgateway_5003
    try:
        res = push_to_gateway(push_addr, job='test_job_{}'.format(i), registry=r1, timeout=5, handler=custom_handle)
    except Exception as  e:
        print(e)

2. 页面上，pushgateway并未更新test_job
  - 未解决问题

3. 推荐使用golang代码重新运行，测试。具体操作看课件即可
```