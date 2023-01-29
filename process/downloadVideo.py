from pytube import YouTube

def downloadVideo(url):
  yt = YouTube(url)

  mp4_stream = yt.streams.filter(mime_type="video/mp4").first()
  mp4_stream.download(filename="/home/yoan/Project/video_trim/new/newVideo.mp4")

  return yt.title
