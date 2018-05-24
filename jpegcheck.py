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
from PIL import Image
import argparse
import shutil

EXTS = ['jpg', 'jpeg', 'JPG', 'JPEG']

def is_jpg(filename):
    """if a file be jpg.

    Args:
        filename: picture to be check
    """
    global EXTS

    if filename.split('.')[-1] not in EXTS:
        print(filename.split('.')[-1])
        return False

    data = open(filename, 'rb').read(11)

    if data[:4] != b'\xff\xd8\xff\xe0': 
        print(data[:4])
        return False
	
    if data[6:] != b'JFIF\0': 
        print(data[6:])
        return False
    return True


def is_vail_jpg(filename):
    """if a file can be open as jpg

    Args:
        filename: picture to be check
    """
    if not is_jpg(filename):
        print('%s is not jpg' % (filename))
        return False
    else:
        try:
            im = Image.open(filename)
            print('%s is vaild' % (filename))
            return True
        except IOError:
            print('%s is invaild' % (filename))
            return False

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
    if option == "Move":
        move_dir= os.path.join(dir, "invaild")
        if not os.path.exists(move_dir):
            os.mkdir(move_dir)
    for file in files:
        file_path = os.path.join(dir,file)
        if os.path.isdir(file_path):
             dir_check(file_path, option)
        else:
            if not is_vail_jpg(file_path):
                if option == "Delete":
                    os.remove(file_path)
                    print('%s is removed' % (file_path))
                elif option == "Move":
                    move_file = os.path.join(move_dir, file)
                    shutil.move(file_path, move_file)
                    print('%s is moved' % (file_path))
    pass

"""
def jpeg_check(path):
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
    src = "./"
    option = "Ignore"
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", help="root path of image folder")
    parser.add_argument("--option", help="process invaild picture: Delete/Ignore/Move")
    args = parser.parse_args()

    src = args.input_dir
    if args.option:
        option = args.option
    dir_check(src, option)


