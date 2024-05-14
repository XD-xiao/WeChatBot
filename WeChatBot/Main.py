from Function import Function

# 输入联系人昵称，得到聊天窗口标题
name = input("请输入联系人昵称:")

WeChatBot = Function(name)
# 输出提示信息，并且避免初次发消息出现错误
WeChatBot.iomanager.sendResult("!!!WeChatBot启动!!")
# 循环检测消息，并执行功能
while True:
    if WeChatBot.checkMessage():
        WeChatBot.chooseFunction()


