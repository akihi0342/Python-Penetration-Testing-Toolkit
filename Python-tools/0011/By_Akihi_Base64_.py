import base64

# 定义一个Base64编码的字符串
base64_code = 'aGVsbG8geHhl'
# 对Base64编码的字符串进行解码，并将结果以UTF-8编码转换为普通字符串
string = base64.b64decode(base64_code).decode('utf-8')
print(f"Base64解码后的字符串: {string}")

# 定义一个普通字符串
string = 'hello xss'
# 将普通字符串以UTF-8编码后进行Base64编码
base64_code = base64.b64encode(string.encode('utf-8'))
print(f"字符串Base64编码后的结果: {base64_code}")