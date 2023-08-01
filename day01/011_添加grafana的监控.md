> grafana也会暴露指标，添加采集
```shell script
http://grafana.prome.me:3000/metrics
```

> 添加到prometheus采集池

```yaml
  - targets:
    - 172.20.70.205:3000
```
> 导入商城的dashboard 
- 地址 https://grafana.com/grafana/dashboards/3590

