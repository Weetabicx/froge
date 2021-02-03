import youtube_dl
import json


def download_clip(url, name):
	config = {
	'format': 'bestaudio/best',
		'outtmpl': name + '.mp3',
		'noplaylist': True,
		'continue_dl': True,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192', }]
	}
	with youtube_dl.YoutubeDL(config) as ydl:
		ydl.cache.remove()
		info_dict = ydl.extract_info(url, download=False)

		title = info_dict.get('title', None)
		duration = info_dict.get('duration', none)
		ydl.download([url])


download_clip(r'https://www.youtube.com/watch?v=1fXYDkpfHsk', 'audio')