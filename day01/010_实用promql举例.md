# 基础
> 文档地址
- https://prometheus.io/docs/prometheus/latest/querying/basics/


## 同环比 offset
- 思考 同环比的本质是什么
- 常用例子
- 举例 查询一小时前的网卡数据 `rate(node_network_receive_bytes_total{device!="lo"}[1m] offset 1h)`

```
avg(rate(node_cpu_seconds_total{instance=~"$node",mode="system"}[$interval] offset 1m)) by (instance) *100
```



- offset修饰符始终需要立即跟随选择器

- rate(node_network_receive_bytes_total{device="eth0"}[1m] ) offset 1h 会报错


## 默认禁用的选项
- https://prometheus.io/docs/prometheus/latest/disabled_features/
> @ 修饰符指定时间
```shell script
--enable-feature=promql-at-modifier

该@修改器可以指定评估时间为即时矢量选择，范围矢量选择和子查询。可以在这里找到更多详细信息。

```
> 负偏移  offset -1w
```shell script
默认情况下会禁用此负偏移量，因为它打破了PromQL不会在样本评估时间之前进行查找的不变性。

--enable-feature=promql-negative-offset

与正偏移量修改器相比，负偏移量修改器使向量选择器可以移至将来。一个可能要使用负偏移量的示例是查看过去的数据并与最新数据进行时间比较。
```

>  远程写接收器
```shell script
--enable-feature=remote-write-receiver

远程写接收器允许Prometheus接受来自其他Prometheus服务器的远程写请求。可以在这里找到更多详细信息。

```

## 子查询

- https://www.robustperception.io/promql-subqueries-and-alignment


# 运算符 operators
- https://prometheus.io/docs/prometheus/latest/querying/operators/
## + - * /
> 加
```shell script
# 查看已用内存 = 总内存 - 可用内存
node_memory_MemTotal_bytes{instance=~"$node"} - node_memory_MemAvailable_bytes{instance=~"$node"}
```


> - *
```shell script
# 查看利用率
(1 - avg(rate(node_cpu_seconds_total{instance=~"172\\.20\\.70\\.205:9100",mode="idle"}[2m])) by (instance))*100
```

> 过滤值 用于配置告警
```shell script
# 平均user态 cpu利用率大于 4就告警
avg(rate(node_cpu_seconds_total{mode="user"}[1m])) by (instance) * 100  > 4

avg(rate(node_cpu_seconds_total{instance=~"$node",mode="system"}[$interval])) by (instance) *100 > 0.9
```


## 组合条件 and
> 要求前后label一致 
- 举例: m3db read 大于并且 db_write 大于1000   ```avg by(cluster) (rate(database_read_success{cluster="hawkeye-inf",instance="10.21.72.147:9004"}[1m]) ) > 100 and avg by(cluster)  (rate(service_writeTaggedBatchRaw_success{cluster="hawkeye-inf",instance="10.21.77.55:9004"}[1m]) ) >1000```
```shell script
#  mem Buffers 和cacahe 
node_memory_Buffers_bytes > 10000 and node_memory_Cached_bytes > 100000
```
- 前后label一致 

## 或条件 or
```shell script
go_gc_duration_seconds > 0.01 or node_memory_Cached_bytes > 100000
```


## 实用功能总结

### label 正则/正则非匹配
- 举例：pod状态 ```kube_pod_status_phase{pod!~"filebeat.*",job="kube-state-metrics", namespace !~"druid",phase=~"Pending|Unknown"}```

### agg 去掉/保留 label ，分布情况
- 去掉举例： ```sum without(code) (rate(apiserver_request_total[2m] ) )  ```

- 保留举例：

   ```sum by(code) (rate(apiserver_request_total[2m] ) )  ``` 

  ` sum by(statuscode) (rate(http_request_total [2m] ) )`

   ` sum by(statuscode,method) (rate(http_request_total [2m] ) )`

    ` sum by(statuscode,method, handler) (rate(http_request_total [2m] ) )`

