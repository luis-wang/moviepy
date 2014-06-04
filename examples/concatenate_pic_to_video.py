#coding:utf8
'''
Created on 2014-6-4

@author: wangxd
'''

import os
from moviepy.editor import *

print 'start....'


filedir = 'data/clips/'
#files = sorted( os.listdir("clips/") )
files = sorted(os.listdir(filedir))

clips = [ VideoFileClip('data/clips/%s'%f) for f in files]
video = concatenate(clips, transition = VideoFileClip("data/logo.avi"))
video.to_videofile("data/logo2.avi",fps=25, codec="mpeg4")



print 'end....'