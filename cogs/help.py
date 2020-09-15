from discord.ext import commands as com
import discord as d


class Help(com.Cog):  # Creates a class with inheritance from a module class
	def __init__(self, bot):  # Defines initialise function
		self.bot = bot  # Allows variable to be used within each function in class

	@com.group(case_insensitive=True, invoke_without_command=True)  # Creates command group object
	async def help(self, ctx):  # Defines function to become a command
		"""Shows all available commands"""

		help = d.Embed(title="All available commands", colour=d.Color(65408))  # Creates discord embed object
		help.add_field(name="Voting", value="How to use the voting system!", inline=False)  # Creates a field within embed
		help.add_field(name="Economy", value="How to use the economy system!", inline=False)  # Creates a field within embed
		help.add_field(name="Misc", value="How to use the miscellaneous commands!", inline=False)  # Creates a field within embed
		await ctx.author.send(embed=help)  # Sends embed

	@help.command()  # Creates command in a command group
	async def voting(self, ctx):  # Defines function to become a command
		"""Provides details and usage of the voting system"""

		voting = d.Embed(title="Voting functionality and usage!", colour=d.Color(65408), description="Commands")  # Creates inital embed object
		voting.add_field(name="Starting a vote", value="f!vote {Number of votes allowed}, {time limit, min:10m, max:24hr, default: 15m} {Vote Subject}", inline=False)  # Adds field in embed object
		voting.add_field(name="Cancelling a vote", value="f!vote cancel", inline=False)  # Adds field in embed object
		voting.add_field(name="Prematurely ending a vote", value="f!vote end", inline=False)  # Adds field in embed object
		voting.add_field(name="Showing current votes", value="f!vote current", inline=False)  # Adds field in embed object

	@help.command(aliases=["miscellaneous", "other"])  # Creates a command object in a command group
	async def misc(self, ctx):
		pass
		misc = d.Embed(title="Misc commands usage!", colour=d.Color(65408), description="Commands")
		misc.add_field(name="Coin flip", value="f!cp, f!flip, f!coinflip", inline=False)
		misc.add_field(name="Time/date(Cause I never know what date it is)", value="f!time, f!clock")
		await ctx.send(embed=misc)


def setup(bot):  # Define setup function
	bot.add_cog(Help(bot))  # Specifies the class which to add as a cog