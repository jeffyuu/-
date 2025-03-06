import logging
import subprocess
from ldplayer import ldplayer
import random
import win32gui
import win32con
import pydirectinput
import time

"""
本页代码实现功能如下：
1、点击具体位置
2、滑动屏幕(根据输入情况进行滑动，对于未给定的坐标，随机滑动)
3、缩放页面
4、。。。。。。
"""

Coordinate_set = [[340,123],[20,10]]

logging.basicConfig(level=logging.INFO, format='%(lineno)d - %(asctime)s - %(filename)s - %(funcName)s - %(message)s')

class Controller():
    def __init__(self,ldplayer_dir="D:/leidian/LDPlayer9/"):
        self.ldplayer_dir = ldplayer_dir

    def click(self,coordinate_set=[[78,784]]):
        if (len(coordinate_set)):
            for coordinate in coordinate_set:
                print(coordinate)
                subprocess.run([self.ldplayer_dir + "adb", "shell", "input", "tap", str(coordinate[0]), str(coordinate[1])],shell=False)

            logging.info("已完成点击！")
        else:
            logging.error("坐标集为空！！")
        
    def slide(self, start = None , end = None):
        if not (start and end):
            start = [random.uniform(200, 600),random.uniform(500, 1000)]
            end = [random.uniform(200, 600),random.uniform(500, 1000)]
        # 利用subprocess进行滑动
        subprocess.run([self.ldplayer_dir + "adb", "shell", "input", "swipe", str(start[0]), str(start[1]), str(end[0]), str(end[1])],shell=False)
        logging.info("已完成滑动！")

    def zoom_out(self,window_handle = 12345):
        time.sleep(5)
        if win32gui.IsWindow(window_handle):
            # 显示窗口
            win32gui.ShowWindow(window_handle, win32con.SW_SHOW)
            # 将窗口设置为前台窗口
            win32gui.SetForegroundWindow(window_handle)
        else:
            logging.info("无效的窗口句柄")
        pydirectinput.press('f5')
        logging.info("已完成缩小页面！")

if __name__ == "__main__":
    con = Controller()
    #con.click()
    #con.slide()
    #con.help()
    #con.zoom_in()
    con.zoom_out()
    ldplayer_dir = "D:/leidian/LDPlayer9/"
    #subprocess.run([con.ldplayer_dir + "adb", "shell", "input", "mouse", "roll","0","-100"],shell=False)