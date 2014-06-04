#coding:utf8
'''
Created on 2014-6-4
work fine

'''

import os
from moviepy.editor import *

print 'start....'


filedir = 'data/clips/'
#files = sorted( os.listdir("clips/") )
files = sorted(os.listdir(filedir))
print 'files = ', files

newfiles = []
for f in files:
    if os.path.splitext(f)[1].lower() == '.jpg':
        newfiles.append(f)

clips = [ VideoFileClip('data/clips/%s' % f) for f in newfiles]

print 'clips = ',clips

#video = concatenate(clips, transition = VideoFileClip("data/test.avi"))
video = concatenate(clips)

video.to_videofile("data/gaojie2.avi", fps=2, codec="mpeg4")



print 'end....'