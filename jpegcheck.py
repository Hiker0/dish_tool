# -*- coding: utf-8 -*-

#========================================================================
# jpg图片检测工具
#
#
#
#
#
#=======================================================================


import os
import argparse
import shutil
import imghdr

EXTS = ['jpg', 'jpeg', 'JPG', 'JPEG']
global move_dir

def suffixal_check(filename):
    """check the suffixal of picture

    :param filename:
    :return:
    """
    global EXTS

    if filename.split('.')[-1] not in EXTS:
        print(filename.split('.')[-1])
        return False
    else:
        return True
def vaild_check(filename):
    type = imghdr.what(filename)
    if type == "jpeg":
        return True
    else:
        return False

"""
#from PIL import Image
def pil_check():
    try:
        im = Image.open(filename)
        print('%s is vaild' % (filename))
        return True
    except IOError:
        print('%s is invaild' % (filename))
        return False
"""

def header_check(filename):
    """check the real format of picture
    Args:
        filename: picture to be check
    """
    #SOI EOI
    data = open(filename, 'rb').read(11)

    if data[:4] != b'\xff\xd8\xff\xe0': 
        print(data[:4])
        return False
	
    if data[6:] != b'JFIF\0': 
        print(data[6:])
        return False
    return True


def file_process(filename, option):
    """if a file can be open as jpg

    Args:
        filename: picture to be check
    """
    global move_dir
    #print("-----", filename,"-----------")
    #print ("suffixal_check", suffixal_check(filename))
    #print("header_check", header_check(filename))
    #print("vaild_check", vaild_check(filename))

    if vaild_check(filename):
        if not suffixal_check(filename):
            newname = os.path.dirname(filename) + os.path.basename(filename).split('.')[0] + ".jpg"
            os.rename(filename, newname)
            print (filename,"=>", newname)
    else:
        if option == "Delete":
            os.remove(filename)
            print('%s is removed' % (filename))
        elif option == "Move":
            move_file = os.path.join(move_dir, os.path.basename(filename))
            shutil.move(filename, move_file)
            print('%s is moved' % (filename))
        else:
            print ("ignore", filename)

def dir_check(dir, option):
    """test the files in dir

    test every file in dir. if file is not a invaild jepg, do options as 'option' assign

    Args:
        filename: picture to be check
        option:
            Delete: delete the invaild file
            Ignore: do nothing
    """
    files= os.listdir(dir)
    for file in files:
        file_path = os.path.join(dir,file)
        if os.path.isdir(file_path):
             dir_check(file_path, option)
        else:
            file_process(file_path, option)
    pass

"""
def jpeg_check(path):
    # ubuntu tool
    s=[]
    files= os.listdir(path) #得到文件夹下的所有文件名称
    for file in files: #遍历文件夹
         file_path = os.path.join(path,file)
         if not os.path.isdir(file_path): #判断是否是文件夹，不是文件夹才打开
            # use jpeginfo to check jpg image first.
            jpgcheck = 'jpeginfo' +' -c ' + file_path + ' -d' +'\n'
            os.system(jpgcheck)

            if not os.path.isfile(file_path):
                print ("%s is deleted\n"%(file_path))
               
    return s
"""

if __name__ == '__main__':
    global move_dir

    src = "./"
    option = "Ignore"
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", help="root path of image folder")
    parser.add_argument("--option", help="process invaild picture: Delete/Ignore/Move")
    args = parser.parse_args()

    if args.input_dir:
        src = args.input_dir
    else:
        print ("you need assign a dir")
        exit(0)

    if args.option:
        option = args.option
    if option == "Move":
        move_dir= os.path.join(src, "invaild")
        if not os.path.exists(move_dir):
            os.mkdir(move_dir)
    dir_check(src, option)


