#coding:utf8

"""
Tests meant to be run with pytest
http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
正确的命令：ffmpeg -ss 0 -i in.mp4 -filter:v scale=640:480 -b:v 21504 -t 5 test.mpg

http://stackoverflow.com/questions/14731501/ffmpeg-error-at-least-one-output-file-must-be-specified：

ffmpeg -ss 0 -i F:\test\video\meitun.MOV -filter:v scale=768:540 -b:v 4556*1024 -t 10 F:\test\video\meitun768x540.mp4



"""
import cv2
import numpy
import subprocess as sp
from moviepy.editor import *

FFMPEG_BIN = "ffmpeg" # on Linux
FFMPEG_BIN = "ffmpeg.exe" # on Windows
input_fname = r'F:\test\video\meitun.MOV'
#读取视频文件

command = [ FFMPEG_BIN,
            '-i', input_fname,
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',]
            #'-vcodec', 'rawvideo', '-']

print 'command = ', command
print str(command).replace("'", "").replace(r"\\", "\\").replace(',', '')

pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)


#读取相应的frame

# read 420*360*3 bytes (= 1 frame)
raw_image = pipe.stdout.read(1280*720*3)
# transform the byte read into a numpy array
image =  numpy.fromstring(raw_image, dtype='uint8')
#image = image.reshape((360,420,3))
# throw away the data in the pipe's buffer.
cv2.imwrite('filename.jpg', image)
pipe.stdout.flush()

























