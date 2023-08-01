# 去哪里找 
# 手段一： rule文件 样例地址 
- https://awesome-prometheus-alerts.grep.to/rules.html#host-and-hardware
- [github](https://github.com/samber/awesome-prometheus-alerts/)

## 机器类型 node_exporter
```yaml
  - alert: 可用内存不总10%
    expr: node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 10
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: Host out of memory (instance {{ $labels.instance }})
      description: "Node memory is filling up (< 10% left)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: 网卡入流量超过100 MB/s
    expr: sum by (instance) (rate(node_network_receive_bytes_total[2m])) / 1024 / 1024 > 100
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: Host unusual network throughput in (instance {{ $labels.instance }})
      description: "Host network interfaces are probably receiving too much data (> 100 MB/s)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: 网卡出流量超过100 MB/s
    expr: sum by (instance) (rate(node_network_transmit_bytes_total[2m])) / 1024 / 1024 > 100
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: Host unusual network throughput out (instance {{ $labels.instance }})
      description: "Host network interfaces are probably sending too much data (> 100 MB/s)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: 块设备读取速率超过50 MB/s
    expr: sum by (instance) (rate(node_disk_read_bytes_total[2m])) / 1024 / 1024 > 50
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: Host unusual disk read rate (instance {{ $labels.instance }})
      description: "Disk is probably reading too much data (> 50 MB/s)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

  - alert: 块设备写入速率超过50 MB/s
    expr: sum by (instance) (rate(node_disk_written_bytes_total[2m])) / 1024 / 1024 > 50
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: Host unusual disk write rate (instance {{ $labels.instance }})
      description: "Disk is probably writing too much data (> 50 MB/s)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"


  - alert: 文件系统分区剩余小于10%
    expr: (node_filesystem_avail_bytes * 100) / node_filesystem_size_bytes < 10 and ON (instance, device, mountpoint) node_filesystem_readonly == 0
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: Host out of disk space (instance {{ $labels.instance }})
      description: "Disk is almost full (< 10% left)\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"


  - alert: 预测文件系统24小时用光
    expr: (node_filesystem_avail_bytes * 100) / node_filesystem_size_bytes < 10 and ON (instance, device, mountpoint) predict_linear(node_filesystem_avail_bytes{fstype!~"tmpfs"}[1h], 24 * 3600) < 0 and ON (instance, device, mountpoint) node_filesystem_readonly == 0
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: Host disk will fill in 24 hours (instance {{ $labels.instance }})
      description: "Filesystem is predicted to run out of space within the next 24 hours at current write rate\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"



  - alert: cpu使用超过80%
    expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100) > 80
    for: 0m
    labels:
      severity: warning
    annotations:
      summary: Host high CPU load (instance {{ $labels.instance }})
      description: "CPU load is > 80%\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

 
```


## 黑盒探针 blackbox_exporter
```yaml
  - alert: BlackboxProbeFailed
    expr: probe_success == 0
    for: 0m
    labels:
      severity: critical
    annotations:
      summary: Blackbox probe failed (instance {{ $labels.instance }})
      description: "Probe failed\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}"

```

# 手段二：去各个exporter的github上找
## 规范的exporter需要提供下列信息 ，mysqld_exporter看起来很 规范 都提供了
1. grafana.json：grafana 大盘模板文件
    -  https://github.com/prometheus/mysqld_exporter/blob/master/mysqld-mixin/dashboards/mysql-overview.json
2. alert_rule.yml : prometheus告警的表达式 
    - https://github.com/prometheus/mysqld_exporter/blob/master/mysqld-mixin/alerts/galera.yaml
    
#  没辙了：咋办： 
1.  看代码
2. metrics指标会写的很详细
```yaml
[root@prome-master01 prometheus]# curl localhost:9093/metrics
# HELP alertmanager_silences_queries_total How many silence queries were received.
# TYPE alertmanager_silences_queries_total counter
alertmanager_silences_queries_total 5

```