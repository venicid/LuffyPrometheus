
# day02/011_prome_shard/prome_shard.py 项目讲解

# 对接服务树等源
```yaml
# 获取，服务树的tree数据，moke
day02/011_prome_shard/get_targets.py
```

# 注册采集源服务到consul中
```yaml
day02/011_prome_shard/consul_work.py

# step_1 注册服务 && 初始化hash-map
ring = ConsistentHashRing(1000, alive_nodes)
service_hash_map[service_name] = ring

```

# watch consul 接收实例变更变换
```yaml
day02/011_prome_shard/consul_work.py
# step_2 开启watch变化结果队列消费进程
# step_3 开启consul watch 进程
# step_4 开启metrics server统计线程
```

# 轮询生成json文件
```yaml
# step_5 主进程：开启定时同步target并发往采集器进程
run_sync_targets(service_hash_map, config)
```

# 发往远端采集器
```yaml
send_target_to_node(service_name, node_map, config)
# ansible 发送到采集器
```


# 日志查看
```shell script
2021-04-07 19:26:36 WARNING consul_work.py [func:watch_service] [line:60]:[节点变化，需要收敛][service:scrape_prome_ecs_inf]
2021-04-07 19:26:36 INFO consul_work.py [func:watch_service] [line:74]:[new_num:1 old_num:2][new_nodes:172.20.70.215 old_nodes:172.20.70.205,172.20.70.215]
2021-04-07 19:26:36 INFO prome_shard.py [func:consumer] [line:219]:[接收到任务][msg:scrape_prome_ecs_inf]
2021-04-07 19:26:36 INFO prome_shard.py [func:shard_job] [line:68]:[shard_job_start_for:scrape_prome_ecs_inf]
```