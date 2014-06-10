from moviepy.editor import *

fn = r'D:\data\qq_space\821090701\FileRecv\MobileFile\movie\2014.mp4'
# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
#clip = VideoFileClip(fn).subclip(50,60)
clip = VideoFileClip(fn).subclip(10,15)



# Reduce the audio volume (volume x 0.8)
clip = clip.volumex(0.8)

# Generate a text clip. You can customize the font, color, etc.
txt_clip = TextClip("My Holidays 2013",fontsize=70,color='white')

# Say that you want it to appear 10s at the center of the screen
txt_clip = txt_clip.set_pos('center').set_duration(10)

# Overlay the text clip on the first video clip
video = CompositeVideoClip([clip, txt_clip])

print 'start..'
# Write the result to a file
video.to_videofile(r"D:\data\qq_space\821090701\FileRecv\MobileFile\movie\2014new.avi",fps=24, codec='mpeg4')
print 'end...'





























