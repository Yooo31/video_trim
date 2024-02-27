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

  def download_video_with_subtitles(self, output_path='./temp'):
    video = YouTube(self.url)

    captions = video.captions
    subtitle = captions.get_by_language_code('en')

    if subtitle:
        video.streams.filter(file_extension='mp4').first().download(output_path=output_path, filename='newVideo.mp4')
        subtitle.download(output_path=output_path, filename='subtitles')
        print("La vidéo et les sous-titres en français ont été téléchargés avec succès.")
    else:
      video.streams.filter(file_extension='mp4').first().download(output_path=output_path, filename='newVideo.mp4')
      print("La vidéo a été téléchargée avec succès (sans sous-titres).")

if __name__ == '__main__':
    url = input("Entrez l'URL de la vidéo YouTube : ")
    downloader = VideoDownloader(url)

    if downloader.validate_url():
        title, author = downloader.get_title_and_author()
        print(f"Crédit : {title} | {author}")

        output_path = './temp'  # Répertoire de téléchargement
        downloader.download_video_with_subtitles(output_path)
        print("La vidéo a été téléchargée avec succès.")
    else:
        print("L'URL fournie est invalide.")