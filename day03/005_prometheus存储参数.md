# 访问prometheus flags api 查看支持的存储参数



|  参数名   | 含义 |默认值  | 说明| 
|  ----  | ----  | ---- | ---- |
| storage.remote.flush-deadline | 在关闭或配置重新加载时等待存储刷盘的时间 |	1分钟 |   可以依据数据量调整    |  
| storage.remote.read-concurrent-limit | 远程读取调用的并发qps， 0表示没有限制。 |	10 |  保护后端存储，避免被高并发打垮  |  
| storage.remote.read-max-bytes-in-frame | 远程读取流中，在解码数据前，单个帧中的最大字节数。请注意，客户端也可能会限制帧大小。默认为protobuf建议的1MB。 |	1M|  保护后端存储，避免被高并发打垮  |  
| storage.remote.read-sample-limit |在单个查询中要通过远程读取接口返回的最大样本总数。 0表示没有限制。对于流式响应类型，将忽略此限制。 |	10 |  保护后端存储，避免被高并发打垮  |  
| storage.tsdb.allow-overlapping-blocks |允许重叠的块，从而启用垂直压缩和垂直查询合并 |	false |    |  
| storage.tsdb.max-block-duration |压实块的时间范围上限 用于测试。 |	（默认为保留期的10％。） |    |  
| storage.tsdb.min-block-duration |数据块在保留之前的最小持续时间。用于测试。 |	 |    |  
| storage.tsdb.no-lockfile |不要在数据目录中创建锁文件。 |false	 |    |  
| storage.tsdb.path |数据目录path |  默认为进程运行目录的data	 |    |  
| storage.tsdb.retention.time |保存样品的时间。当设置此标志时，它将覆盖“storage.tsdb.retention”。如果既没有这个标志，也没有“storage.tsdb”。保留”也不“storage.tsdb.retention。设置大小，保留时间默 认为15d。支持单位:y, w, d, h, m, s, ms。 | 保留时间默 认为15d	 |    |  
| storage.tsdb.retention.size | 大小[实验]块可以存储的最大字节数。需要一个单位，支持单位:B, KB, MB, GB, TB, PB, EB。例:“512 mb”。这个标志是实验性的，可以在以后的版本中更改| 	 |    |  
| storage.tsdb.wal-compression |  开启wal snappy压缩 | 	true |    |  
| storage.tsdb.wal-segment-size | wal文件大小 | 	默认128M |    |  


