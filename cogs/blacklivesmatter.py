from discord.ext import commands
from discord import Embed

class BlackLivesMatter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		await message.channel.send("Here!")

		
	@commands.group()  # Creates a command group object
	async def blm(self, ctx):  # Defines function to become a command
		blm_embed = Embed(title="Black Lives Matter Information", url="https://blacklivesmatter.com/")  # Creates the embed with title & url
		blm_embed.add_field(name="Police brutality mapping", value="https://mappingpoliceviolence.org/", inline=False)  # Adds field
		await ctx.send(embed=blm_embed)

async def setup(bot):
	await bot.add_cog(BlackLivesMatter(bot))
