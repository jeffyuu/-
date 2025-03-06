from collections import deque
import os



class Queue:
    def __init__(self):
        self.queue = deque()

    def inital_queue(self):#初始化队列
        self.queue = deque()
        for _ in range(0):
            self.queue.append(0)
            self.queue.append(1)
            self.queue.append(2)
        print("初始化队列成功")
        

    def get_task_info(self,taskid):#根据任务id执行任务
        task_functions = {
            0: self.screen_shot,
            1: lambda: self.Match_click(image_path="picture1.png"),
            2: lambda: self.Match_click(image_path="picture2.png"),
        }
        func = task_functions.get(taskid)
        if func:
            print("执行任务成功")
            return func()      
        else:
            return "无效的输入"
        
class priority_que():
    def __init__(self):
        self.coin = 0
        self.goldwater = 0
        self.roil = 0
        self.queue = deque()
    
    def initial_source(self):
        self.queue = deque()
        self.coin = 0
        self.goldwater = 0
        self.roil = 0
        print("初始化资源成功")


class Game:#task
    def __init__(self):
        number_of_task = 3

    def game_start(self):
        os.system("ldconsole launch --name mySimulator")
        os.system("ldconsole runapp --index 1 --packagename com.tencent.tmgp.supercell.clashofclans")


if __name__ == "__main__":
    os.system("echo hello")
    game = Game()
    game.game_start()