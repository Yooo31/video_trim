from moviepy.editor import *
import os
import shutil
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})


path_to_cut_folder = "cut"
path_to_finished_folder = "finished"

for i, file in enumerate(os.listdir(path_to_cut_folder)):
    video_path = os.path.join(path_to_cut_folder, file)
    video = VideoFileClip(video_path)
    txt_clip = (TextClip("Partie {}".format(i+1), fontsize=24, color='white')
                .set_position('bottom')
                .set_duration(video.duration))
    final_video = CompositeVideoClip([video, txt_clip])
    final_video_path = os.path.join(path_to_finished_folder, file)
    final_video.write_videofile(final_video_path)
    shutil.move(final_video_path, final_video_path)

