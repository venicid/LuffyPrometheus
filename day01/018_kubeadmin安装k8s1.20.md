# 地址
- https://kuboard.cn/install/install-k8s.html
# 准备工作
```shell script

# 修改 hostname
hostnamectl set-hostname your-new-host-name
# 查看修改结果
hostnamectl status
# 设置 hostname 解析
echo "127.0.0.1   $(hostname)" >> /etc/hosts

```
