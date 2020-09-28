from discord.ext import commands as com
import discord as d
from random import randint
from datetime import datetime as dt
import typing as t


class MiscCommands(com.Cog):  # Creates class with inheritance from a module class
	def __init__(self, bot):  # Defines initialise function
		self.bot = bot

	@com.command(aliases=["cf", "flip"])  # Creates a command object
	async def coinflip(self, ctx):
		"""Flips a coin"""
		chance = randint(0, 6000)  # Ramdom number
		msg = d.Embed(color=d.Color(65408))  # Creates initial embed with colour
		if chance >= 3000:  # If random number below a threshold, Tails
			msg.title = "Heads!"  # Sets embed title
		elif chance == 3000:  # If random number equals threshold, Coin land on edge
			msg.title = "There is a 1/6000 chance that a US nickel lands on it's upright on it's edge & this is exactly that scenario!"  # Sets embed title
		elif chance <= 3000:  # If random number above a threshold, Heads
			msg.title = "Tails!"  # Sets embed title
		await ctx.send(embed=msg)  # Sends embed

	@com.command(aliases=["clock"])  # Creates a command object with aliases
	async def time(slef, ctx):  # Defines function to become a command
		time = dt.utcnow()
		await ctx.send(embed=d.Embed(color=d.Color(65408), title="The current UTC time is: {0} | The date is: {1}".format(time.strftime("%X"), time.strftime("%x"))))

	@com.command()  # Creats a command object
	async def avatar(self, ctx, user: t.Optional[d.User]):  # Defines function to become a command

		specified = user or ctx.author
		avatar = d.Embed()  # Creates embed
		avatar.set_image(url=specified.avatar_url)  # Sets image embed
		await ctx.send(embed=avatar)  # Sends an embed containing the avatar

	@com.command()
	async def mute(self, ctx, target: d.Member):
		mute = None

		for role in ctx.guild.roles:
			if role.name == "Muted":
				mute = role
				break

		if mute is None:
			mute = await ctx.guild.create_role(name="Muted", permissions=None)  # Creates muted role with no permissions

		await target.add_roles(mute)


def setup(bot):  # Defines setup functiuon for cog
	bot.add_cog(MiscCommands(bot))  # Specifies class to be added as a cog
