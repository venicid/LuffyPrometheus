import json
import logging
import os
import time

from ansi_api_28 import AnsibleApi
from dingtalk import sent_dingtalk
from concurrent.futures import ThreadPoolExecutor
from flask import request, Flask, jsonify, redirect

LOG_PATH = "./app.log"
LOG_LEVEL = "DEBUG"
logging.basicConfig(
    # console 日志
    filename=LOG_PATH,
    format='%(asctime)s %(levelname)s %(filename)s %(funcName)s [line:%(lineno)d]:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level=LOG_LEVEL)

app = Flask(__name__)



def run_play(ips, yaml_path, extra_vars=dict):
    t = AnsibleApi()
    t.playbookrun(ips, [yaml_path], extra_vars)
    return t.get_result()


def now_date_str_new():
    return time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))


def local_pprof(ips):
    file_name = "m3_pprof_{}".format(now_date_str_new())
    with open(file_name, 'w') as f:
        f.write("\n".join(ips))
    cmd = "/bin/bash m3_pprof.sh {} {}".format(file_name, "./pprof/")
    logging.info("local_pprof_cmd:{}".format(cmd))
    os.popen(cmd)


@app.route('/alert/callback', methods=['GET', 'POST'])
def handle_callback():
    r = request.data
    req_data = json.loads(r)

    print("111111111111111")
    print(req_data)

    alerts = req_data.get("alerts")
    commonLabels = req_data.get("commonLabels")
    instances = []
    for x in alerts:
        if x.get("status") != "firing":
            continue
        labels = x.get("labels")
        if not labels:
            continue
        instances.append(labels.get("instance").split(":")[0])
    alertname = commonLabels.get("alertname")
    service = commonLabels.get("job")
    app = ""
    if service:
        app = service
    extra_vars = {
        "app": app,
    }

    print("22222")

    print(alertname)
    print(app)

    yaml_path = "./perf_deploy.yaml"
    dingding_msg = "默认动作 pprof :{}".format(",".join(instances))
    if "cpu" in alertname:
        yaml_path = "./perf_deploy.yaml"
        dingding_msg = '开始dump cpu:{}'.format(",".join(instances))
    elif "mem" in alertname:
        yaml_path = "./restart_service.yaml"
        dingding_msg = '回调重启服务 {}:{}'.format(app, ",".join(instances))
    else:
        pass

    print(333333)
    print(instances)
    print(yaml_path)
    print(extra_vars)

    res = run_play(instances, yaml_path, extra_vars=extra_vars)

    print(44444444444)
    print(res)
    logging.info("[handle_callback] [instances:{}] [res:{}]".format(",".join(instances), json.dumps(res)))
    # logging.info("[handle_callback] [instances:{}] [res:{}]".format(",".join(instances), "local_pprof"))
    # sent_dingtalk(dingding_msg)

    return jsonify(req_data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
