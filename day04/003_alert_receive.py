import json

from flask import request, Flask, jsonify, redirect
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(filename)s [func:%(funcName)s] [line:%(lineno)d]:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO"
)

app = Flask(__name__)

"""
2021-05-02 10:40:31 INFO a.py [func:push_metrics_redirect] [line:28]:[host:127.0.0.1:5001][path:/alert][data:b'{"receiver":"web\\\\.hook","status":"firing","alerts":[{"status":"firing","labels":{"alertname":"node_load","instance":"192.168.43.114:9100","job":"node_exporter","severity":"critical"},"annotations":{"summary":"\xe6\x9c\xba\xe5\x99\xa8\xe5\xa4\xaa\xe7\xb4\xaf\xe4\xba\x86"},"startsAt":"2021-05-02T02:39:16.628934947Z","endsAt":"0001-01-01T00:00:00Z","generatorURL":"http://prome-master01:9090/graph?g0.expr=node_load1+%3E+0\\u0026g0.tab=1","fingerprint":"40ee791929e72e8b"}],"groupLabels":{"alertname":"node_load"},"commonLabels":{"alertname":"node_load","instance":"192.168.43.114:9100","job":"node_exporter","severity":"critical"},"commonAnnotations":{"summary":"\xe6\x9c\xba\xe5\x99\xa8\xe5\xa4\xaa\xe7\xb4\xaf\xe4\xba\x86"},"externalURL":"http://prome-master01:9093","version":"4","groupKey":"{}:{alertname=\\"node_load\\"}","truncatedAlerts":0}\n']
2021-05-02 10:40:31 INFO _internal.py [func:_log] [line:113]:127.0.0.1 - - [02/May/2021 10:40:31] "POST /alert HTTP/1.1" 200 -

data = {'receiver': 'web\\.hook', 'status': 'resolved', 'alerts': [{'status': 'resolved',
                                                                    'labels': {'alertname': 'node_load',
                                                                               'instance': '192.168.43.114:9100',
                                                                               'job': 'node_exporter',
                                                                               'severity': 'critical'},
                                                                    'annotations': {'summary': '机器太累了'},
                                                                    'startsAt': '2021-05-02T02:39:16.628934947Z',
                                                                    'endsAt': '2021-05-02T02:54:31.628934947Z',
                                                                    'generatorURL': 'http://prome-master01:9090/graph?g0.expr=node_load1+%3E+0&g0.tab=1',
                                                                    'fingerprint': '40ee791929e72e8b'},
                                                                   {'status': 'resolved',
                                                                    'labels': {'alertname': 'node_load',
                                                                               'instance': '192.168.43.2:9100',
                                                                               'job': 'node_exporter',
                                                                               'severity': 'critical'},
                                                                    'annotations': {'summary': '机器太累了'},
                                                                    'startsAt': '2021-05-02T02:41:46.628934947Z',
                                                                    'endsAt': '2021-05-02T02:46:16.628934947Z',
                                                                    'generatorURL': 'http://prome-master01:9090/graph?g0.expr=node_load1+%3E+0&g0.tab=1',
                                                                    'fingerprint': '0fd88a48463c0b87'}],
        'groupLabels': {'alertname': 'node_load'},
        'commonLabels': {'alertname': 'node_load', 'job': 'node_exporter', 'severity': 'critical'},
        'commonAnnotations': {'summary': '机器太累了'}, 'externalURL': 'http://prome-master01:9093', 'version': '4',
        'groupKey': '{}:{alertname="node_load"}', 'truncatedAlerts': 0}
"""


@app.route('/alert', methods=['GET', 'PUT', 'POST'])
# @app.route('/', methods=['GET', 'PUT', 'POST'])
def push_metrics_redirect():
    req_data = request.data
    req_path = request.path
    req_host = request.host
    msg = "[host:{}][path:{}][data:{}]".format(
        req_host,
        req_path,
        req_data,

    )
    logging.info(msg)
    return jsonify("haha"), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True, processes=1)
    """
    修改配置文件中的webhook的 alert的url
    reload prometheus
    运行该py文件
    启动alerttm_send.py文件
    查看日志and页面，已经收到告警
    """
