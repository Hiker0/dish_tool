# -*- coding:utf-8 -*-

#===============================================================
#基于DHash 算法的重复图片检测, 计算俩俩之间的汉明距离
#打印出重复文件信息
#ARGS
#	--src:要检测的文件夹
#===============================================================


from PIL import Image
import os
import argparse

IMAGE_SIZE = 32
DISTAN_THRESHOLD = 200

global allDiff
allDiff = []

#---------------------------------
#DHASH实现
#---------------------------------
def __difference(image):
    """
    *Private method*
    计算image的像素差值
    :param image: PIL.Image
    :return: 差值数组。0、1组成
    """
    resize_width = IMAGE_SIZE
    resize_height = IMAGE_SIZE
    # 1. resize to (9,8)
    smaller_image = image.resize((resize_width, resize_height))
    # 2. 灰度化 Grayscale
    grayscale_image = smaller_image.convert("L")
    # 3. 比较相邻像素
    pixels = list(grayscale_image.getdata())
    difference = []
    for row in range(resize_height):
        row_start_index = row * resize_width
        for col in range(resize_width - 1):
            left_pixel_index = row_start_index + col
            difference.append(pixels[left_pixel_index] > pixels[left_pixel_index + 1])
    return difference

def __hamming_distance_with_hash(dhash1, dhash2):
    """
    *Private method*
    根据dHash值计算hamming distance
    :param dhash1: str
    :param dhash2: str
    :return: 汉明距离(int)
    """
    difference = (int(dhash1, 16)) ^ (int(dhash2, 16))
    return bin(difference).count("1")

def calculate_hash(image):
    """
    计算图片的dHash值
    :param image: PIL.Image
    :return: dHash值,string类型
    """
    difference = __difference(image)
    # 转化为16进制(每个差值为一个bit,每8bit转为一个16进制)
    decimal_value = 0
    hash_string = ""
    for index, value in enumerate(difference):
        if value:  # value为0, 不用计算, 程序优化
            decimal_value += value * (2 ** (index % 8))
        if index % 8 == 7:  # 每8位的结束
            hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))  # 不足2位以0填充。0xf=>0x0f
            decimal_value = 0
    return hash_string

def hamming_distance(first, second):
    """
    计算两张图片的汉明距离(基于dHash算法)
    :param first: Image或者dHash值(str)
    :param second: Image或者dHash值(str)
    :return: hamming distance. 值越大,说明两张图片差别越大,反之,则说明越相似
    """
    # A. dHash值计算汉明距离
    if isinstance(first, str):
        return __hamming_distance_with_hash(first, second)

    # B. image计算汉明距离
    hamming_distance = 0
    image1_difference = __difference(first)
    image2_difference = __difference(second)
    for index, img1_pix in enumerate(image1_difference):
        img2_pix = image2_difference[index]
        if img1_pix != img2_pix:
            hamming_distance += 1
    return hamming_distance

#--------------------------------

def picPostfix():  # 相册后缀的集合
    """能够处理的图片后缀

    :return:
    """
    postFix = set()
    postFix.update(['bmp', 'jpg', 'png', 'tiff', 'gif', 'pcx', 'tga', 'exif',
                    'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'JPG', 'raw', 'jpeg'])
    return postFix

def foundSame(file_name, hash):
    """判断是否有重复

    :param file_name:
    :param hash:
    :return:
    """
    for i in range(len(allDiff)):
        ans = hamming_distance(allDiff[i][1], hash)
        #print ('[%s]\t[%s]\t%s'%(allDiff[i][0], file_name, ans))
        if ans <= DISTAN_THRESHOLD:  # 判别的汉明距离，自己根据实际情况设置
           print ('%s duplicate with %s\n'%(file_name, allDiff[i][0]))
           return True
    return False

def processSame(file_name):
    """处理重复图片

    :param file_name:
    :return:
    """
    global totalDup
    totalDup = totalDup + 1
	
	#TODO 在这里处理重复图片
    #print ('%s is duplicate'%(file_name))

def gethash(file_name):
    """建立字典

    :param file_name:
    :return:
    """
    if file_name.split('.')[-1] in postFix:  # 判断后缀是不是照片格式
        try:
            im = Image.open(file_name) 
            hash = calculate_hash(im)
            #print('%s  %s'%(file_name, hash))
            if not foundSame(file_name, hash):
                allDiff.append((file_name, hash))
            else:
                processSame(file_name)
        except OSError:
            pass

def processDir(file_dir):
    """遍历文件夹

    :param file_dir:
    :return:
    """
    global totalNum
    print('root %s'%(file_dir))   
    for file in os.listdir(file_dir):
        if os.path.isdir(file):
            processDir(r'%s/%s'%(file_dir, file))
        else:
            totalNum = totalNum + 1
            gethash(r'%s/%s'%(file_dir, file))
            #print (file)

if __name__ == '__main__':

    totalNum = 0
    totalDup = 0
    dirName = "./"                         # 相册路径
    postFix = picPostfix()                 #  图片后缀的集合
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="src dir to work")
    parser.add_argument("--option", help="option to handle similar pictures")
    args = parser.parse_args()
    
    dirName = args.src
    processDir(dirName)
    
    print('total:%d, duplicate:%d'%(totalNum, totalDup))