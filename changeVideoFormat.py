from moviepy.editor import *

file = "new/newVideo.mp4"

clip = VideoFileClip(file)
aspect_ratio = clip.aspect_ratio

# Resize the video based on the width
resized_clip = clip.resize(width=780)

# Create a black background clip
black_bg = ColorClip((780,1280), color=(0,0,0))

# Position the resized video clip in the center of the black background
final_clip = CompositeVideoClip([black_bg, resized_clip.set_pos(('center', 'center'))])
final_clip = final_clip.set_duration(resized_clip.duration)

# Write the final video to file
final_clip.write_videofile("output.mp4")


