import os
import re
import subprocess
import time
from pycaw.utils import AudioUtilities
from nltk.chat.util import Chat, reflections
from fuzzywuzzy import fuzz
from IOManager import IOManager


class Function(object):
    iomanager = None
    message = None
    loaded_pairs = []
    chatbot = None

    def __init__(self, name):
        # 初始化IOManager，用来输入输出
        self.iomanager = IOManager(name)
        # 读取聊天模板
        with open('AIDialogueTemplate.txt', 'r') as file:
            for line in file:
                self.loaded_pairs.append(eval(line.strip()))
        # 初始化聊天机器人
        self.chatbot = Chat(self.loaded_pairs, reflections)
        pass

    def getMessage(self):
        return self.message

    def setMessage(self, message):
        self.message = message

    def checkMessage(self):
        mySession = None
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            # 找到指定会话，并保证是发声状态
            if session.Process is not None and session.Process.name() == "WeChat.exe":
                mySession = session

        # 判断指定进程是否存在
        while True:
            time.sleep(0.5)
            if mySession.State == 1:
                return True
            elif mySession is None:
                print("未找到进程")
                return False

    # 获取新的消息
    def getNewMessage(self):
        return self.iomanager.getchatMessage()

    # 分析文本
    def analyzeText(self):
        # 编写脚本：编写脚本XXXXX
        # 发送文件: 发送X盘的XXXXX

        if self.message.startswith("编写脚本"):
            self.setMessage(self.message[4:])
            # 删除message中空格、回车等空白字符
            self.setMessage(self.message.strip())
            return 2
        elif self.message.startswith("发送文件"):
            self.setMessage(self.message[4:])
            self.setMessage(self.message.strip())

            # 匹配盘符和文件名
            match = re.match(r'(?P<drive>[A-Z])盘中(?P<filename>.*)', self.message)
            if match:
                print(f"盘符: {match.group('drive')}, 文件名: {match.group('filename')}")
                drive_letter = match.group('drive')
                filename = match.group('filename')
                # 获取盘符
                drive_path = f'{drive_letter}:\\'
                # 遍历盘符下的所有文件和文件夹
                for root, dirs, files in os.walk(drive_path):
                    # 检查当前目录名是否包含指定的部分文件夹名
                    if filename in files:
                        print(f'OS:找到文件: {os.path.join(root, filename)}')
                        self.setMessage(os.path.join(root, filename))
                        return 3
                # 未找到文件
                self.iomanager.sendResult('未在指定盘符和部分文件夹路径下找到该文件')
                print("OS:未在指定盘符和部分文件夹路径下找到该文件")

            else:  # 未能识别
                self.iomanager.sendResult(f'无法解析字符串: {self.message}')
                print("OS:" + f'无法解析字符串: {self.message}')
            # 无法正常进行发送，返回0则什么都不做
            return 0
        else:  # 聊天功能
            return 1

    def chooseFunction(self):
        # 获取新的消息
        self.setMessage(self.getNewMessage())
        # 判断消息类型
        res = self.analyzeText()

        if res == 1:
            self.chat()
        elif res == 2:
            self.executeScripts()
        elif res == 3:
            self.sendFile()

        pass

    # 计算最相似字符串和匹配度
    def find_most_similar(self, target):
        max_similarity = 0
        most_similar_string = ""
        for s in self.loaded_pairs:
            similarity = fuzz.ratio(target, s[0])
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_string = s[0]
        return most_similar_string, max_similarity

    def chat(self):
        most_similar_str, similarity_score = self.find_most_similar(self.message)
        if similarity_score > 40:
            print("OS:" + most_similar_str, similarity_score)
            try:
                # 执行聊天机器人
                response = self.chatbot.respond(most_similar_str)
                # 发送结果
                self.iomanager.sendResult(response)
            except Exception as e:
                self.iomanager.sendResult("抱歉，我不理解")
                print("OS:抱歉，我不理解")

        else:
            self.iomanager.sendResult("抱歉，我不理解")
            print("OS:匹配值过低")

    def executeScripts(self):
        # 创建一个名为test.bat的文件，内容为message，即脚本内容
        with open("test.bat", "w") as f:
            f.write("""@echo off
                    """)
            f.write(self.message)

        # 判断文件是否可执行
        if os.access("test.bat", os.X_OK):
            subprocess.call(["test.bat"])
            self.iomanager.sendResult("脚本执行成功")
            print("OS:脚本执行成功")
        else:
            self.iomanager.sendResult("脚本无法执行")
            print("OS:脚本无法执行")

    def sendFile(self):
        self.iomanager.sendFile(self.message)
