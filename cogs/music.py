from discord.ext import commands, tasks
from discord import Embed, File, FFmpegOpusAudio, PCMVolumeTransformer
import os
from discord.utils import get
import ffmpeg
import typing
from math import floor
import asyncio
import youtube_dl
import threading 

def audio_download(url:str, guild: int):
	"""Download youtube audio"""

	# Config for downloading youtube audio
	config = {
		'format': 'bestaudio/best',
			'outtmpl': fr'C:\Users\usywa\Videos\audio_files\{guild}\0' + '.mp3',
			'noplaylist': True,
			'continue_dl': True,
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192', }]
	}

	with youtube_dl.YoutubeDL(config) as ydl:
		ydl.cache.remove()
		info = ydl.extract_info(url, download=False)

		title = info.get('title', None)
		duration = info.get('duration', None)
		ydl.download([url])
	return title, duration # Returns the title and duration 


class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.vc = {}
		self.current = {}
		self.queue = {}
		self.current = {}
		self.stop = {}
		self.next = {}


	@commands.command()  # Transforms a function into a command
	async def play(self, ctx, url: typing.Optional[str] = None):

		try:
			self.vc[ctx.guild.id] = ctx.author.voice.channel
		except AttributeError:
			return await ctx.send('You must be in voice channle to use this command')
			
		try:
			if ctx.voice_client.is_playing():
				return print(True)
		except:
			pass

		try:
			if ctx.voice_client.is_playing():
				title, duration = audio_download(url, ctx.guild.id)
				await self.queue[ctx.guild.id].put(fr'C:\Users\usywa\Videos\audio_files\{ctx.guild.id}\{self.current.get(ctx.guild.id)}.mp3')
				self.current[ctx.guild.id] += 1
				await ctx.send(f'Queued {title}, {duration}')
				return 
		except AttributeError:
			pass

		# Unpauses the player if was paused
		try:
			if ctx.voice_client.is_paused():
				ctx.voice_client.resume()
				await ctx.message.add_reaction('▶️')
				return 
		except AttributeError:
			pass

		if url == None:
			return await ctx.send('No url specified')  # If no url is provided

		self.current[ctx.guild.id] = 0
		title, duration = audio_download(url, ctx.guild.id)
		await ctx.send(f'Playing {title}, {duration}')


		voice = get(self.bot.voice_clients, guild=ctx.guild)

		if voice and voice.is_connected():
			await voice.move_to(self.vc[ctx.guild.id])
		else:
			voice = await self.vc[ctx.guild.id].connect()

		await ctx.guild.change_voice_state(channel=self.vc[ctx.guild.id], self_mute=False, self_deaf=True)

		self.queue[ctx.guild.id] = asyncio.Queue()
		self.next[ctx.guild.id] = asyncio.Event()


		await self.queue[ctx.guild.id].put(fr'C:\Users\usywa\Videos\audio_files\{ctx.guild.id}\0.mp3')

		self.current[ctx.guild.id] += 1

		await self.queue_player(ctx)


	@commands.command()
	async def die(self, ctx):
		"""Leaves voice channel"""
		await ctx.voice_client.disconnect()
		await ctx.message.add_reaction(emoji='✅')

	@commands.command(aliases=['stop'])
	async def pause(self, ctx):
		"""pauses the currently playing song"""
		ctx.voice_client.pause()
		await ctx.message.add_reaction(emoji='⏸️')

	@commands.command()
	async def volume(self, ctx):
		pass

	@commands.is_owner()  # Runs a commands.Check
	@commands.command()
	async def queue_player(self, ctx):
		src = await self.queue[ctx.guild.id].get()
		ctx.voice_client.play(FFmpegOpusAudio(src), after=None)
		await self.queue_player(ctx)
	
		

	@commands.is_owner()
	@commands.command()
	async def play_next(self, ctx):
		pass

		

def setup(bot):
	bot.add_cog(Music(bot))