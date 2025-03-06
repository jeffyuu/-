import logging
import time
from ldplayer import ldplayer
from image_matching import image_matching
from controller import Controller

#调用ldplayer类，获得雷电模拟器的路径和·窗口句柄
ld = ldplayer()
LDplayer_dir = ld.ldplayer_dir
WINdow_handle = ld.station_player()["绑定窗口句柄"]

im = image_matching()
co = Controller()



#调用image_matching类，获得雷电模拟器的截图

logging.basicConfig(level=logging.INFO, format='%(lineno)d - %(asctime)s - %(filename)s - %(funcName)s - %(message)s')

class reality():
    def __init__(self,ldplayer_dir=LDplayer_dir,window_handle=WINdow_handle):
        self.ldplayer_dir = ldplayer_dir
        self.window_handle = window_handle

    def init_reality(self):
        pass
        
    def forward_flow(self):
        ld.ld_and_start()
        time.sleep(60)
        #如果有广告，将广告给关掉

        pass

    def upgrate_heros(self):
        pass

    def home_attack(self):
        image_dict1 = {"jingong":"image/game_image/jinggong1.png"}
        im.match_image(image_dict1)
        co.click(im.all_matches)

        image_dict2 = {"jingong":"image/game_image/jinggong2.png"}
        im.match_image(image_dict2)
        co.click(im.all_matches)

        image_dict3 = {"feilong":"image/game_image/feilong1.png"}
        im.match_image(image_dict3)
        co.click(im.all_matches)

        attack_set = {
            "1":"image/attack_image/at1.png",
            "2":"image/attack_image/at2.png",
            "3":"image/attack_image/at3.png",
            "4":"image/attack_image/at4.png",
            "5":"image/attack_image/at5.png",
            "6":"image/attack_image/at6.png",
            "7":"image/attack_image/at7.png",
            "8":"image/attack_image/at8.png",
            "9":"image/attack_image/at9.png",
            "10":"image/attack_image/at10.png"
        }
        im.match_image(attack_set)
        co.click(im.all_matches)

        pass

    def train_army(self):

        pass

    def quit_game(self):
        ld.ld_and_close()
        pass

if __name__ == "__main__":
    re = reality()
    re.home_attack()