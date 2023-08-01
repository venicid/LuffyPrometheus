> 准备node机器
```shell script
# 机器2
hostnamectl set-hostname prome-node01
```

> 节点主机名写入hosts
```shell script


echo "192.168.116.130   prome-master01" >> /etc/hosts
echo "192.168.116.131   prome-node01" >> /etc/hosts


``` 

> master上生成ssh key 并拷贝到node上
```shell script
# 全部yes
ssh-keygen

ssh-copy-id prome-node01

# 测试ssh联通
ssh prome-node01


ssh-copy-id prome-master01
ssh prome-master01
```



> master 上安装ansible
```shell script
yum install -y ansible

# 关闭hostcheck 
vim /etc/ansible/ansible.cfg

ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no 

```

> playbook执行时需要设置机器文件 
```shell script
cat <<EOF > /opt/tgzs/host_file
prome-master01
prome-node01
EOF

# 测试
ansible -i host_file all -m ping
```

导入本地的service目录的文件到/opt/tgzs目录下

>  设置syslog 和logrotate服务
```shell script
ansible-playbook -i host_file init_syslog_logrotate.yaml

# check
ll /etc/rsyslog.d/
cat /etc/rsyslog.d/syslog_server.conf 

ll /etc/logrotate.d/
cat /etc/logrotate.d/logrotate.conf
```

> 编写ansible 发布服务脚本
```shell script

ansible-playbook -i host_file  service_deploy.yaml  -e "tgz=node_exporter-1.1.2.linux-amd64.tar.gz" -e "app=node_exporter"

```

> 检查node_exporter服务状态
```shell script

ansible -i host_file all -m shell -a " ps -ef |grep node_exporter|grep -v grep "

ansible -i host_file all -m shell -a " ss -ntlp | grep 9100"

less /opt/logs/node_exporter.log
```
> 浏览器访问 9100/metrics
```shell script

node01.prome.me:9100/metrics
master01.prome.me:9100/metrics

# 提前关闭防火墙
http://192.168.116.130:9100/metrics
http://192.168.116.131:9100/metrics
```