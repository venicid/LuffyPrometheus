#!/bin/bash


systemctl stop m3dbnode
# 慎重哦
rm -rf /opt/app/m3db
# 创建目录
mkdir -p /opt/app/m3db/data/{m3db,m3kv}
# 拷贝文件
/bin/cp -f  m3dbnode /opt/app/m3db/m3dbnode
/bin/cp -f  m3dbnode_single.yaml /opt/app/m3db/m3dbnode_single.yaml
# 设置内核参数
sysctl -w vm.max_map_count=3000000
sysctl -w vm.swappiness=1
sysctl -w fs.file-max=3000000
sysctl -w fs.nr_open=3000000
ulimit -n 3000000

grep 'vm.max_map_count = 3000000' /etc/sysctl.conf || cat >> /etc/sysctl.conf <<'EOF'
# m3db
vm.max_map_count = 3000000
vm.swappiness = 1
fs.file-max = 3000000
fs.nr_open = 3000000
EOF

# 复制service文件
sudo /bin/cp -f -a m3dbnode.service /etc/systemd/system/m3dbnode.service
systemctl daemon-reload
systemctl start m3dbnode
systemctl status m3dbnode