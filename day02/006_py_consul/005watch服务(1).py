import time

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

    def watch_service(self, service_name):
        index = None
        while True:
            try:
                last_index = index

                index, d = self.consul.health.service(service_name, passing=True, index=index, wait='10s')

                if last_index == index or last_index == None:
                    print('没变')
                    continue
                print("变了")
                data = d
                new_nodes = []
                num = len(data)
                print(data)
                for num_index, x in enumerate(data):
                    Service = x.get("Service")
                    address = Service.get("Address")
                    id = Service.get("ID")
                    msg = "[alive_node_detail][num:{}/{}][addr:{}][id:{}]".format(
                        num_index + 1,
                        num,
                        address,
                        id
                    )
                    print(msg)
                    logging.info(msg)
                    if address:
                        new_nodes.append(address)


            except Exception as e:
                logging.error("[watch_error,service:{},error:{}]".format(service_name, e))
                time.sleep(5)
                continue


if __name__ == '__main__':
    c_host = '192.168.116.130'
    c_port = 8500
    c = ConsulWork(c_host, c_port)
    # c.watch_service('pushgateway')
    c.watch_service('pgw')

    # step 1
    """
    首先能看到正常的两个节点信息
    2021-04-02 19:20:05 INFO 005watch服务.py watch_service [line:99]:[alive_node_detail][num:1/2][addr:172.20.70.205][id:pushgateway_172.20.70.205_9091]
    2021-04-02 19:20:05 INFO 005watch服务.py watch_service [line:99]:[alive_node_detail][num:2/2][addr:172.20.70.215][id:pushgateway_172.20.70.215_9091]
    """
    # step 2
    # 此时到机器上停止一台pushgateway服务
    # systemctl stop  pushgateway
    """
    可以看到 只有一个存活节点
    2021-04-02 19:21:08 INFO 005watch服务.py watch_service [line:99]:[alive_node_detail][num:1/1][addr:172.20.70.215][id:pushgateway_172.20.70.215_9091]
    """
    # step 3
    # 此时到机器上启动pushgateway服务
    # systemctl start  pushgateway
    """
    可以看到 又打印两个节点信息了
    2021-04-02 19:22:08 INFO 005watch服务.py watch_service [line:99]:[alive_node_detail][num:1/2][addr:172.20.70.205][id:pushgateway_172.20.70.205_9091]
    2021-04-02 19:22:08 INFO 005watch服务.py watch_service [line:99]:[alive_node_detail][num:2/2][addr:172.20.70.215][id:pushgateway_172.20.70.215_9091]
    """

    # step 4
    # 过了5分钟发现又打印了一遍两个节点
    # 这是因为consul.health.service函数有个 wait参数代表本地请求的最长时间等待时间，默认为5分钟
    # 所以我们需要根据index 是否变换判断节点到底变没变
    #             *wait* the maximum duration to wait (e.g. '10s') to retrieve
    #             a given index. this parameter is only applied if *index* is also
    #             specified. the wait time by default is 5 minutes.
    """
    2021-04-02 19:48:16 INFO 005watch服务.py watch_service [line:99]:[alive_node_detail][num:1/2][addr:172.20.70.205][id:pushgateway_172.20.70.205_9091]
    2021-04-02 19:48:16 INFO 005watch服务.py watch_service [line:99]:[alive_node_detail][num:2/2][addr:172.20.70.215][id:pushgateway_172.20.70.215_9091]
    2021-04-02 19:53:17 INFO 005watch服务.py watch_service [line:99]:[alive_node_detail][num:1/2][addr:172.20.70.205][id:pushgateway_172.20.70.205_9091]
    2021-04-02 19:53:17 INFO 005watch服务.py watch_service [line:99]:[alive_node_detail][num:2/2][addr:172.20.70.215][id:pushgateway_172.20.70.215_9091]
    """

    """
    没变
    2021-04-02 20:01:25 INFO 005watch服务.py watch_service [line:105]:[alive_node_detail][num:1/2][addr:172.20.70.205][id:pushgateway_172.20.70.205_9091]
    2021-04-02 20:01:25 INFO 005watch服务.py watch_service [line:105]:[alive_node_detail][num:2/2][addr:172.20.70.215][id:pushgateway_172.20.70.215_9091]
    没变
    2021-04-02 20:01:35 INFO 005watch服务.py watch_service [line:105]:[alive_node_detail][num:1/2][addr:172.20.70.205][id:pushgateway_172.20.70.205_9091]
    2021-04-02 20:01:35 INFO 005watch服务.py watch_service [line:105]:[alive_node_detail][num:2/2][addr:172.20.70.215][id:pushgateway_172.20.70.215_9091]
    """
