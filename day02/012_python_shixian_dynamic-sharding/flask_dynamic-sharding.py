import time
from consul_work_n import Consul
from consistent_hash_ring import ConsistentHashRing
import yaml
from flask import request, Flask, jsonify, redirect
from multiprocessing import Process, Queue, Pool, Manager
import logging

"""
2021-04-08 19:48:31 INFO consul_work_n.py [func:watch_service] [line:70]:[new_num:1 old_num:2][new_nodes:172.20.70.215 old_nodes:172.20.70.205:9091,172.20.70.215:9091]
2021-04-08 19:48:37 INFO flask_01.py [func:push_metrics_redirect] [line:43]:[req_path:/metrics/job/test_job][target_node:172.20.70.215][next_url:http://172.20.70.215/metrics/job/test_job]
2021-04-08 19:48:37 INFO _internal.py [func:_log] [line:113]:127.0.0.1 - - [08/Apr/2021 19:48:37] "GET /metrics/job/test_job HTTP/1.1" 302 -
2021-04-08 19:48:46 WARNING consul_work_n.py [func:watch_service] [line:60]:[节点变化，需要收敛][service:pushgateway]
2021-04-08 19:48:46 INFO consul_work_n.py [func:watch_service] [line:70]:[new_num:2 old_num:1][new_nodes:172.20.70.205,172.20.70.215 old_nodes:172.20.70.215]
2021-04-08 19:48:51 INFO flask_01.py [func:push_metrics_redirect] [line:43]:[req_path:/metrics/job/test_job][target_node:172.20.70.205][next_url:http://172.20.70.205/metrics/job/test_job]
2021-04-08 19:48:51 INFO _internal.py [func:_log] [line:113]:127.0.0.1 - - [08/Apr/2021 19:48:51] "GET /metrics/job/test_job HTTP/1.1" 302 -
"""

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(filename)s [func:%(funcName)s] [line:%(lineno)d]:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO"
)
service_hash_map = None
app = Flask(__name__)


def load_base_config(yaml_path):
    with open(yaml_path, encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


@app.route('/query', methods=['GET'])
def query():
    return jsonify("haha"), 200


@app.route('/metrics/job/<job_name>', methods=['GET', 'PUT', 'POST'])
def push_metrics_redirect(job_name):
    req_path = request.path
    hash_ring = service_hash_map['pushgateway']
    target_node = hash_ring.get_node(str(req_path))

    next_url = "http://{}{}".format(target_node, req_path)
    msg = "[req_path:{}][target_node:{}][next_url:{}]".format(
        req_path,
        target_node,
        next_url
    )
    logging.info(msg)
    return redirect(next_url, code=307)


def watch_func():
    while True:
        print("mock_watch")
        time.sleep(5)


def main_run():
    manager = Manager()

    # 2. 创建一个 全局一致性哈希map
    global service_hash_map
    service_hash_map = manager.dict()
    yaml_path = './dynamic-sharding.yml'
    config = load_base_config(yaml_path)
    # 初始化consul
    consul_host = config.get("consul_server").get("host")
    consul_port = config.get("consul_server").get("port")
    consul_obj = Consul(consul_host, consul_port)
    service_name = config.get('consul_server').get('register_service_name')

    # 注册服务
    pgw_port = config.get("pushgateway").get("port")
    print(pgw_port)
    ggw_nodes = config.get("pushgateway").get("servers")
    all_service = consul_obj.get_all_service()
    for host in ggw_nodes:
        one_service_id = "{}_{}_{}".format(service_name, host, pgw_port)
        this_service = all_service.get(one_service_id)
        if not this_service:
            # 说明服务不存在，需要注册

            res = consul_obj.register_service(
                service_name, host, int(pgw_port)
            )
            logging.info("[new_service_need_register][register_service_res:{}][service:{}][node:{},port:{}]".format(
                res, service_name, host, pgw_port
            ))
    # 给新注册的服务探测时间
    time.sleep(1)
    alive_nodes = consul_obj.get_service_health_node(service_name)

    alive_nodes = ["{}:{}".format(h, pgw_port) for h in alive_nodes]
    print(alive_nodes)
    ring = ConsistentHashRing(1000, alive_nodes)
    service_hash_map[service_name] = ring

    # 开启consul watch
    p_watch = Process(target=consul_obj.watch_service, args=(service_name, service_hash_map))
    p_watch.start()


if __name__ == '__main__':
    main_run()

    app.run(host='0.0.0.0', port=5003, threaded=True, processes=1)
