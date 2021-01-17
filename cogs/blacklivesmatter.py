from discord.ext import commands as com
import discord as d


class BlackLivesMatter(com.Cog):
	def __init__(self, bot):
		self.bot = bot

	@com.group()  # Creates a command group object
	async def blm(self, ctx):  # Defines function to become a command
		blm_embed = d.Ember(title="Black Lives Matter Information", url="https://blacklivesmatter.com/")  # Creates the embed with title & url
		blm_embed.add_field(name="Petition Links as of Jun 1 2020", value="https://docs.google.com/document/d/1-He4uzB2k0oBybIfQZ_B9uulDYlmfv3GzRkILdSUQNw", inline=False)  # Adds field
		blm_embed.add_field(name="Incident repository", value="https://github.com/2020PB/police-brutality", inline=False)  # Adds field
		blm_embed.add_field(name="Police brutality mapping", value="https://mappingpoliceviolence.org/", inline=False)  # Adds field
		await ctx.send(embed=blm_embed)


def setup(bot):
	bot.add_cog(BlackLivesMatter(bot))
