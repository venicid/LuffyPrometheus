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


if __name__ == '__main__':
    c_host = '192.168.116.130'
    c_port = 8500
    c = ConsulWork(c_host, c_port)
    # 简单put get
    c.set_key_v("key_a", "value_c")

    # index,data = c.get_key_v("key_a")
    # 使用index 作为参数会阻塞住请求
    # 直到有数据更新或者超时
    # c.block_get_key_v("key_a", index)
