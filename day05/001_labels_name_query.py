import json
import time
import requests
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(filename)s [func:%(funcName)s] [line:%(lineno)d]:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO"
)


def label_names(host, expr=""):

    uri = 'http://{}/api/v1/labels'.format(host)
    end = int(time.time())
    start = end - 5 * 60

    G_PARMS = {
        # "match[]": expr,
        "start": start,
        "end": end,
    }
    if expr:
        G_PARMS["match[]"] = expr
    res = requests.get(uri, G_PARMS)
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
    label_names_num = len(jd.get("data"))
    msg = "[series_selector:{}][label_names_num:{}][they are:{}]".format(
        expr,
        label_names_num,
        json.dumps(jd.get("data"),indent=4)
    )
    logging.info(msg)




if __name__ == '__main__':
    # label_names("192.168.43.114:9090","node_uname_info")
    label_names("192.168.116.130:9090","node_cpu_seconds_total")