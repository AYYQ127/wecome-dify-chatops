import requests
from requests.auth import HTTPBasicAuth
import time
import re

# Jenkins 服务器信息
JENKINS_URL = "http://jenkins.com" # 需要修改
# JOB_NAME = "aaaa"
USERNAME = "aaaa"  # 需要修改
API_TOKEN = "bbbbbbbbbb"  # 需要修改



def trigger_build(job_name):
    params = {"BUILDER": "ChatOps"}
    """触发 Jenkins 构建并返回 Queue ID"""
    build_url = f"{JENKINS_URL}/job/{job_name}/buildWithParameters"

    response = requests.post(build_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), params=params)

    if response.status_code != 201:
        return None

    return get_queue_id(job_name)


def get_queue_id(job_name, retries=15, delay=1):
    """查询 Queue ID"""
    queue_url = f"{JENKINS_URL}/queue/api/json"

    for _ in range(retries):
        queue_info = requests.get(queue_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN)).json()
        for item in queue_info.get("items", []):
            if item.get("task", {}).get("name") == job_name:
                return item["id"]
        time.sleep(delay)

    #print("❌ 未找到 Queue ID，构建可能失败！")
    return None


def get_build_number(queue_id, retries=15, delay=1):
    """获取 Build Number"""
    queue_item_url = f"{JENKINS_URL}/queue/item/{queue_id}/api/json"

    for _ in range(retries):
        queue_item_info = requests.get(queue_item_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN)).json()
        executable = queue_item_info.get("executable")

        if executable:
            return executable.get("number")

        print("⏳ 等待 Jenkins 分配 Build Number...")
        time.sleep(delay)

    #print("❌ 获取 Build Number 失败！")
    return None


def monitor_build_console(job_name, build_number):
    """轮询 Jenkins 控制台日志，检查构建状态"""
    console_url = f"{JENKINS_URL}/job/{job_name}/{build_number}/consoleText"

    while True:
        response = requests.get(console_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

        if response.status_code != 200:
            print(f"⚠️ 无法获取控制台日志，HTTP 状态码: {response.status_code}")
            break

        logs = response.text
        last_lines = logs.strip().split("\n")[-5:]

        if "Finished: SUCCESS" in last_lines:
            print("✅ 构建成功！")
            return {
                "result": "✅ 构建成功！",
            }
        elif any(fail_flag in last_lines for fail_flag in ["Finished: FAILURE", "Finished: ABORTED"]):
            print("❌ 构建失败！")
            return {
                "result": "❌ 构建失败！",
            }

        print("⏳ 构建进行中...")
        time.sleep(5)


def remove_chinese(text):
    # 正则表达式匹配中文字符并去除
    return re.sub(r'[\u4e00-\u9fa5]', '', text)


def main(thisquery_name: str) -> dict:
    JOB_NAME = remove_chinese(thisquery_name)

    queue_id = trigger_build(JOB_NAME)

    if queue_id is None:
        return {
            "result": "❌ 未找到 Queue ID，构建可能失败，请联系管理员查看后台日志",
        }

    build_number = get_build_number(queue_id)
    if build_number is None:
        return {
            "result": "❌ 获取 Build Number 失败！",
        }
    # 有可能是别的原因超时
    return {
        "result": "由于dify有15秒超时，请自行查看C组消息  "
                  "项目名称：" + JOB_NAME +
                  "  构建编号：" + str(build_number),
    }

    # monitor_build_console(JOB_NAME, build_number)


# if __name__ == '__main__':
#     main('帮我发版aaaaa')

