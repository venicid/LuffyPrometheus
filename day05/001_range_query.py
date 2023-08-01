import json
import time
import requests
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(filename)s [func:%(funcName)s] [line:%(lineno)d]:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO"
)


def ins_query(host,expr="node_load1"):
    start_ts = time.perf_counter()
    uri="http://{}/api/v1/query_range".format(host)
    end = int(time.time())
    minutes = 5 * 12
    start = end - minutes * 60

    # step = 20 * (1 + minutes // 60)
    step = 30
    G_PARMS = {
        "query": expr,
        "start": start,
        "end": end,
        "step": step
    }
    res = requests.get(uri, G_PARMS)

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
        step,
        result_series
    )
    logging.info(msg)
if __name__ == '__main__':
    ins_query("192.168.43.114:9090")