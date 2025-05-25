from Cryptodome.Cipher import AES
import binascii

# 定义AES加密所需的密钥，密钥长度必须为16字节
key = b'abcdefghabcdefgh'
# 定义需要加密的文本
text = 'zhusimaji'
# 对文本进行填充，使其长度为16的倍数，使用'='进行填充
padded_text = text + (16 - (len(text) % 16)) * '='
print(f"填充后的文本: {padded_text}")

# 创建一个AES加密对象，使用ECB模式
aes = AES.new(key, AES.MODE_ECB)
# 对填充后的文本进行加密，并将加密结果转换为十六进制字符串
encrypto_text = aes.encrypt(padded_text.encode())
encryptResult = binascii.b2a_hex(encrypto_text)
print(f"加密后的十六进制结果: {encryptResult}")

# 将十六进制的加密结果转换为二进制数据
encrypto_text = binascii.a2b_hex(encryptResult)
# 对二进制的加密数据进行解密
decryptResult = aes.decrypt(encrypto_text)
print(f"解密后的结果: {decryptResult}")