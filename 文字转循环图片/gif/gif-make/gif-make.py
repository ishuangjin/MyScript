# coding: utf-8

# # 完整代码如下
import imageio
import os
import sys

def func(DURATION):
    # 获取当前的工作路径
    path = os.getcwd()
    # 获取当前工作路径下的文件列表
    file_list = os.listdir(path)
    # 复制文件列表到另外一个列表
    png_list = file_list.copy()
    # 移除结尾不是png的图片，只保留结尾都是png的图片
    for file in file_list:
        if file[-3:]!= "jpg":
            png_list.remove(file)
    # 将图片中的数字，升序排列
    png_list.sort(key=lambda x: float(x[:-4]))
    # 获取每张图片的绝对路径，并获取每张照片的RGB通道值，将7张照片的RGB通道值，保存在一个列表中
    frames = []
    for png in png_list:
        image_path = os.path.join(path, png)
        frames.append(imageio.imread(image_path))
    # 将图片保存为gif图，设置了时间
    gif_path = os.path.join(path, "my_gif1.gif")
    imageio.mimsave(gif_path, frames, 'GIF', duration=DURATION)
func(0.5)


# # # 每一步的详细演示过程
#
# DURATION = 0.5
#
#
# # 获取当前的工作路径
# path = os.getcwd()
# print(path)
#
#
# # 获取当前工作路径下的文件列表
# file_list = os.listdir(path)
# print(file_list)
#
#
# # 复制一个列表
# png_list = file_list.copy()
# print(png_list)
#
#
# for file in file_list:
#     print(file[-3:])
#
#
# # 移除结尾不是png的图片，只保留结尾都是png的图片
# for file in file_list:
#     if file[-3:]!= "png":
#         png_list.remove(file)
# print(png_list)
#
#
# # 将图片中的数字，升序排列
# png_list.sort(key=lambda x: float(x[:-4]))
# print(png_list)
#
#
# # 获取每张图片的绝对路径
# for png in png_list:
#     image_path = os.path.join(path, png)
#     print(image_path)
#
#
# # 获取每张照片的RGB通道值，将7张照片的RGB通道值，保存在列表中
# for png in png_list:
#     image_path = os.path.join(path, png)
#     frames.append(imageio.imread(image_path))
# print(len(frames))
#
#
# # 将图片保存为gif图，设置了时间
# gif_path = os.path.join(path, "my_gif.gif")
# imageio.mimsave(gif_path, frames, 'GIF', duration=DURATION)
