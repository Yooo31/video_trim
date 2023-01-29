from moviepy.editor import *
import random
import os
import re
import shutil
# from moviepy.config import change_settings
# change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

def randomColor():
  r = random.randint(200, 255)
  g = random.randint(0, 255)
  b = random.randint(0, 255)
  return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def addText():
  background = randomColor()

  path_to_cut_folder = "../cut"
  path_to_finished_folder = "../finished"

  for i, file in enumerate(os.listdir(path_to_cut_folder)):
    video_path = os.path.join(path_to_cut_folder, file)
    video = VideoFileClip(video_path)
    file_name = os.path.splitext(file)[0]
    match = re.search(r'\d+', file_name)
    if match:
      txt_clip = (TextClip("Partie {}".format(match.group()), stroke_width=5, fontsize=50, color='white', bg_color=background)
                  .set_position((280, 950))
                  .set_duration(video.duration))
    else:
      txt_clip = (TextClip("Partie {}".format(i+1), stroke_width=5, fontsize=50, color='white', bg_color=background)
                  .set_position((280, 950))
                  .set_duration(video.duration))
    final_video = CompositeVideoClip([video, txt_clip])
    final_video_path = os.path.join(path_to_finished_folder, file)
    final_video.write_videofile(final_video_path)
    shutil.move(final_video_path, final_video_path)
