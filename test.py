total_time = 545
rollback = 3
clip_duration = 60
is_finished = False
start_time = 0
end_time = 0
part = 0

while not is_finished:
  if part != 0:
    start_time = end_time - rollback
  end_time += clip_duration

  part += 1

  if total_time - end_time < 60:
    end_time = total_time
    is_finished = True
  print(f"start_time: {start_time}, end_time: {end_time}")


##################""

# for i in range(int(duration/part_duration)+1):
#         start_time = i*part_duration
#         end_time = start_time+part_duration
#         if i == 0:
#             subclip = clip.subclip(start_time, end_time)
#         else:
#             subclip = clip.subclip(start_time-5, min(end_time, duration))
#         if i == int(duration/part_duration) and subclip.duration < 20:
#             # if the last part is less than 20 sec, add it to the previous part
#             previous_part = VideoFileClip("./cut/part_{}.mp4".format(i))
#             previous_part = concatenate_videoclips([previous_part, subclip])
#             previous_part.write_videofile("./cut/part_{}.mp4".format(i))
#         else:
#             subclip.write_videofile("./cut/part_{}.mp4".format(i+1))