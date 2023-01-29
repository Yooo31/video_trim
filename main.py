from process import downloadVideo, changeVideoFormat, cutVideos, addText

print("Start downloading this video")
title = downloadVideo.downloadVideo("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print("Video downloaded")

print("Start change video format")
changeVideoFormat.changeFormat()
print("Format is changed")

print("Start cuting video")
cutVideos.cutVideo(75)
print("Video are cut")

print("Start add text to video")
addText.addText()
print(("Text added"))