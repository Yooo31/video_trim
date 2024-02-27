from moviepy.editor import *
import random
import os
import re
import shutil

class VideoEditor:
  def __init__(self):
    pass

  @staticmethod
  def set_video_timing(timing):
    try:
      timing = int(timing)

      if timing <= 180:
        with open(os.path.join("process", "timing.txt"), "w") as file:
          file.write(str(timing))
        return True

      else:
        return False

    except ValueError:
      return False

  @staticmethod
  def get_video_timing():
    with open(os.path.join("process", "timing.txt"), "r") as file:
      timing = file.read()
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
    clip = VideoFileClip("../new/output.mp4")
    duration = clip.duration

    part_duration = VideoEditor.get_video_timing()

    for i in range(int(duration/part_duration)+1):
        start_time = i*part_duration
        end_time = start_time+part_duration
        if i == 0:
            subclip = clip.subclip(start_time, end_time)
        else:
            subclip = clip.subclip(start_time-5, min(end_time, duration))
        if i == int(duration/part_duration) and subclip.duration < 20:
            # if the last part is less than 20 sec, add it to the previous part
            previous_part = VideoFileClip("./cut/part_{}.mp4".format(i))
            previous_part = concatenate_videoclips([previous_part, subclip])
            previous_part.write_videofile("./cut/part_{}.mp4".format(i))
        else:
            subclip.write_videofile("./cut/part_{}.mp4".format(i+1))

  @staticmethod
  def add_text():
    def randomColor():
      r = random.randint(200, 255)
      g = random.randint(0, 255)
      b = random.randint(0, 255)

      return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    background = randomColor()

    path_to_cut_folder = "/home/yoan/Project/video_trim/cut"
    path_to_finished_folder = "/home/yoan/Project/video_trim/finished"

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