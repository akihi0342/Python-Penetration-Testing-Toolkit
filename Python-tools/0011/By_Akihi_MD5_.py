from hashlib import md5

def encrypt_md5(msg):
    """
    对输入的消息进行MD5加密
    :param msg: 待加密的消息
    :return: 加密后的十六进制字符串
    """
    # 创建一个MD5对象
    new_md5 = md5()
    # 更新MD5对象的内容，将消息以UTF-8编码后传入
    new_md5.update(msg.encode(encoding='utf-8'))
    # 返回加密后的十六进制字符串
    return new_md5.hexdigest()

if __name__ == '__main__':
    # 对指定的消息进行MD5加密并打印结果
    print(f"MD5加密结果: {encrypt_md5('Welcme to the 90s')}")