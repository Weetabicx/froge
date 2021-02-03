from discord.ext import commands
from discord import Embed, File, FFmpegOpusAudio, PCMVolumeTransformer
import os
from discord.utils import get
import ffmpeg
import typing
from math import floor
import asyncio


class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.vc = {}
		self.current = {}
		self.queue = {}

	def audio_download(url):

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
		info = ydl.extract_info(url, download=False)

		title = info.get('title', None)
		duration = info.get('duration', None)

		ydl.download([url])
		return title, duration

	@commands.command()
	async def play(self, ctx, url: typing.Optional[str] = None):
		"""Downloads youtube url and plays video"""

		if ctx.voice_client.is_playing():
			self.queue[ctx.guild.id] = []
			self.queue[ctx.guild.id].append(url)

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

		audio_download(url)

		try:
			self.vc[ctx.guild.id] = ctx.author.voice.channel
		except AttributeError:
			return await ctx.send('You must be in voice channle to use this command')

		voice = get(self.bot.voice_clients, guild=ctx.guild)

		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await self.vc[ctx.guild.id].connect()

		await ctx.guild.change_voice_state(channel=self.vc[ctx.guild.id], self_mute=False, self_deaf=True)

		queue_value = self.current.get(ctx.guild.id) or 0
		ctx.voice_client.play(FFmpegOpusAudio(fr'C:\Users\usywa\Videos\audio_files\{ctx.guild.id}\{queue_value}.mp3'))
		self.current_number[ctx.guild.id] = 0


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
		await self.call(ctx)

    @commands.is_owner()  # Runs a commands.Check
	@commands.command()
	async def queue_player(self, ctx):


		

def setup(bot):
	bot.add_cog(Music(bot))