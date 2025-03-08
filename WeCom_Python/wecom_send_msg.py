import requests
import json

# 自行修改一下参数
corpid = 'aaa'
corpsecret = 'bbb'


def get_access_token():
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    params = {
        "corpid": corpid,
        "corpsecret": corpsecret
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "access_token" in data:
            access_token = data["access_token"]
            return access_token
        else:
            print("获取 access_token 失败:", data)
    else:
        print("请求失败，HTTP 状态码:", response.status_code)


def send_app_msg(touser, content):
    acto = get_access_token()
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + acto

    print("发送消息的用户" + touser)
    print("发送的消息体" + content)

    body = {
        "touser": touser,
        "toparty": "",
        "totag": "",
        "msgtype": "text",
        "agentid": 1000001, # 自行修改一下参数
        "text": {
            "content": content
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0
    }
    response = requests.post(url, json=body)
    if response.status_code == 200:
        print("返回结果:", response.json()["errmsg"])
    else:
        print("请求失败，HTTP 状态码:", response.status_code)


# if __name__ == '__main__':
#     send_app_msg('PengYuYan', '123')
