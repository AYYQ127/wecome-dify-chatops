import requests
import json


def run_workflow(user, thatquery_name):
    print("dify的用户" + user)
    print("dify的工作流参数" + thatquery_name)
    # dify.ai.com需要改
    workflow_url = "http://dify.ai.com/v1/workflows/run"
    headers = {
        "Authorization": "Bearer app-aaaaaaaa", # 这里需要修改
        "Content-Type": "application/json"
    }

    data = {
            "inputs": {
                "thisquery_name": thatquery_name
            },
            "response_mode": "blocking",
            "user": user
        }

    try:
        # print("运行工作流...")
        response = requests.post(workflow_url, headers=headers, json=data)
        if response.status_code == 200:
            # print("工作流执行成功")
            return response.json()
        else:
            print(f"工作流执行失败，状态码: {response.status_code}")
            return {"status": "error", "message": f"Failed to execute workflow, status code: {response.status_code}"}
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"status": "error", "message": str(e)}


if __name__ == '__main__':
    user = "username"
    thatquery_name = "帮我发版aaaaat"
    result = run_workflow(user, thatquery_name)
    # print(result)
    # 获取 text 内容
    text_content = result['data']['outputs']['text']
    # 去掉 ``` 标记
    text_content = text_content.replace("```", "").strip()
    text_content = text_content.strip()  # 去掉前后空白字符
    print(text_content)
