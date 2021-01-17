# Imports modules
from discord.ext import commands
import discord


class Presence(commands.Cog):  # Creates a class
	def __init__(self, bot):  # Define initalise function to run on class call
		self.bot = bot  # Set's bot var to wider class scope

	@commands.Cog.listener("on_ready")  # Listener for on ready event 
	async def status(self):  # Runs function on ready
		await self.bot.change_presence(activity=discord.Game(name="Swag"))  # Set's discord activity 

def setup(bot):  # Define setup
	bot.add_cog(Presence(bot))  # Adds the cog to the bot
