from moviepy.editor import *

def cutVideo(time):
    clip = VideoFileClip("../new/output.mp4")
    duration = clip.duration

    part_duration = time

    for i in range(int(duration/part_duration)+1):
        start_time = i*part_duration
        end_time = start_time+part_duration
        if i == 0:
            subclip = clip.subclip(start_time, end_time)
        else:
            subclip = clip.subclip(start_time-5, min(end_time, duration))
        if i == int(duration/part_duration) and subclip.duration < 20:
            # if the last part is less than 20 sec, add it to the previous part
            previous_part = VideoFileClip("/home/yoan/Project/video_trim/cut/part_{}.mp4".format(i))
            previous_part = concatenate_videoclips([previous_part, subclip])
            previous_part.write_videofile("/home/yoan/Project/video_trim/cut/part_{}.mp4".format(i))
        else:
            subclip.write_videofile("/home/yoan/Project/video_trim/cut/part_{}.mp4".format(i+1))
