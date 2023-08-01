> 文档地址
- https://prometheus.io/docs/guides/multi-target-exporter/

# exporter 分类

|  是否支持多实例采集   | 举例 | 采集触发模式  | 
|  ----  | ----  | ---- | 
| 是	| `blackbox_exporter` `snmp exporter` |	请求时采集|  
| 否	| `node_exporter`  |	内部ticker采集|  


# proemetheus exporter 多实例采集说明
> 为什么有多实例采集
- 要么无法在目标服务器上运行程序，例如说网络设备的SNMP
- 要么我们对距离（例如网站从网络外部特定点到站点的延迟和可访问性）特别感兴趣，这是常见的黑盒导出器的用例。
- 或者说部署agent代价比较大




> 多实例采集模式特点

- exporter将通过网络协议获取目标的指标。
- exporter不必在获取度量标准的计算机上运行。
- Prometheus GET请求的参数作为 exporter获取目标和查询配置字符串
- 然后，exporter在收到Prometheus的GET请求之后开始抓取
- exporter可以采集多个目标


> blackbox_exporter 需要传入target 和 module 参数，采用下列方式加入的采集池中 
```yaml
  - job_name: 'blackbox-http'
    # metrics的path 注意不都是/metrics
    metrics_path: /probe
    # 传入的参数
    params:
      module: [http_2xx]  # Look for a HTTP 200 response.
      target: [prometheus.io,www.baidu.com,172.20.70.205:3000]
    static_configs:
      - targets:
        - 172.20.70.205:9115 
```
- 此方案的缺点
    - 实际采集目标位于参数配置中，这非常不寻常，以后很难理解。
    - 该instance标签显示的是`blackbox_exporter`的地址，从技术上讲是真实的，但不是我们感兴趣的内容。
    - 我们看不到我们探查了哪个URL。这是不切实际的，并且如果我们探查多个URL，也会将不同的指标混合到一个指标中。

- 解决方案说明：relabeling
    - 所有以__开头的标签在采集完成后都会被drop调。大多数内部标签以开头__
    - 可以设置一个内部标签形如`__param_<name>` ，代表设置URL参数 name=value 
    - 有一个内部标签__address__，在static_configs时由targets设置，其值是抓取请求的主机名。默认情况下，它被赋值给instance 标签，代表采集来源。

    
> blackbox_exporter relabel 配置
- 将参数作为采集的target传入
```yaml
  - job_name: 'blackbox-http'
    # metrics的path 注意不都是/metrics
    metrics_path: /probe
    # 传入的参数
    params:
      module: [http_2xx]  # Look for a HTTP 200 response.
    static_configs:
      - targets:
        - http://prometheus.io    # Target to probe with http.
        - https://www.baidu.com   # Target to probe with https.
        - http://172.20.70.205:3000 # Target to probe with http on port 3000.
    relabel_configs:
      # 第一步：我们从标签中获取值__address__（来自targets），然后将它们写入新标签__param_target
      # 然后blackbox_exporter 会接收到 target参数
      - source_labels: [__address__]
        target_label: __param_target

      # 第二步：我们从标签_param_target中获取值，并使用这些值创建instance标签。
      - source_labels: [__param_target]
        target_label: instance

      # 第三步： 将采集源由原来的targe替换为 真实的blackbox_exporter地址
      - target_label: __address__
        replacement: 127.0.0.1:9115  # The blackbox exporter's real hostname:port.

```


# prometheus特殊tag说明
- __address__
- __name__
- instance
- job
- __metrics_path__ 