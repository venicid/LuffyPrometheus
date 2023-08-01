import requests
import logging

logging.basicConfig(
    # TODO console 日志,上线时删掉
    # filename=LOG_PATH,
    format='%(asctime)s %(levelname)s %(filename)s %(funcName)s [line:%(lineno)d]:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO"
)


def get_high_can(host, res_dic):
    uri = "http://{}/api/v1/status/tsdb".format(host)

    res = requests.get(uri)

    if res.status_code != 200:
        msg = "[error_code_not_200]"
        logging.error(msg)
        return res_dic
    jd = res.json()
    if not jd:
        msg = "[error_loads_json]"
        logging.error(msg)
        return res_dic
    inner_d = jd.get("data")
    if not inner_d:
        return res_dic

    hi_result = inner_d.get("seriesCountByMetricName")
    if not hi_result:
        return res_dic
    for x in hi_result:
        metric_name, num = x.get("name"), int(x.get("value"))
        if not res_dic.get(metric_name):
            res_dic[metric_name] = 0
        res_dic[metric_name] += num
    return res_dic

def dic_top_10():
    d = {
        "a":1,
        "b":2,
        "c":3,
        "d":4,
        "e":5,
    }
    a1 = sorted(d.items(),key = lambda x:x[1],reverse = True)

    print(a1)
if __name__ == '__main__':
    res_dic = {}
    res_dic = get_high_can("192.168.43.114:9090", res_dic)
    print(res_dic)
    dic_top_10()