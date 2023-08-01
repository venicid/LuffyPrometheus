import requests

rebot_hook_url = "https://oapi.dingtalk.com/robot/send?access_token=af4f6b7eb81829f56e5084a8a27ca5fd26b6c9e93b83731f8758ab7a3cc065d3"


def sent_dingtalk(content):
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "atMobiles": [
                "15810947075",
            ],
            "isAtAll": False
        }
    }
    res = requests.post(rebot_hook_url, json=data)
    print(res.status_code)
    print(res.text)
