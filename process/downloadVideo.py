from pytube import YouTube

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
    return title, author

  def download_video(self):
    video = YouTube(self.url)
    video.streams.filter(file_extension='mp4').first().download(output_path="./new", filename='newVideo.mp4')

if __name__ == '__main__':
    url = input("Entrez l'URL de la vidéo YouTube : ")
    downloader = VideoDownloader(url)

    if downloader.validate_url():
        title, author = downloader.get_title_and_author()
        downloader.download_video()

        print(f"Crédit : {title} | {author}")
        print("La vidéo a été téléchargée avec succès.")

    else:
        print("L'URL fournie est invalide.")