
# 创建etcd证书
kubectl create secret generic etcd-certs --from-file=/etc/kubernetes/pki/etcd/healthcheck-client.crt --from-file=/etc/kubernetes/pki/etcd/healthcheck-client.key --from-file=/etc/kubernetes/pki/etcd/ca.crt -n kube-system

# 节点上创建prometheus数据目录
mkdir /data/prometheus
chown -R 65534:65534 /data/prometheus

# pv.yaml中 节点选择器，填写 node的hostname
