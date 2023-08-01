> 文档地址 
- https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config

> relabel说明
- relabel是一种强大的工具，可以在采集目标之前动态重写目标的标签集

> relabel_action 动作说明 
- replace： regex匹配source_labels，然后把replacement设置为target_label，可以使用匹配组的引用（${1}，${2}，...）
    - 举例 k8s中采集 容器基础指标时如下配置
    ```yaml
    - job_name: kubernetes-nodes-cadvisor
      honor_timestamps: true
      scrape_interval: 30s
      scrape_timeout: 10s
      metrics_path: /metrics
      scheme: https
     
      kubernetes_sd_configs:
      - role: node
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        insecure_skip_verify: true
      relabel_configs:
      - separator: ;
        regex: __meta_kubernetes_node_label_(.+)
        replacement: $1
        action: labelmap
      - separator: ;
        regex: (.*)
        target_label: __metrics_path__
        replacement: /metrics/cadvisor
        action: replace
    ```
    - 这里的 表示服务发现后的node中标签以`_meta_kubernetes_node_label_`开头的key，替换为后面的字符串
    - 举例`__meta_kubernetes_node_label_kubernetes_io_arch="amd64" `这组keyv将被替换为 `kubernetes_io_arch="amd64"`



- keep：source_labels regex匹配的目标被keep，白名单
- drop：source_labels regex匹配的目标被drop，黑名单
    - 配置样例
    ```yaml
        - source_labels: [__name__]
        separator: ;
        # 标签key前缀匹配到的drop
        regex: '(kubelet_|apiserver_|container_fs_).*'
        replacement: $1
        action: drop
    ```
    
- hashmod：设置target_label为的modulus哈希值的source_labels
    - 这个prome数据量太大了，需要启动多个prome，需要做的是：在这个namespace再启动一个prome ，在所有的scrape job中添加如下relabel_configs配置  ， 第一个实例 regex:         ^0$，第二个实例 regex:         ^1$
    ```yaml
     relabel_configs:
      - source_labels: [__address__]
        regex: (.*)
        modulus: 2
        target_label: __tmp_hash
        replacement: $1
        action: hashmod
      - source_labels: [__tmp_hash]
        regex: ^0$
        replacement: $1
        action: keep
      relabel_configs:
        - source_labels: [__address__]
          modulus:       2
          target_label:  __tmp_hash
          action:        hashmod
        - source_labels: [__tmp_hash]
          regex:         ^0$
          action:        keep  
    ```
    
- labelmap：regex与所有标签名称匹配。然后匹配标签的值复制到由给定的标签名称replacement与匹配组的参考（${1}，${2}，...）在replacement由他们的价值取代。
- labeldrop：将regex匹配到的标签删除
- labelkeep：将regex没匹配到的标签删除





