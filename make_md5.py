# -*- coding:utf-8 -*-

import hashlib
import os
import argparse
import sys
from hashlib import md5
import importlib
importlib.reload(sys)
from dhash_diff import calculate_hash
from PIL import Image

def md5_file(name):
    m = md5()
    a_file = open(name, 'rb')    #需要使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()

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
            path = os.path.join(file_dir, file)
            md5 = md5_file(path)
            #fp = open(path, 'rb')
            #im = Image.open(fp)
            #md5 = calculate_hash(im)
            #fp.close()
            ext = os.path.splitext(path)[1]
            newname=os.path.join(file_dir,(md5+ext))
            if not os.path.exists(newname):
                os.rename(path, newname)
                print (path, newname)
            else:
                #os.remove(path)
                print (path, "delete")


if __name__ == '__main__':
    totalNum = 0
    totalDup = 0
    dirName = "./"  # 相册路径
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="src dir to work")
    parser.add_argument("--option", help="option to handle similar pictures")
    args = parser.parse_args()

    dirName = args.src
    processDir(dirName)

    print('total:%d, duplicate:%d' % (totalNum, totalDup))