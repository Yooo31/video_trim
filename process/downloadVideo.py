from pytube import YouTube
from datetime import datetime
import json

class VideoDownloader:
  def __init__(self, url):
    self.url = url

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
    video = YouTube(self.url)
    video.streams.filter(file_extension='mp4').first().download(output_path="./new", filename='newVideo.mp4')

    with open("informations.json", "r+") as file:
      data = json.load(file)
      data["last_url"] = self.url
      data["last_date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      file.seek(0)
      json.dump(data, file, indent=2)

