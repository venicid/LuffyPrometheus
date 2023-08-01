import requests

"""
可以把各种云的云监控信息调用alertmanager 的api 把告警接入：
1. 注册公有云消息通知服务SMN 接收推送消息
2. etl后调 /api/v1/alerts
"""
def send(host):
    uri = "http://{}:9093/api/v1/alerts".format(host)
    data = [
        {
            "labels": {
                "alertname": "eee报警测试测试",
                "group": "eeee",
                # "unionProject": "net_monitor",
                "severity": "2",
                "job": "node_exporter",
                "k1": "v1",
            },
            "annotations": {
                "value": "100ms"
            },


        },
    ]
    res = requests.post(uri,json=data)
    print(res.status_code)
    print(res.text)

send("192.168.116.130")
send("192.168.116.131")
# send("192.168.0.107")
# send("192.168.0.106")