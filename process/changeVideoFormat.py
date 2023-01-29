from moviepy.editor import *

def changeFormat():
  file = "../new/newVideo.mp4"

  clip = VideoFileClip(file)
  # aspect_ratio = clip.aspect_ratio

  resized_clip = clip.resize(width=780)

  black_bg = ColorClip((780,1280), color=(0,0,0))

  final_clip = CompositeVideoClip([black_bg, resized_clip.set_pos(('center', 'center'))])
  final_clip = final_clip.set_duration(resized_clip.duration)

  final_clip.write_videofile("../new/output.mp4")


