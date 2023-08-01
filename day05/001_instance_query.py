import json
import time

import requests
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(filename)s [func:%(funcName)s] [line:%(lineno)d]:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO"
)


def ins_query(host,expr="node_disk_reads_merged_total"):
    start_ts = time.perf_counter()
    uri="http://{}/api/v1/query".format(host)
    g_parms = {
        "query": expr,
    }
    res = requests.get(uri, g_parms)

    if res.status_code!=200:
        msg = "[error_code_not_200]"
        logging.error(msg)
        return
    jd = res.json()
    if not jd:
        msg = "[error_loads_json]"
        logging.error(msg)
        return
    inner_d = jd.get("data")
    if not inner_d:
        return

    result = inner_d.get("result")
    result_series = len(result)
    end_ts = time.perf_counter()
    for index,x in enumerate(result):
        msg = "[series:{}/{}][metric:{}]".format(
            index+1,
            result_series,
            json.dumps(x.get("metric"),indent=4)
        )
        logging.info(msg)
    msg = "Load time: {}  Resolution: {}s   Result series: {}".format(
        end_ts-start_ts,
        15,
        result_series
    )
    logging.info(msg)
if __name__ == '__main__':
    ins_query("192.168.0.106:9090",expr='''max(rate(node_network_receive_bytes_total{origin_prometheus=~"",job=~"node_exporter"}[2m])*8) by (instance)''')