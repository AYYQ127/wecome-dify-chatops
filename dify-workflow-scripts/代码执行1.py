def main(thisquery_name: str) -> dict:
    query_mapping = {
        "/k8sftp分区": "az_fs_instance_disk_query8",
        "发版": "发版",
        "Deepseek": "Deepseek"
    }

    # 其他匹配项
    result = next((v for k, v in query_mapping.items() if k in thisquery_name),
                  "找不到匹配的选项，YFos还在学习中，请到dify工作流中配置'" + thisquery_name + "'相关流程")

    return {"result": result}
