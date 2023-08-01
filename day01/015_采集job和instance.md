> 文档地址
- https://prometheus.io/docs/concepts/jobs_instances/

# 说明
## instance 
- 用Prometheus术语来说，可以抓取的端点称为实例 instance
## job 
- 具有相同目的的实例的集合（例如，出于可伸缩性或可靠性而复制的过程）称为job
## 举例
```yaml
  - job_name: 'pushgateway'
    honor_timestamps: true
    scrape_interval: 15s
    scrape_timeout: 10s
    metrics_path: /metrics
    scheme: http
    static_configs:
    - targets:
      - 172.20.70.205:9091
      - 172.20.70.205:9092
      - 172.20.70.215:9091

```

# 自动生成的标签和时间序列
当Prometheus抓取目标时，它会自动在抓取的时间序列上附加一些标签，以识别被抓取的目标：

- job：目标所属的已配置作业名称。

- instance：<host>:<port>抓取的目标网址的一部分。

- up{job="<job-name>", instance="<instance-id>"}：1实例是否正常（即可达）或0刮取失败。
    - 设置告警查看采集失败的实例 `up==0`
    
      ```yml
      # pro-sql，查看target的状态
      up
      up == 0
      up == 1
      ```
    
       
    
- scrape_duration_seconds{job="<job-name>", instance="<instance-id>"}：刮擦的耗时
    - 举例
    ```shell script
    scrape_duration_seconds{instance="172.20.70.205", job="blackbox-ssh"} 0.001817932
    scrape_duration_seconds{instance="172.20.70.205:3000", job="single-targets"} 0.005416658
    scrape_duration_seconds{instance="172.20.70.205:9091", job="pushgateway"} 0.002726714
    scrape_duration_seconds{instance="172.20.70.205:9092", job="pushgateway"} 0.000506256
    scrape_duration_seconds{instance="172.20.70.205:9100", job="single-targets"} 0.012790691
    scrape_duration_seconds{instance="172.20.70.205:9104", job="single-targets"} 0.021421043
    scrape_duration_seconds{instance="172.20.70.205:9115", job="blackbox-http-targets"} 0.00427973
    ```
    - 用途：统计job中采集比较耗时的instance ,
        - 为什么慢
            - 网络质量
            - metrics数据量太大
            - prometheus采集端有瓶颈了，需要扩容
        - 上次采集最慢的五个 job+instance topk(5,scrape_duration_seconds)
        - 采集时间超过3秒的 scrape_duration_seconds > 3



- scrape_samples_post_metric_relabeling{job="<job-name>", instance="<instance-id>"}：relabel之后剩余的重新标记后剩余的样本数
    - 何为样本：简单理解就是 标签组唯一 
- scrape_samples_scraped{job="<job-name>", instance="<instance-id>"}：目标暴露的样本数
    - 举例  topk(5,scrape_samples_scraped)
        ```shell script
        scrape_samples_scraped{instance="172.20.70.205:9256", job="single-targets"} 1691
        scrape_samples_scraped{instance="172.20.70.215:9256", job="single-targets"} 1010
        scrape_samples_scraped{instance="172.20.70.205:9104", job="single-targets"} 816
        scrape_samples_scraped{instance="172.20.70.215:9100", job="single-targets"} 500
        scrape_samples_scraped{instance="172.20.70.205:9100", job="single-targets"} 500
        ```
    - 用途： 统计样本数量按 job+instance分类
    - 按job排序  `topk(5,sum(scrape_samples_scraped) by (job))`
        ```shell script
        {job="single-targets"} 4957
        {job="redis_exporter_targets"} 299
        {job="pushgateway"} 102
        {job="blackbox-http-targets"} 72
        {job="blackbox-ssh"} 6
        ```
    
- scrape_series_added{job="<job-name>", instance="<instance-id>"}：此抓取中新系列的大概数量。v2.10的新功能
    - 用途 统计新增的metrics，可以用来查看写峰
    - 大部分情况应该都是旧的metrics append写入
    
# prometheus特殊tag说明
- __address__ 采集endpoint的地址
- __name__   metrics 的名称
- instance   endpoint最后的tag
- job         任务
- __metrics_path__  采集的http path 如 /metrics  /cadvisor/metrics 