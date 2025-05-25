#!/usr/bin/python3
# -*- coding: utf-8 -*-

import itertools

def read_information_list():
    """
    读取个人信息文件，并将信息存入全局列表 infolist
    """
    try:
        # 以只读模式打开个人信息文件
        with open('person_information', 'r') as information_file:
            # 逐行读取文件内容
            lines = information_file.readlines()
            for line in lines:
                # 去除每行首尾空格，并按冒号分割，取第二部分存入 infolist
                infolist.append(line.strip().split(':')[1])
    except Exception as e:
        # 打印异常信息和错误提示
        print(f"{e}\n")
        print("读取个人信息文件时出错！")

def create_number_list():
    """
    创建数字列表，包含所有 3 位数字的组合
    """
    # 定义数字字符集
    words = "0123456789"
    # 利用 itertools 生成所有 3 位数字的排列组合
    itertools_number_list = itertools.product(words, repeat=3)
    for number in itertools_number_list:
        # 将组合转换为字符串并添加到数字列表中
        numberList.append("".join(number))

def add_top_pwd():
    """
    读取常见密码文件，并将其内容写入字典文件
    """
    try:
        # 以只读模式打开常见密码文件
        with open('TopPwd', 'r') as information_file:
            # 逐行读取文件内容
            lines = information_file.readlines()
            for line in lines:
                # 将每行内容写入字典文件
                dictionaryFile.write(line)
    except Exception as e:
        # 打印异常信息和错误提示
        print(f"{e}\n")
        print("读取常见密码文件时出错！")

def create_special_list():
    """
    创建特殊字符列表
    """
    # 定义特殊字符集
    special_words = "`~!@#$%^&*()?|/><,."
    for char in special_words:
        # 将每个特殊字符添加到特殊字符列表中
        specialList.append(char)

def combination():
    """
    组合个人信息、数字和特殊字符，生成密码字典
    """
    for a in range(len(infolist)):
        # 如果个人信息长度大于等于 8 位，直接写入字典文件
        if len(infolist[a]) >= 8:
            dictionaryFile.write(f"{infolist[a]}\n")
        else:
            # 计算需要补充的字符数量
            need_words = 8 - len(infolist[a])
            # 生成所有可能的补充字符组合
            for b in itertools.permutations("1234567890", need_words):
                # 将个人信息和补充字符组合后写入字典文件
                dictionaryFile.write(f"{infolist[a]}{''.join(b)}\n")
        # 个人信息两两组合
        for c in range(0, len(infolist)):
            if len(infolist[a] + infolist[c]) >= 8:
                # 将组合后的信息写入字典文件
                dictionaryFile.write(f"{infolist[a]}{infolist[c]}\n")
        # 个人信息与特殊字符组合
        for d in range(0, len(infolist)):
            for e in range(0, len(specialList)):
                combined = f"{infolist[a]}{specialList[e]}{infolist[d]}"
                if len(combined) >= 8:
                    # 特殊字符在中间的组合写入字典文件
                    dictionaryFile.write(f"{infolist[a]}{infolist[d]}{specialList[e]}\n")
                    # 特殊字符在头部的组合写入字典文件
                    dictionaryFile.write(f"{infolist[a]}{specialList[e]}{infolist[d]}\n")
                    # 特殊字符在尾部的组合写入字典文件
                    dictionaryFile.write(f"{specialList[e]}{infolist[a]}{infolist[d]}\n")
    # 关闭字典文件
    dictionaryFile.close()

if __name__ == '__main__':
    # 以写入模式打开字典文件
    dictionaryFile = open('passwords', 'w')
    # 存储个人信息的列表
    infolist = []
    # 存储数字组合的列表
    numberList = []
    # 存储特殊字符的列表
    specialList = []
    # 读取个人信息文件
    read_information_list()
    # 创建数字列表
    create_number_list()
    # 创建特殊字符列表
    create_special_list()
    # 将常见密码写入字典文件
    add_top_pwd()
    # 组合信息生成密码字典
    combination()
    print('\n' + u"字典生成成功！" + '\n' + '\n' + u"字典文件名：passwords")