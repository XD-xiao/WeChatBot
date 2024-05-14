import os
import time
from pywinauto.application import Application


class IOManager:
    dlg = None

    def __init__(self, title):
        try:
            # 连接窗口，并保存
            app = Application('uia').connect(title_re=title)
            self.dlg = app.window(title_re=title)
            print("程序启动")
        except:
            print("OS:未找到窗口")

    def getchatMessage(self):
        # 获取聊天所有信息
        list_box = self.dlg.child_window(control_type="List")
        # 获取最后一条消息
        item = list_box.children(control_type="ListItem")[-1]
        # 返回消息文本
        return item.window_text()

    def sendResult(self, res):
        # 输入消息
        time.sleep(0.5)
        self.dlg["Edit"].type_keys(res)
        print("OS发送信息:" + res)
        time.sleep(1)
        # 点击发送按钮
        send_button = self.dlg.child_window(title="发送(S)", control_type="Button")
        if send_button.exists():
            print("OS:找到发送按钮")
            send_button.click_input()
        else:
            print("OS:未找到发送按钮")

    def sendFile(self, file_Path):
        time.sleep(1)
        file_button = self.dlg.child_window(title="发送文件", control_type="Button")

        # 判断文件是否存在
        if os.path.exists(file_Path):
            # 点击发送文件按钮
            file_button.click_input()
            # 连接打开文件窗口，并操作
            openapp = Application(backend='win32').connect(title_re='打开')
            win = openapp['打开']
            input = win.child_window(class_name="Edit")
            input.click_input()
            input.type_keys(file_Path, with_spaces=True)
            win.child_window(title="打开(&O)", class_name="Button").click_input()

            time.sleep(1)
            send_button = self.dlg.child_window(title="发送（1）", control_type="Button")
            # 判断发送按钮是否存在，以确定是否可以发送文件
            if send_button.exists():
                send_button.click_input()
                self.sendResult("发送成功")
            else:
                yes_button = self.dlg.child_window(title="确定", control_type="Button")
                if yes_button.exists():
                    yes_button.click_input()
                else:
                    print("确认按钮不存在")
                self.sendResult("文件无法发送")
        else:
            self.sendResult("文件不存在")
