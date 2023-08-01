import json
import time
import requests
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(filename)s [func:%(funcName)s] [line:%(lineno)d]:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO"
)


def label_values(host, metric_name, exist_tag_kv, tag_key):

    uri = 'http://{}/api/v1/series'.format(host)
    end = int(time.time())
    start = end - 5 * 60
    expr= '''%s{%s}''' % (metric_name, exist_tag_kv),
    G_PARMS = {
        "match[]": expr,
        "start": start,
        "end": end,
    }
    res = requests.get(uri, G_PARMS,timeout=5)
    tag_values = set()
    if res.status_code != 200:
        msg = "[error_code_not_200]"
        logging.error(msg)
        return
    jd = res.json()
    if not jd:
        msg = "[error_loads_json]"
        logging.error(msg)
        return
    for i in jd.get("data"):
        tag_values.add(i.get(tag_key))
    msg = "\n[prometheus_host:{}]\n[expr:{}]\n[target_tag:{}]\n[num:{}][tag_values:{}]".format(
        host,
        expr,
        tag_key,
        len(tag_values),
        tag_values)
    logging.info(msg)
    return tag_values




if __name__ == '__main__':
    start = time.perf_counter()
    label_values("192.168.116.130:9090","node_uname_info",'job="node_exporter"',"instance")
    end  = time.perf_counter()
    haoshi = end-start
    print(haoshi)