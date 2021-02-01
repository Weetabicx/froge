from discord.ext import commands
from discord import Embed, File, FFmpegOpusAudio, PCMVolumeTransformer
from pytube import YouTube
import os
from discord.utils import get
import ffmpeg
import typing

class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.vc = {}
		self.current_track = {}

	@commands.command()
	async def play(self, ctx, url: typing.Optional[str] = None):

		try:
			if ctx.voice_client.is_paused():
				ctx.voice_client.resume()
				await ctx.message.add_reaction('▶️')
				return 
		except AttributeError:
			pass

		if url == None:
			return await ctx.send('No url specified')

		download = YouTube(url)
		audio = download.streams.filter(only_audio=True).first().download(r'C:\Users\usywa\Videos\audio_files')
		try:
			os.rename(audio, fr'C:\Users\usywa\Videos\audio_files\{ctx.author.id}.mp3')
		except FileExistsError:
			os.remove(fr'C:\Users\usywa\Videos\audio_files\{ctx.author.id}.mp3')
			os.rename(audio, fr'C:\Users\usywa\Videos\audio_files\{ctx.author.id}.mp3')

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

		ctx.voice_client.play(FFmpegOpusAudio(fr'C:\Users\usywa\Videos\audio_files\{ctx.author.id}.mp3'))

	@commands.command()
	async def die(self, ctx):
		await ctx.voice_client.disconnect()
		await ctx.message.add_reaction(emoji='✅')

	@commands.command(aliases=['stop'])
	async def pause(self, ctx):
		ctx.voice_client.pause()
		await ctx.message.add_reaction(emoji='⏸️')

	@commands.command()
	async def volume(self, ctx, value: float):
		print(ctx.voice_client.source.volume)

def setup(bot):
	bot.add_cog(Music(bot))