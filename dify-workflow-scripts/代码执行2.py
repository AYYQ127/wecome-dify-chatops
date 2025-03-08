import requests


def extract_data(prometheus_url, query, key_name="instance"):
    """统一处理提取数据的逻辑，支持传递动态提取的字段"""
    response = requests.get(prometheus_url, params={'query': query})

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            return [(result["metric"].get(key_name, "unknown"), float(result["value"][1]))
                    for result in data["data"]["result"]]
    else:
        print(f"Error: {response.status_code}")
    return []


def format_output(data, unit='MB', metric_type='内存占用'):
    """格式化输出结果，支持单位转换和不同度量类型"""
    result = []
    for key_value, value in data:
        result.append(f"{key_value} {metric_type}: {value:.2f} {unit}")
    return result


def main(text: str) -> dict:
    thisquery_name = text
    # Prometheus 的 API 地址
    prometheus_urls = {
        "fs": 'http://prometheus.aaa.bbb/api/v1/query' # 需要修改
    }

    # 查询的 Prometheus 表达式
    queries = {
        "az_fs_instance_disk_query8": '(1 - node_filesystem_avail_bytes{fstype=~"ext.*|xfs",mountpoint="/k8sftp"} / node_filesystem_size_bytes{fstype=~"ext.*|xfs",mountpoint="/k8sftp"}) * 100'
    }

    # 获取并输出数据
    query = queries.get(thisquery_name)  # 直接通过查询名称获取查询语句
    if query is None:
        return {
            "result": "Error: 查询名称无效",
        }

    # 判断查询名称中是否同时包含 "az" 和 "fs"，如果包含则请求两个 API
    if "az" in thisquery_name and "fs" in thisquery_name:
        prom_types = ["fs", "az"]
        key_name = "instance"  # 对于 fs 查询，使用 container 作为 key_name
    elif "az" in thisquery_name:
        prom_types = ["az"]
        key_name = "container"  # 对于 az 查询，使用 instance 作为 key_name
    elif "fs" in thisquery_name:
        prom_types = ["fs"]
        key_name = "container"  # 对于 fs 查询，使用 container 作为 key_name
    else:
        prom_types = []
        key_name = "instance"  # 默认使用 instance 作为 key_name

    # 提取数据并输出
    result_data = []
    for prom_type in prom_types:
        # 提取数据
        data = extract_data(prometheus_urls[prom_type], query, key_name)

        # 判断是硬盘相关查询，使用百分比单位和硬盘使用率
        if "disk" in thisquery_name:
            unit = '%'
            metric_type = '磁盘使用率'
        else:
            unit = ''
            metric_type = '未知属性'

        # 获取格式化后的输出
        formatted_output = format_output(data, unit=unit, metric_type=metric_type)
        result_data.append(f"{thisquery_name} ({prom_type}):")
        result_data.extend(formatted_output)

    return {
        "result": "\n".join(result_data),
    }
