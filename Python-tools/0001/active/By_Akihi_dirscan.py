import requests

# 设置请求头，模拟浏览器访问
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/60.0'}

# 获取用户输入的目标 URL
url = input('请输入目标 URL: ')
# 获取用户输入的字典文件名称，若未输入则默认使用 'php.txt'
txt = input('请输入字典文件名称（默认为 php.txt）: ')

# 如果用户未输入字典文件名称，使用默认值
if not txt:
    txt = 'php.txt'

# 用于存储字典文件中的路径列表
url_list = []

try:
    # 打开字典文件
    with open(txt, 'r') as f:
        # 逐行读取文件内容
        for line in f:
            # 去除每行末尾的换行符
            line = line.strip()
            # 将处理后的路径添加到列表中
            url_list.append(line)
except FileNotFoundError:
    # 若文件未找到，打印错误信息
    print(f"错误：未找到文件 {txt}")
except Exception as e:
    # 其他异常情况，打印具体错误信息
    print(f"发生未知错误：{e}")

# 遍历路径列表
for path in url_list:
    # 拼接完整的请求 URL
    full_url = f'http://{url}/{path}'
    try:
        # 发送 GET 请求
        response = requests.get(full_url, headers=headers)
        # 打印请求的 URL 和响应状态码
        print(f'{full_url}----------------{response.status_code}')
    except requests.RequestException as e:
        # 请求异常，打印请求的 URL 和错误信息
        print(f'{full_url}----------------{e}')