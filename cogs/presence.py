from discord.ext import commands
import discord


class Presence(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener("on_ready")
	async def status(self):
		await self.bot.change_presence(activity=discord.Game(name="Swag"))

def setup(bot):
	bot.add_cog(Presence(bot))
