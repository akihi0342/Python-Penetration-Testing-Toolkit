

# Python渗透测试工具集

## 项目简介

本项目致力于使用Python 3.9对常用渗透测试工具进行全面复现，是渗透测试与Python安全编程学习的优质资源。项目遵循"权衡工具与编程，实现最高效渗透测试"的理念，同时追求"不依赖工具，达到渗透测试最高境界"的目标。

所有工具和脚本均可直接用于实战环境，同时也是学习Python安全编程的理想范例。代码设计注重模块化与可扩展性，便于学习者理解渗透测试原理与Python编程技巧的结合。

## 适用环境

- **操作系统**: Kali Linux
- **Python版本**: Python 3.9
- **依赖库**: 项目各模块所需依赖将在后续补充

## 项目结构

### 第1章 渗透测试框架
1. **POC脚本**: 概念验证脚本框架
2. **EXP脚本**: 漏洞利用脚本框架
3. **可执行文件转换**: 将Python脚本转换为可执行文件的方法

### 第2章 信息搜集
#### 被动信息搜集
1. DNS解析工具
2. 子域名挖掘工具
3. 邮件地址爬取工具

#### 主动信息搜集
1. 基于ICMP的主机发现
2. 基于TCP/UDP的主机发现
3. 基于ARP的主机发现
4. 端口探测工具
5. 服务识别工具
6. 操作系统识别工具
7. 敏感目录探测工具

### 第3章 漏洞检测与防御
#### 未授权访问漏洞
1. Redis未授权访问漏洞利用
2. Redis未授权访问漏洞检测方法

#### 外部实体注入漏洞
1. XXE漏洞检测方法

#### SQL盲注漏洞
1. 基于布尔型的SQL盲注检测
2. 基于时间型的SQL盲注检测

#### SQLMap Tamper脚本
1. Tamper脚本编写基础
2. 高级Tamper脚本编写技巧

#### 服务器端请求伪造漏洞
1. SSRF漏洞检测方法
2. SSRF网络代理工具

### 第4章 数据加密
1. Base64编码/解码工具
2. DES加密/解密实现
3. AES加密/解密实现
4. MD5哈希计算工具

### 第5章 身份认证
1. 社会工程学密码字典生成器
2. Web后台弱口令检测脚本
3. SSH口令破解脚本
4. FTP口令破解脚本

### 第6章 模糊测试
1. 安全狗绕过技术
2. 模糊测试与WebShell结合技术

### 第7章 流量分析
1. 流量嗅探工具
2. ARP毒化工具
3. DoS攻击工具
   - 数据链路层DoS攻击
   - 网络层DoS攻击
   - 传输层DoS攻击
   - 应用层DoS攻击

### 第8章 Python免杀技术
1. Shellcode生成工具
2. Shellcode加载与执行技术
3. 常见免杀方法实现

### 第9章 远程控制工具
#### Socket网络编程
1. TCP服务端/客户端实现
2. UDP服务端/客户端实现
3. 文件传输服务器示例

#### 远程控制工具
1. 被控端程序实现
2. 主控端程序实现

## 使用说明

每个章节的工具和脚本均为独立模块，可根据需要单独使用。使用前请确保已安装所需依赖库（后续将提供详细安装指南）。

部分工具可能需要root权限才能正常运行，请在Kali Linux环境下以适当权限执行。

## 学习资源

本项目不仅是实用工具集，也是学习Python安全编程的绝佳资源。每个模块均附带详细注释，解释渗透测试原理和Python实现细节。

建议配合相关安全书籍和在线教程学习，以获得更深入的理解。

## 注意事项

1. 本项目仅用于安全研究与教学，请勿用于未经授权的渗透测试。
2. 使用任何渗透测试工具前，必须获得目标系统所有者的明确授权。
3. 作者不对因使用本项目工具造成的任何损失负责。

## 贡献

欢迎安全研究人员和Python开发者贡献代码或提出改进建议。请遵循项目的贡献指南进行提交。

