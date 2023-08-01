import json
import requests


def create_silence():
    """
    页面上提交slience，查看相应的body与url
    :return {"silenceID":"85b1506f-41a9-40c0-a950-c8a460dcbfa4"}
    """

    payload = {"matchers": [{"name": "alertname", "value": "mysql_qps too high", "isRegex": False},
                            {"name": "instance", "value": "192.168.0.106:9104", "isRegex": False},
                            {"name": "job", "value": "mysqld_exporter", "isRegex": False},
                            {"name": "node_name", "value": "abc", "isRegex": False},
                            {"name": "severity", "value": "warning", "isRegex": False}],
               "startsAt": "2021-05-15T05:21:14.688Z", "endsAt": "2021-05-15T07:21:14.688Z", "createdBy": "xiaoyi",
               "comment": "test", "id": None}
    payload = {
        "matchers": [
            {
                "name": "job",
                "value": "node_exporter",
                "isRegex": False
            }
        ],
        "startsAt": "2023-07-15T05:21:14.688Z",
        "endsAt": "2023-07-21T05:21:14.688Z",
        "createdBy": "ning1875",
        "comment": "静默所有机器告警",
        "id": None
    }
    uri = "http://192.168.116.130:9093/api/v2/silences"
    res = requests.post(uri, json=payload)
    print(res.status_code)
    print(res.text)


create_silence()
