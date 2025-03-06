import subprocess
import time
import winreg
import logging

'''
本脚本包括一个雷电模拟器类，用于控制和管理雷电模拟器实例。
主要功能与函数有：
1. 获取雷电模拟器安装目录
2. 获取雷电模拟器实例状态
3. 启动雷电模拟器实例并打开指定应用
4. 关闭雷电模拟器实例中的指定应用
5. 获取雷电模拟器截图
6、调整窗口配置，分辨率，以及改为平板
'''

logging.basicConfig(level=logging.INFO, format='%(lineno)d - %(asctime)s - %(filename)s - %(funcName)s - %(message)s')

class ldplayer:
    """
    雷电模拟器类，用于控制和管理雷电模拟器实例。
    属性:
    雷电模拟器安装目录 (str): 雷电模拟器的安装目录。
    雷电模拟器索引 (int): 要控制的模拟器实例索引。
    """

    def __init__(self, leiplayer_index=0):
        """
        初始化雷电模拟器实例。
        参数:
        模拟器索引 (int): 要控制的模拟器实例索引。默认值为0。
        """
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\leidian\LDPlayer9"
        value_name = "InstallDir"

        # 获取注册表值得到雷电模拟器安装目录
        self.ldplayer_dir = self.get_registry_value(key, sub_key, value_name)
        self.ldplayer_index = leiplayer_index

    @staticmethod
    def get_registry_value(key, sub_key, value_name):
        """
        从注册表中获取指定的值。
        参数:
        key (winreg.HKEY_*): 注册表项根。
        sub_key (str): 注册表子项路径。
        value_name (str): 注册表值的名称。
        返回值:
        str: 注册表值的内容，如果注册表路径不存在或发生错误，返回None。
        """
        try:
            reg_key = winreg.OpenKey(key, sub_key)
            value, value_type = winreg.QueryValueEx(reg_key, value_name)
            winreg.CloseKey(reg_key)
            return value
        except FileNotFoundError:
            print("指定的注册表路径不存在,雷电模拟器未正确安装")
        except Exception as e:
            print("发生错误:", e)
            return None

    @staticmethod
    def ldcmd_2_dict(text):
        """
        将雷电模拟器命令行返回的文本解析为字典。
        参数:
        text (str): 包含文本内容的字符串，每行代表一个条目，条目之间使用换行符分隔。
                    每个条目应包含逗号分隔的值，分别为索引、标题、顶层窗口句柄、绑定窗口句柄、
                    是否进入Android、进程PID、VBox进程PID、宽度、高度、DPI。
        返回值:
        dict: 包含解析后内容的字典。字典的键为索引，值为包含条目内容的字典。
              条目字典包含以下键值对：
                  - "标题"：标题字符串
                  - "顶层窗口句柄"：顶层窗口句柄整数
                  - "绑定窗口句柄"：绑定窗口句柄整数
                  - "是否进入Android"：是否进入Android布尔值
                  - "进程PID"：进程PID整数
                  - "VBox进程PID"：VBox进程PID整数
                  - "宽度"：宽度整数
                  - "高度"：高度整数
                  - "DPI"：DPI整数
        """
        result = {}
        lines = text.strip().split('\n')
        for line in lines:
            parts = line.split(',')
            index = int(parts[0])
            title = parts[1]
            top_window_handle = int(parts[2])
            bound_window_handle = int(parts[3])
            enter_android = bool(int(parts[4]))
            process_pid = int(parts[5])
            vbox_process_pid = int(parts[6])
            width = int(parts[7])
            height = int(parts[8])
            dpi = int(parts[9])

            result[index] = {
                "标题": title,
                "顶层窗口句柄": top_window_handle,
                "绑定窗口句柄": bound_window_handle,
                "是否进入Android": enter_android,
                "进程PID": process_pid,
                "VBox进程PID": vbox_process_pid,
                "宽度": width,
                "高度": height,
                "DPI": dpi
            }

        return result

    def station_player(self):
        """
        获取所有模拟器实例的状态。
        返回值:
        dict: 当前模拟器实例的状态信息字典，包含以下键值对：
              - "标题"：标题字符串
              - "顶层窗口句柄"：顶层窗口句柄整数
              - "绑定窗口句柄"：绑定窗口句柄整数
              - "是否进入Android"：是否进入Android布尔值
              - "进程PID"：进程PID整数
              - "VBox进程PID"：VBox进程PID整数
              - "宽度"：宽度整数
              - "高度"：高度整数
              - "DPI"：DPI整数
        """
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        station = subprocess.run(
            [self.ldplayer_dir + "ldconsole.exe", "list2"],
            encoding='gbk',
            stdout=subprocess.PIPE,
            startupinfo=startupinfo
        )
        dict_player_message = self.ldcmd_2_dict(station.stdout)
        if dict_player_message:
            logging.info("成功获取雷电模拟器状态信息")
            return dict_player_message[self.ldplayer_index]
        
    

    def ld_and_start(self, packageName):
        """
        启动当前模拟器实例并打开指定的应用。
        参数:
        包名 (str): 要打开的应用的包名。
        """
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.run(
            [self.ldplayer_dir + "ldconsole.exe", "launchex", "--index", str(self.ldplayer_index), "--packagename", packageName],
            shell=False,
            startupinfo=startupinfo
        )
        time.sleep(5)
        logging.info("模拟器启动成功且成功打开游戏")


    def ld_and_close(self, packageName):
        """
        关闭当前模拟器实例中的指定应用。
        参数:
        包名 (str): 要关闭的应用的包名。
        """
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.run(
            [self.ldplayer_dir + "ldconsole.exe", "killapp", "--index", str(self.ldplayer_index), "--packagename", packageName],
            shell=False,
            startupinfo=startupinfo
        )
        logging.info("模拟器关闭成功且成功关闭游戏")


if __name__ == "__main__":

    ld = ldplayer(0)
    print(ld.ldplayer_dir)
    # 模拟器打开（从0开始，根据实际情况修改）
    app_package = "com.tencent.tmgp.supercell.clashofclans"
    ld.ld_and_start(app_package)
    time.sleep(5)
    print(ld.station_player())
    ld.ld_and_close(app_package)
    print(ld.station_player())
    time.sleep(2)
