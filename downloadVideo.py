from pytube import YouTube

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTube(url)
path = "new/"
mp4_stream = yt.streams.filter(mime_type="video/mp4").first()
mp4_stream.download(path, filename="newVideo.mp4")
print(yt.title)
