from moviepy.editor import *
import random
import os
import re
import shutil
import json

class VideoEditor:
  def __init__(self):
    pass

  @staticmethod
  def set_video_timing(timing):
    try:
      timing = int(timing)

      if timing <= 180:
        with open("informations.json", "r+") as file:
          data = json.load(file)
          data["timing"] = timing
          file.seek(0)
          json.dump(data, file, indent=2)

        return True

      else:
        return False

    except ValueError:
      return False

  @staticmethod
  def get_video_timing():
    with open("informations.json", "r") as file:
      data = json.load(file)
      timing = data["timing"]

    return int(timing)


  @staticmethod
  def change_format():
    file = "./new/newVideo.mp4"

    clip = VideoFileClip(file)
    # aspect_ratio = clip.aspect_ratio

    resized_clip = clip.resize(width=780)

    black_bg = ColorClip((780,1280), color=(0,0,0))

    final_clip = CompositeVideoClip([black_bg, resized_clip.set_pos(('center', 'center'))])
    final_clip = final_clip.set_duration(resized_clip.duration)

    final_clip.write_videofile("./new/output.mp4")

  @staticmethod
  def cut_video():
    clip = VideoFileClip("./new/output.mp4")
    total_duration = clip.duration
    clip_duration = VideoEditor.get_video_timing()
    rollback = 3
    is_finished = False
    start_time = 0
    end_time = 0
    part = 0

    while not is_finished:
      if part != 0:
        start_time = end_time - rollback
      end_time += clip_duration

      if total_duration - end_time < 60:
        end_time = total_duration
        is_finished = True

      part += 1

      subclip = clip.subclip(start_time, end_time)
      subclip.write_videofile("./cut/part_{}.mp4".format(part))

  @staticmethod
  def add_text():
    def randomColor():
      r = random.randint(200, 255)
      g = random.randint(0, 255)
      b = random.randint(0, 255)

      return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    background = randomColor()

    path_to_cut_folder = "./cut"
    path_to_finished_folder = "./finished"

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