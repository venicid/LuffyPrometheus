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

'''
alertmanager webhook 



'''
web_hook_data = {'receiver': 'callback_local', 'status': 'firing', 'alerts': [
    {'status': 'firing', 'labels': {
        'alertname': 'local_alert_test', 'cluster': 'hawkeye-business-new', 'env': 'prod', 'group': 'SGT',
        'instance': '10.21.72.64:9100', 'job': 'ec2', 'local_test': 'm3coo', 'service': 'm3coordinator',
        'severity': '2'},
     'annotations': {
         'value': '6.738567168e+10'},
     'startsAt': '2020-05-12T16:01:09.758374234+08:00',
     'endsAt': '0001-01-01T00:00:00Z',
     'generatorURL': 'http://sgt-hawkeye-serverside-monitor-prod:9090/graph?g0.expr=node_memory_MemTotal_bytes%7Bcluster%3D~%22hawkeye-business-new%22%2Cservice%3D~%22m3coordinator%22%7D+%3E+0&g0.tab=1',
     'fingerprint': '749d434c689318e6'},
    {'status': 'firing', 'labels': {
        'alertname': 'local_alert_test',
        'cluster': 'hawkeye-business-new',
        'env': 'prod', 'group': 'SGT',
        'instance': '10.21.73.145:9100',
        'job': 'ec2', 'local_test': 'm3coo',
        'service': 'm3coordinator',
        'severity': '2'}, 'annotations': {
        'value': '6.738567168e+10'},
     'startsAt': '2020-05-12T16:01:09.758374234+08:00',
     'endsAt': '0001-01-01T00:00:00Z',
     'generatorURL': 'http://sgt-hawkeye-serverside-monitor-prod:9090/graph?g0.expr=node_memory_MemTotal_bytes%7Bcluster%3D~%22hawkeye-business-new%22%2Cservice%3D~%22m3coordinator%22%7D+%3E+0&g0.tab=1',
     'fingerprint': '4d84c75594729d25'},
    {'status': 'firing', 'labels': {
        'alertname': 'local_alert_test',
        'cluster': 'hawkeye-business-new',
        'env': 'prod', 'group': 'SGT',
        'instance': '10.21.78.21:9100',
        'job': 'ec2', 'local_test': 'm3coo',
        'service': 'm3coordinator',
        'severity': '2'}, 'annotations': {
        'value': '6.738567168e+10'},
     'startsAt': '2020-05-12T16:01:09.758374234+08:00',
     'endsAt': '0001-01-01T00:00:00Z',
     'generatorURL': 'http://sgt-hawkeye-serverside-monitor-prod:9090/graph?g0.expr=node_memory_MemTotal_bytes%7Bcluster%3D~%22hawkeye-business-new%22%2Cservice%3D~%22m3coordinator%22%7D+%3E+0&g0.tab=1',
     'fingerprint': 'a9f768d0b500358f'},
    {'status': 'firing', 'labels': {
        'alertname': 'local_alert_test',
        'cluster': 'hawkeye-business-new',
        'env': 'prod', 'group': 'SGT',
        'instance': '10.21.78.235:9100',
        'job': 'ec2', 'local_test': 'm3coo',
        'service': 'm3coordinator',
        'severity': '2'}, 'annotations': {
        'value': '6.738567168e+10'},
     'startsAt': '2020-05-12T16:01:09.758374234+08:00',
     'endsAt': '0001-01-01T00:00:00Z',
     'generatorURL': 'http://sgt-hawkeye-serverside-monitor-prod:9090/graph?g0.expr=node_memory_MemTotal_bytes%7Bcluster%3D~%22hawkeye-business-new%22%2Cservice%3D~%22m3coordinator%22%7D+%3E+0&g0.tab=1',
     'fingerprint': '68ebb3f9ea909c8e'},
    {'status': 'firing', 'labels': {
        'alertname': 'local_alert_test',
        'cluster': 'hawkeye-business-new',
        'env': 'prod', 'group': 'SGT',
        'instance': '10.21.78.73:9100',
        'job': 'ec2', 'local_test': 'm3coo',
        'service': 'm3coordinator',
        'severity': '2'}, 'annotations': {
        'value': '6.738567168e+10'},
     'startsAt': '2020-05-12T16:01:09.758374234+08:00',
     'endsAt': '0001-01-01T00:00:00Z',
     'generatorURL': 'http://sgt-hawkeye-serverside-monitor-prod:9090/graph?g0.expr=node_memory_MemTotal_bytes%7Bcluster%3D~%22hawkeye-business-new%22%2Cservice%3D~%22m3coordinator%22%7D+%3E+0&g0.tab=1',
     'fingerprint': 'e448a7eb906ede64'},
    {'status': 'firing', 'labels': {
        'alertname': 'local_alert_test',
        'cluster': 'hawkeye-business-new',
        'env': 'prod', 'group': 'SGT',
        'instance': '10.21.79.175:9100',
        'job': 'ec2', 'local_test': 'm3coo',
        'service': 'm3coordinator',
        'severity': '2'}, 'annotations': {
        'value': '6.738567168e+10'},
     'startsAt': '2020-05-12T16:01:09.758374234+08:00',
     'endsAt': '0001-01-01T00:00:00Z',
     'generatorURL': 'http://sgt-hawkeye-serverside-monitor-prod:9090/graph?g0.expr=node_memory_MemTotal_bytes%7Bcluster%3D~%22hawkeye-business-new%22%2Cservice%3D~%22m3coordinator%22%7D+%3E+0&g0.tab=1',
     'fingerprint': 'afe15b8c559ff790'}],
                 'groupLabels': {'alertname': 'local_alert_test'},
                 'commonLabels': {'alertname': 'local_alert_test', 'cluster': 'hawkeye-business-new', 'env': 'prod',
                                  'group': 'SGT', 'job': 'ec2', 'local_test': 'm3coo', 'service': 'm3coordinator',
                                  'severity': '2'}, 'commonAnnotations': {'value': '6.738567168e+10'},
                 'externalURL': 'http://hawkeye.ushareit.me', 'version': '4',
                 'groupKey': '{}/{local_test=~"^(?:m3coo)$"}:{alertname="local_alert_test"}'}


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
    service = commonLabels.get("service")
    app = "m3db"
    if service:
        app = service
    extra_vars = {
        "app": app,
    }

    executor = ThreadPoolExecutor(1)
    executor.submit(local_pprof, instances)
    # yaml_path = "./perf_deploy.yaml"
    dingding_msg = "默认动作 pprof :{}".format(",".join(instances))
    if "cpu" in alertname:
        yaml_path = "./perf_deploy.yaml"
        dingding_msg = '开始dump cpu:{}'.format(",".join(instances))
    elif "mem" in alertname:
        yaml_path = "./restart_service.yaml"
        dingding_msg = '回调重启服务 {}:{}'.format(app, ",".join(instances))
    else:
        pass

    res = run_play(instances, yaml_path, extra_vars=extra_vars)
    logging.info("[handle_callback] [instances:{}] [res:{}]".format(",".join(instances), json.dumps(res)))
    # logging.info("[handle_callback] [instances:{}] [res:{}]".format(",".join(instances), "local_pprof"))
    sent_dingtalk(dingding_msg)

    return jsonify(req_data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
