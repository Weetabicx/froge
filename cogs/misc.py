from discord.ext import commands as com
import discord as d
import random
from datetime import datetime as dt
import typing as t
from cogs.utils.readable_time import readable_time


class MiscCommands(com.Cog):  # Creates class with inheritance from a module class
	def __init__(self, bot):  # Defines initialise function
		self.bot = bot

	@com.command(aliases=["flip"])  # Creates a command object
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
		time = dt.utcnow()  # Assigns utc time
		await ctx.send(embed=d.Embed(color=d.Color(65408), title="The current UTC time is: {0} | The date is: {1}".format(time.strftime("%X"), time.strftime("%x"))))

	@com.command()  # Creats a command object
	async def avatar(self, ctx, user: t.Optional[d.User]):  # Defines function to become a command

		specified = user or ctx.author
		avatar = d.Embed(color=d.Color(65408))  # Creates embed
		avatar.set_image(url=specified.avatar_url)  # Sets image embed
		await ctx.send(embed=avatar)  # Sends an embed containing the avatar

	@com.command()  # Decorator with makes a function into a discord command
	async def age(self, ctx):

		specified = ctx.author
		await ctx.send(embed=d.Embed(color=d.Color(65408), description=specified.created_at.strftime("%c")))

	@com.cooldown(1, 86_400, com.BucketType.user)
	@com.command()
	async def swag(self, ctx):
		swag_factor = random.uniform(-100, 100)
		message = ""
		if swag_factor > 90:
			message = random.choice(["You are so smexy", "I am envious of your swag", "I am in absolute AWE!"])
		elif swag_factor <=90 and swag_factor > 50:
			message = random.choice(["You are pretty swag! nice.", "That's a reasonable amount of swag you have", "Decent swag!"])
		elif swag_factor <=50 and swag_factor >=-50:
			message = random.choice(["Your swag is below averge. YIKES!", "Eww, I hope you don't stay long.", "You are shunned by your friends and family..."])
		elif swag_factor >=-90 and swag_factor <-50:
			message = random.choice(["This is a amazingly terrible amount of swag...", "You should rethink your life choices...", "You are not swag, like even remotely..."])
		elif swag_factor <-90:
			message = random.choice(["How are you even like this????", "What have you done with your life...", "This is genuinely sad..."])

		await ctx.send(f"you have a swag factor of {swag_factor}! {message}")

	@swag.error
	async def swag_error(self, ctx, error):
		if isinstance(error, com.CommandOnCooldown):
			await ctx.send(f"This command is on cooldown. Try again in {readable_time(round(error.retry_after, 0))}")

	@com.command()  # Command decorator  
	async def dababy(self, ctx):  # Defines the function to run on command call
		dababies = [511490437853478925, 266999593084911616]  
		if ctx.author.id in dababies:
			await ctx.send("You are dababy")
		else:
			await ctx.send("You are not dababy")

	@com.command()  # Command decorator
	async def git(self, ctx):  #  Defines command 
		await ctx.send(embed=d.Embed(color=d.Color(65408), title="https://github.com/Weetabicx/froge"))  # Sends github repo


def setup(bot):  # Defines setup functiuon for cog
	bot.add_cog(MiscCommands(bot))  # Specifies class to be added as a cog
