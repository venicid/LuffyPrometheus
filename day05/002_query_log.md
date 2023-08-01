# 配置
```yaml
# global段开启log即可
global:
  query_log_file: /opt/logs/prometheus_query_log

```

# range_query_log解析
```shell script
{
   # 请求基础信息
    "httpRequest":{
        "clientIP":"192.168.43.114",
        "method":"POST",
        "path":"/api/v1/query_range"
    },
    # 参数段
    "params":{
        "end":"2021-05-03T02:32:45.000Z",
        "query":"rate(node_disk_reads_completed_total{instance=~"192\\.168\\.43\\.114:9100"}[2m])",
        "start":"2021-05-03T02:17:45.000Z",
        "step":15
    },
    # 统计段
    "stats":{
        "timings":{
            "evalTotalTime":0.000331799,
            "resultSortTime":0.000001235,
            "queryPreparationTime":0.000075478,
            "innerEvalTime":0.00024141,
            "execQueueTime":0.000012595,
            "execTotalTime":0.000354698
        }
    },
    # 请求时间
    "ts":"2021-05-03T02:32:49.876Z"
}
```
