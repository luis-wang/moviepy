#coding:utf8
'''
C:\Users\Administrator>
'''

import os,sys
import subprocess as sp


home_path = r'C:\Users\Administrator'
os.chdir(home_path)

command = r'D:\install\ffmpeg\ffmpeg-20131213-git-5d8e4f6-win64-static\bin\ffmpeg -h'
os.system(command)
#pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

#print pipe



