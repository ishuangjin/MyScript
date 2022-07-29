import imageio
from PIL import ImageFont, Image, ImageDraw
import os


def new_png(food):
    # 设置字体和字号大小
    font = ImageFont.truetype(os.path.join("fonts", "aaa.ttf"), 84)

    for idx in food:
        im1 = Image.open('seed.png')
        # 在图片上添加文字
        draw = ImageDraw.Draw(im1)
        draw.text((0, 0), str(idx), (0, 0, 0), font)
        draw = ImageDraw.Draw(im1)
        # 保存图片
        im1.save('./imgs/' + str(idx) + ".png")


def create_gif(image_list, gif_name, duration=0.1):
    os.chdir(os.path.join(os.getcwd(), "imgs"))
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return


def main():
    # 获取当前的工作路径
    path = os.getcwd()
    food = ["猪脚饭", "小炒鸡肉", "小鱼干", "啤酒鸭", "红烧鱼块", "毛豆炒肉",
            "烟笋腊肉", "爆炒猪舌", "麻辣肠", "烧鸭", "白切鸡", "卤水鸭",
            "酸笋炒肉", "酸菜鱼", "剁椒鱼头", "鸡腿", "油豆腐炒肉", "红萝卜炒肉",
            "小炒肉", "木耳炒肉", "香干炒肉", "西红柿炒蛋", "热狗炒蛋", "红烧茄子",
            "青菜", "豆芽", "冬瓜", "土豆", "豆腐", "花菜", "青瓜", "包菜", "猪血", "海带",
            "千张", "大白菜", "小南瓜", "老南瓜", "米粒肉末", "雪里红肉末", "凉拌皮蛋"]
    new_png(food)
    png_path = os.path.join(path, "imgs")
    # 获取当前工作路径下的文件列表
    file_list = os.listdir(png_path)
    # print(file_list)
    # 复制文件列表到另外一个列表
    png_list = file_list.copy()
    # 移除结尾不是png的图片，只保留结尾都是png的图片
    for file in file_list:
        if file[-3:] != "png":
            png_list.remove(file)
    image_list = png_list
    gif_name = 'new.gif'
    duration = 0.08
    create_gif(image_list, gif_name, duration)


if __name__ == '__main__':
    main()