- 举例：apiserver 请求qps和按动作分布 ```sum (rate(apiserver_request_total[2m] ) ) by(verb)```

- 举例：apiserver 请求qps和按动作,code分布 ```sum (rate(apiserver_request_total[2m] ) ) by(verb,code)```

### label_replace 变化label

- 举例：新增host标签内容为instance的ipaddr ```label_replace(up, "host", "$1", "instance",  "(.*):.*")```  

- 原始series   ``` up{instance="localhost:8080",job="cadvisor"}   1 ``

- 改造后series ``` up{host="localhost",instance="localhost:8080",job="cadvisor"}   1 ``

- 将 instance标签替换为host : 不想在采集上修改了，直接在告警中修改

  `sum without(instance )(label_replace(up, "host", "$1", "instance", "(.*):.*"))`
### topk bottomK 看top
- 举例：查看容器cpu使用率top5 ```topk(5,sum(rate (container_cpu_usage_seconds_total[1m])) by(pod))```

  查看node使用率最高的top1

  topk(1,node_memory_MemTotal_bytes{instance=~"$node"}) 

### 同环比 相减
- 举例：qps环比1小时 掉10 ```sum (rate(apiserver_request_total[2m] offset 1h) ) - sum (rate(apiserver_request_total[2m] ) )  > 10 ```

### absent nodata报警
- ==1代表absent生效
- 举例：```absent(container_cpu_usage_seconds_total{pod=~"k8s-mon.*jddj2"})```
- ` absent(aup{})` ，值为1 ， no data 代表没有找到aup

举例子

- live_people_sum > 80 告警
- 检查，live_people_sum 这个值，是否缺少，为null

### 查询时直接添加value过滤 
- 举例:容器处于waiting状态 ```kube_pod_container_status_waiting==1```
- 举例: 过滤cpu核数大于8的节点  ```kube_node_status_capacity_cpu_cores>8```
- 举例：pod状态异常：```sum by (namespace, pod,cluster,phase) (kube_pod_status_phase{pod!~"filebeat.*",job="kube-state-metrics", namespace !~"druid",phase=~"Pending|Unknown"}) > 0```

### 查询时直接做value计算
- 举例: 根据idle算util百分比 ```100 * (1 - avg by(instance)(irate(node_cpu{mode='idle'}[5m])))``` 

### 组合条件 and
- 举例: m3db read 大于并且 db_write 大于1000   ```avg by(cluster) (rate(database_read_success{cluster="hawkeye-inf",instance="10.21.72.147:9004"}[1m]) ) > 100 and avg by(cluster)  (rate(service_writeTaggedBatchRaw_success{cluster="hawkeye-inf",instance="10.21.77.55:9004"}[1m]) ) >1000```
- 前后label一致 
- or 同理

### 分位值histogram_quantile 
- 举例查看apiserver 请求延迟90分位 ```histogram_quantile(0.90, sum(rate(apiserver_request_duration_seconds_bucket{verb!~"CONNECT|WATCH"}[5m])) by (le))```

### 两组series关联  成功率，灭火图
- 举例：apiserver 请求成功率 ```sum(apiserver_request_total{code=~"2.*|3.*"})/  sum(apiserver_request_total)```
- http请求成功率
  - sum(rate(http_request_total{statuscode=~"2.*|3.*"}[1m])) / sum(rate(http_request_total{}[1m]))


> 灭火图：饼图。http请求成功率

- `sum(rate(http_request_total{statuscode=~"2.*"}[1m]))` 
- ` sum(rate(http_request_total{statuscode=~"3.*"}[1m]))`
- ` sum(rate(http_request_total{statuscode=~"4.*"}[1m]))`


### agg_over_time 给所有ts的value做agg
- 举例查看一天的alert ```sort_desc(sum(sum_over_time(ALERTS{alertstate=`firing`}[24h])) by (alertname))```
- 举例查看一天的alert ```sort_desc(sum(sum_over_time(ALERTS{alertstate=`firing`}[24h])) by (alertname))```