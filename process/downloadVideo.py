from pytube import YouTube

def downloadVideo(url):
  yt = YouTube(url)
  path = "new/"

  mp4_stream = yt.streams.filter(mime_type="video/mp4").first()
  mp4_stream.download(path, filename="newVideo.mp4")

  return yt.title
