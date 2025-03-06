import cv2
import time
import numpy as np
import subprocess
from ldplayer import ldplayer
import logging

"""
本页代码实现了视觉学习类：
1、调用模拟器截图页面，并保存图像
2、多目标识别并返回坐标值
3、展示图像识别的内容，用于调试
"""

logging.basicConfig(level=logging.INFO, format='%(lineno)d - %(asctime)s - %(filename)s - %(funcName)s - %(message)s')

THRES_HOLD = 0.7
MATCH_NUMBERS = 3


class image_matching():

    def __init__(self,ldplayer_dir="D:/leidian/LDPlayer9/"):
        self.ldplayer_dir = ldplayer_dir
        self.image = self.obtain_ld_screen()
        self.all_matches = []

    def obtain_ld_screen(self):
        subprocess.run([self.ldplayer_dir + "adb", "shell", "screencap", "-p", "/sdcard/screencap.png"],shell=False)
        subprocess.run([self.ldplayer_dir + "adb", "pull", "/sdcard/screencap.png", "image/screencap.png"],shell=False)
        image = cv2.imread("image/screencap.png")
        logging.info("成功获取雷电模拟器截图")
        return image

    def match_image(self,image_path_dict,threshold=THRES_HOLD):
        self.obtain_ld_screen()
        if self.image is None:
            logging.error("Main image is not loaded successfully.")
            return
        
        if len(image_path_dict) == 0:
            logging.error("No image to match")
            return
        rectangles = [] # 用于记录所有匹配到的矩形区域
        self.all_matches = []  # 先清空，用于记录所有模板的匹配结果

        for key, value in image_path_dict.items():
            template = cv2.imread(value)
            if template is None:
                logging.error(f"Failed to read template image: {value}")
                continue

            # 确保图像和模板的通道数一致
            if len(self.image.shape) == 3 and len(template.shape) == 2:
                template = cv2.cvtColor(template, cv2.COLOR_GRAY2BGR)
            elif len(self.image.shape) == 2 and len(template.shape) == 3:
                template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

            # 确保数据类型一致
            if self.image.dtype != template.dtype:
                self.image = self.image.astype(np.float32)
                template = template.astype(np.float32)

            h, w = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY).shape
            # 使用模板匹配
            result = cv2.matchTemplate(self.image, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)

            # 记录当前模板的匹配结果
            if len(loc[0]) > 0:
                #self.all_matches.extend(zip(*loc[::-1]))
                #print(self.all_matches)
                pass

            # 在原始图像上绘制匹配区域
            for pt in zip(*loc[::-1]):  # 反转坐标 (x, y)
                cv2.rectangle(self.image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
                rectangles.append((pt[0], pt[1], w, h))
                cv2.putText(self.image, key, (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 应用非极大值抑制（合并重叠区域）
        rectangles, _ = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        for x, y, w, h in rectangles:
            self.all_matches.append([x+w//2,y+h//2]) # 返回识别的图像中心点坐标

        if len(self.all_matches) == 0:
            logging.error("未匹配到任何图像")
        else:
            print(self.all_matches)
            logging.info("图像已匹配，并返回图像坐标")

    def show_image(self):
        cv2.imshow('Multi-Target Matches', self.image)
        logging.info("窗口已打开！！")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    #ld = ldplayer(0)
    #app_package = "com.tencent.tmgp.supercell.clashofclans"
    #ld.ld_and_start(app_package)
    image_matching = image_matching()
    image_matching.match_image()
    image_matching.show_image()