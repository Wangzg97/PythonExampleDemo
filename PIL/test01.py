# PIL接口详解
# PIL只支持python2.x而Pillow是在PIL基础上fork的版本，支持python3.x
# 安装 conda install Pillow 或 pip install Pillow
# 代码参考：《走向Tensorflow2.0：深度学习应用编程快速入门》赵英俊

import os
import sys

from PIL import Image, ImageFilter

# ****************************图像读写******************************* #

# 直接打开图像Image.open()
with open('test.jpg', 'rb') as fp:
    im = Image.open(fp)
    # im.show()

# 读取压缩文件中的图像TarIO(),不必解压缩
# fp2 = TarIO.TarIO("test.tar", "test/test.jpg")
# img = Image.open(fp2)
# img.show()


# 将图像保存为JPEG格式Image.save()
# sys.argv[]是用来获取命令行参数的，sys.argv[0]表示代码本身文件路径，所以参数从1开始.
# 比如
# python test.py --t help --v
# 那么sys.argv就是['test.py', '--t', 'help', '--v']
# 那么sys.argv[1:]就是['--t', 'help', '--v']
# 下同
for infile in sys.argv[1:]:
    f, e = os.path.splitext(infile)
    out = f + ".jpg"
    if infile != out:
        try:
            Image.open(infile).save(out)
        except IOError:
            print("failed")

# ****************************图像编辑******************************* #

# 生成缩略图
# 预设缩略图尺寸
size = (128, 128)
# 逐个读取图片并转化成缩略图
for infile in sys.argv[1:]:
    # 保存路径
    out = os.path.splitext(infile)[0] + ".thumbnail"
    if infile != out:
        try:
            # 转换并保存
            img = Image.open(infile)
            img.thumbnail(size)
            img.save(out, "JPEG")
        except IOError:
            print("failed")

# 查看图像格式
for infile in sys.argv[1:]:
    with Image.open(infile) as img:
        print(infile, img.format, "%d x % d" % img.size, img.mode)  # 格式、尺寸、色彩模式

# 截取图片
file = "test.jpg"
img = Image.open(file)
# 截取范围
area = (100, 100, 200, 200)
img.crop(area)
# img.save("test_res.jpg", "JPEG")


# 改变尺寸
file = "test.jpg"
img = Image.open(file)
# 重置为256px x 256px, rotate(x)为将图片旋转x度
img.resize((256, 256)).rotate(45)
# img.save("test_res.jpg", "JPEG")

# ****************************像素变换******************************* #

# 色彩模式转换,convert()
file = "test.jpg"
img = Image.open(file).convert("L")  # 模式"1"为二值图像,"L"为灰色图像。共九种不同模式：1，L，P，RGB，RGBA，CMYK，YCbCr,I，F
# img.save("test_res.jpg", "JPEG")


# 像素对比度调节
file = "test.jpg"
img = Image.open(file)
# ImageFilter为滤波函数类。 BLUR:模糊滤波；CONTOUR:轮廓滤波；DETAIL:细节滤波 ...等等
img.filter(ImageFilter.DETAL)
# img.save("test_res.jpg", "JPEG")
