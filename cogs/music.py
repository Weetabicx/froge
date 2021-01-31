from discord.ext import commands
from discord import Embed, File
from pytube import YouTube
import os
from discord.utils import get

class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.vc = {}

	@commands.command()
	async def play(self, ctx, url: str):
		download = YouTube(url)
		audio = download.streams.filter(only_audio=True).first().download(r'C:\Users\usywa\Videos\audio_files')
		try:
			os.rename(audio, fr'C:\Users\usywa\Videos\audio_files\{ctx.author.id}.mp3')
		except FileExistsError:
			os.remove(fr'C:\Users\usywa\Videos\audio_files\{ctx.author.id}.mp3')
			os.rename(audio, fr'C:\Users\usywa\Videos\audio_files\{ctx.author.id}.mp3')

		self.vc[ctx.guild.id] = ctx.author.voice.channel

		voice = get(self.bot.voice_clients, guild=ctx.guild)

		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await self.vc[ctx.guild.id].connect()

	@commands.command()
	async def die(self, ctx):
		await ctx.voice_client.disconnect()

def setup(bot):
	bot.add_cog(Music(bot))