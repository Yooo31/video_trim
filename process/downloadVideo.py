from pytube import YouTube
from datetime import datetime
import json, os

class VideoDownloader:
  def __init__(self, url):
    self.url = url

  def delete_folder_contents(folder_path):
    if os.path.isdir(folder_path):
      for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
          os.remove(file_path)
        elif os.path.isdir(file_path):
          VideoDownloader.delete_folder_contents(file_path)

  def validate_url(self):
    try:
      YouTube(self.url).check_availability()
      return True

    except Exception as e:
      print("L'URL est invalide :", e)
      return False

  def get_title_and_author(self):
    video = YouTube(self.url)
    title = video.title
    author = video.author

    with open("informations.json", "r+") as file:
      data = json.load(file)
      data["title"] = title
      data["author"] = author
      file.seek(0)
      json.dump(data, file, indent=2)

    return title, author

  def download_video(self):
    VideoDownloader.delete_folder_contents("./new")
    VideoDownloader.delete_folder_contents("./finished")
    VideoDownloader.delete_folder_contents("./cut")

    video = YouTube(self.url)
    video.streams.filter(file_extension='mp4').first().download(output_path="./new", filename='newVideo.mp4')

    with open("informations.json", "r+") as file:
      data = json.load(file)
      data["last_url"] = self.url
      data["last_date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      file.seek(0)
      json.dump(data, file, indent=2)

