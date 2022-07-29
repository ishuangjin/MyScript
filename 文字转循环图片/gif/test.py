# -*- coding: utf-8 -*-

import os

import imageio
import pygame


def gif_make(DURATION):
    # 获取当前的工作路径
    path = os.getcwd()
    # 获取当前工作路径下的文件列表
    file_list = os.listdir(path)
    # 复制文件列表到另外一个列表
    png_list = file_list.copy()
    # 移除结尾不是png的图片，只保留结尾都是png的图片
    for file in file_list:
        if file[-3:] != "jpg":
            png_list.remove(file)
    # 将图片中的数字，升序排列
    # png_list.sort(key=lambda x: float(x[:-4]))
    # 获取每张图片的绝对路径，并获取每张照片的RGB通道值，将7张照片的RGB通道值，保存在一个列表中
    frames = []
    for png in png_list:
        image_path = os.path.join(path, png)
        frames.append(imageio.imread(image_path))
    # 将图片保存为gif图，设置了时间
    gif_path = os.path.join(path, "my_gif.gif")
    imageio.mimsave(gif_path, frames, 'GIF', duration=DURATION)


def pic_make(food):

    pygame.init()

    for text in food:
        font = pygame.font.Font(os.path.join("fonts", "aaa.ttf"), 96)
        rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
        picname = text + ".jpg"
        pygame.image.save(rtext, picname)


if __name__ == '__main__':
    food = ["猪脚饭", "小炒鸡肉", "小鱼干", "啤酒鸭", "红烧鱼块", "毛豆炒肉",
            "烟笋腊肉", "爆炒猪舌", "麻辣肠", "烧鸭", "白切鸡", "卤水鸭",
            "酸笋炒肉", "酸菜鱼", "剁椒鱼头", "鸡腿", "油豆腐炒肉", "红萝卜炒肉",
            "小炒肉", "木耳炒肉", "香干炒肉", "西红柿炒蛋", "热狗炒蛋", "红烧茄子",
            "青菜豆芽冬瓜", "土豆豆腐", "花菜", "青瓜", "包菜", "猪血", "海带",
            "千张", "大白菜", "小南瓜", "老南瓜", "米粒肉末", "雪里红肉末", "凉拌皮蛋"]
    pic_make(food=food)
    gif_make(0.1)
