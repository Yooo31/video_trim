import glob

class VideoSender:
  @staticmethod
  def send_videos(bot, chat_id):
    videos_path = "./cut/*.mp4"
    video_files = glob.glob(videos_path)

    if video_files:
      for video_file in video_files:
        bot.send_document(chat_id=chat_id, document=open(video_file, 'rb'))
    else:
      bot.send_message(chat_id=chat_id, text="Aucune vidéo disponible pour le moment.")
