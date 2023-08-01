# 时序数据模型
> 数据点 ： Samples form the actual time series data. Each sample consists of:

- a float64 value
- a millisecond-precision timestamp
```golang
type sample struct {
    t int64
    v float64
}
```

> 序列 
- 就是标识符（维度），主要的目的是方便进行搜索和筛选
- 每个时间序列都通过其指标名称和可选的键值对（称为标签）来唯一标识。
```shell script
api_http_requests_total{method="POST", handler="/messages"}
```

# 存储模型
> 针对tsdb`写多读少`的存储特点
> LSM-Tree通常对于写入更友好，而BTree则对于读应用更友好。



# prometheus tsdb发展历史
- Prometheus 1.0版本的TSDB（V2存储引擎）基于LevelDB，并且使用了和Facebook Gorilla一样的压缩算法，能够将16个字节的数据点压缩到平均1.37个字节。
- Prometheus 2.0版本引入了全新的V3存储引擎，提供了更高的写入和查询性能 


# tsdb需要处理的问题 
## 元数据索引

## 处理旧数据
## 提前聚合
## 低延迟