# -*- coding:utf-8 -*-

#========================================================================
#图片清洗工具
#	'f' 标记false, 
#	'b''s' 后退
#	'q'结束并保存结果
#   其他键标记为true
#清洗完成后 ,自动分配到flase, true 文件夹
#=======================================================================

import cv2
from numpy import *
import os
import sys
import shutil
import argparse
import time

EXTS= ['jpg','jpeg','JPG','JPEG','png','PNG']

def main(src):

    listfile = os.listdir(src)
    true_list = []
    false_list = []

    start = time.time()
    filenum = len(listfile)
    i = 0;
    print ("filenum %d"%(filenum))
    quit = 0
    
    while(i < filenum and quit == 0):
        file = listfile[i]
        file_path = os.path.join(src, file)
        print("next: ", listfile[i])
        
        if os.path.isdir(file_path):
            i = i+1
            print('%s is dir' % (file))
            continue

        if file.split('.')[-1] not in EXTS:
            false_list.append(file)
            print('%s erro postfix' % (file))
            i = i+1
            continue
        try:
            image = cv2.imread(file_path)
            cv2.namedWindow(file, 0);
            cv2.resizeWindow(file, 640, 480);
            cv2.moveWindow(file, 100, 100)
            cv2.imshow(file, image)
            finished = len(true_list)+len(false_list)
            print('total:%d, finished :%d, true: %d, false:%d left:%d' % \
				(filenum, finished, len(true_list), len(false_list), filenum-finished))
            sys.stdout.flush()
            key = cv2.waitKey(0)
            #print(key)
            if key == ord('f'):
                false_list.append(file)
                print('%s fail' % (file))
                i = i + 1
            elif key == ord('s') or key == ord('b'):
                if i > 0:
                    i = i - 1
                if false_list.count(listfile[i])>0:
                    false_list.remove(listfile[i])
                if true_list.count(listfile[i])>0:
                    true_list.remove(listfile[i])
                print("back...")
            elif key == ord('q'):
                quit = 1
                break
            else:
                true_list.append(file)

                print('%s success' % (file))
                i = i + 1

            cv2.destroyWindow(file)
        except cv2.error:
            i = i+1
        
        sys.stdout.flush()
        
    end = time.time()

    #suc_dir = os.path.join(src, "true")
    # if not os.path.exists(suc_dir):
    # os.mkdir(suc_dir)
    fail_dir = os.path.join(src, "false")
    true_dir = os.path.join(src, "true")
    if not os.path.exists(fail_dir):
        os.mkdir(fail_dir)
    if not os.path.exists(true_dir):
        os.mkdir(true_dir)
        
    for file in false_list:
        shutil.move(os.path.join(src, file), os.path.join(fail_dir, file))
    for file in true_list:
        shutil.move(os.path.join(src, file), os.path.join(true_dir, file))
        

    print('total time: %ds' % (end - start))
    finished = len(true_list)+len(false_list)
    print('total:%d, finished :%d, true: %d, false:%d left:%d' % (filenum, finished, len(true_list), len(false_list), filenum-finished))

if __name__ == '__main__':
    src = "./"
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", help="src dir to copy")
    args = parser.parse_args()

    src = args.src
    main(src)

