import consul
import asyncio
import logging

logging.basicConfig(
    # TODO console 日志,上线时删掉
    # filename=LOG_PATH,
    format='%(asctime)s %(levelname)s %(filename)s %(funcName)s [line:%(lineno)d]:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO"
)


class ConsulWork(object):
    def __init__(self, host, port):
        self.consul = consul.Consul(host, port)

    def set_key_v(self, key, value):
        res = self.consul.kv.put(key, value)
        msg = "[set_key_v_res][key:{}][value:{}][res:{}]".format(

            key,
            value,
            res,

        )
        logging.info(msg)

    def get_key_v(self, key):
        index, data = self.consul.kv.get(key)
        msg = "[get_key_v_res][key:{}][index:{}][data:{}]".format(
            key,
            index,
            data,
        )
        logging.info(msg)
        return index, data

    def block_get_key_v(self, key, index):
        index, data = self.consul.kv.get(key, index=index)
        msg = "[block_get_key_res][key:{}][index:{}][data:{}]".format(
            key,
            index,
            data,
        )
        logging.info(msg)
        return index, data

    def register_service(self, name, host, port, tags=None):
        tags = tags or []
        # 注册服务
        id = "{}_{}_{}".format(name, host, port)
        return self.consul.agent.service.register(
            name,
            id,
            host,
            port,
            tags,
            # 健康检查ip端口，检查时间：5,超时时间：30，注销时间：30s
            # check=consul.Check().tcp(host, port, "5s", "5s", "60s"))
            check=consul.Check().tcp(host, port, "5s", "5s"))


    def register_service_with_deregister(self, name, host, port, tags=None):
        tags = tags or []
        # 注册服务
        id = "{}_{}_{}".format(name, host, port)
        return self.consul.agent.service.register(
            name,
            id,
            host,
            port,
            tags,
            # 健康检查ip端口，检查时间：5,超时时间：30，注销时间：15s
            # 意思是15秒后 还是检测失败就自动注销掉服务
            check=consul.Check().tcp(host, port, "5s", "5s", "15s"))
            # check=consul.Check().tcp(host, port, "5s", "5s"))



if __name__ == '__main__':
    c_host = '192.168.116.130'
    c_port = 8500
    c = ConsulWork(c_host, c_port)
    res1 = c.register_service("pgw", '192.168.116.130', 9091)
    # res2 = c.register_service_with_deregister("pushgateway", '172.20.70.205', 9991)
    res2 = c.register_service("pgw", '192.168.116.131', 9091)
    print(res1,res2)


"""
# 停止某个server,观察
[root@prome-node01 ~]# systemctl status pushgateway
[root@prome-node01 ~]# systemctl stop pushgateway

"""