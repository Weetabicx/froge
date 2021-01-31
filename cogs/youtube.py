from pytube import YouTube
import os

yt = YouTube(str(input("Enter the URL of the video you want to download: \n>> ")))

print("Select download format:")
print("1: Video file with audio (.mp4)")
print("2: Audio only (.mp3)")

media_type = input(">> ")

if media_type == "1":
    video = yt.streams.first()

elif media_type == "2":
    video = yt.streams.filter(only_audio = True).first()

else:
    print("Invalid selection.")

print("Enter the destination (leave blank for current directory)")
destination = str(input(">> ")) or '.'

out_file = video.download(output_path = destination)

if media_type == "2":
    base, ext = os.path.splitext(out_file)
    print(base, ext)
    new_file = 'audio' + '.mp3'
    os.rename(out_file, new_file)

print(yt.title + " has been successfully downloaded.")