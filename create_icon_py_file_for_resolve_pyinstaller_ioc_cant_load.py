# coding=utf-8
# @auth: applex
# @date: 2018-03-28

# 当前文件为了解决pyinstaller打包后无法加载窗口图标问题
# 脚本先将图标文件按照base64编码读入icon.py中的img变量中
# 然后入口程序代码中在需要加载icon的地方调用icon.py生成tmp.ico
# 加载后删除tem.ioc

import base64
with open("logo.ico", "rb") as ico:
    b64str = base64.b64encode(ico.read())
    write_data = "img = '%s'" % b64str
    with open("logo.py", "w+") as logo:
        logo.write(write_data)
