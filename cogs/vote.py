# Imports required modules with keyword
from discord.ext import commands as com
import discord as d
import typing as t
from datetime import datetime as dt, timedelta as td


class Vote(com.Cog):  # Creates a class with inheritance from 'Cog' class
	def __init__(self, bot):  # Initalises the class
		self.bot = bot  # Adds variable to wider scope
		self.vote_msg = {}  # Creates an empty dictionary which will store the vote message of a guild
		self.vote_timers = {}  # Creates an empty dictionary which will store the times at which votes will end
		self.vote_subject = {}  # Creates an empty dictionary which will store the subject for a vote
		self.votes = {}  # Creates an empty dictionary which will store the vote limit on a vote
		self.voteisrunning = {}  # Creates an empty dict which stores a boolean to determnine wheather a vote is running
		self.for_vote = {}  # Creates an empty dict for storing votes for
		self.against_vote = {}  # Creates an empty dict for storing votes against
		self.has_voted = {}  # A dict which stores a list for each guild with a vote running

	def guild_vote_reset(self, guild_id):  # Resets the values for the vote for a guild
		self.vote_msg.pop(guild_id)
		self.vote_timers.pop(guild_id)
		self.vote_subject.pop(guild_id)
		self.votes.pop(guild_id)
		self.voteisrunning.pop(guild_id)
		self.for_vote.pop(guild_id)
		self.against_vote.pop(guild_id)
		self.has_voted.pop(guild_id)

	@com.group(case_insensative=True, invoke_without_command=True)  # Creates command group
	async def vote(self, ctx, votes: t.Optional[int] = 10, timer: t.Optional[int] = 10, *, subject: str):  # Creates function to become a command

		is_running = self.voteisrunning.get(ctx.guild.id)  # Get's a value
		if is_running is True:  # Is a vote already running?
			return  # Stops the program

		self.vote_timers[ctx.guild.id] = dt.utcnow() + td(minutes=timer)  # Assigns the timer value

		vote_embed = d.Embed(color=d.Color(65408))  # Creates the initial discord embed
		vote_embed.title = "Vote for {0}".format(subject)  # Adds the title specifing the vote topic
		vote_embed.description = "Max number of votes: {}".format(votes)  # Adds the description which includes the max vote
		vote_embed.add_field(name="For", value=0, inline=True)  # Adds the for field which will be updated with each new vote
		vote_embed.add_field(name="Against", value=0, inline=True)  # Adds the against field which will be updated with each new vote
		vote_embed.set_footer(text="Vote end time: {}".format(self.vote_timers[ctx.guild.id].strftime("%x %X")))

		self.vote_subject[ctx.guild.id] = subject  # Assigns the subject value
		self.votes[ctx.guild.id] = votes  # Assign the max vote
		self.for_vote[ctx.guild.id] = 0  # Assigns the base value
		self.against_vote[ctx.guild.id] = 0  # Assigns the base value
		self.vote_msg[ctx.guild.id] = await ctx.send(embed=vote_embed)  # Sends the vote embed
		self.voteisrunning[ctx.guild.id] = True  # A vote is now underway
		self.has_voted[ctx.guild.id] = []  # Assings "None" to list

	@vote.command(aliases=["early"])  # Creates command group object with aliases
	async def end(self, ctx):  # Defines function to become a command

		if ctx.guild is None:  # If there is no guild
			return  # Stops function
		vote_status = self.voteisrunning.get(ctx.guild.id)  # Get's the boolean which determines if a vote is running
		if vote_status is None:  # If there is no bollean
			return  # Stops the function

		current_message = self.vote_msg.get(ctx.guild.id)  # Get's the current vote message
		await current_message.delete()  # Deletes the current vote message

		for_votes = self.for_vote.get(ctx.guild.id)
		against_votes = self.against_vote.get(ctx.guild.id)
		max_votes = self.votes.get(ctx.guild.id)
		vote_embed = d.Embed(color=d.Color(65408))  # Creates the initial discord embed
		if for_votes > against_votes:  # If greater number of for votes
			vote_embed.title = "Vote for {0} has ended | Against Wins!".format(self.vote_subject.get(ctx.guild.id))  # Adds the title specifing the vote topic
		elif for_votes < against_votes:  # If greater number of against votes
			vote_embed.title = "Vote for {0} has ended | For Wins!".format(self.vote_subject.get(ctx.guild.id))  # Adds the title specifing the vote topic
		elif for_votes == against_votes:  # If equal number of for and against votes
			vote_embed.title = "Vote for {0} has ended | Tie!".format(self.vote_subject.get(ctx.guild.id))  # Adds the title specifing the vote topic

			vote_embed.description = "Max number of votes: {}".format(max_votes)  # Adds the description which includes the max vote
			vote_embed.add_field(name="For", value=for_votes, inline=True)  # Adds the for field which will be updated with each new vote
			vote_embed.add_field(name="Against", value=against_votes, inline=True)  # Adds the against field which will be updated with each new vote
			vote_embed.set_footer(text="Vote end time: {}".format(self.vote_timers[ctx.guild.id].strftime("%x %X")))

		self.guild_vote_reset(ctx.guild.id)  # Resets values since the vote has ended

	@vote.command(aliases=["current"])  # Creates command object
	async def now(self, ctx):  # Defines function to be command
		if ctx.guild is None:
			return
		vote_status = self.voteisrunning.get(ctx.guild.id)  # Get's the boolean which determines if a vote is running
		if vote_status is None:  # If there is no bollean
			return  # Stops the function

		message = self.vote_msg.get(ctx.guild.id)  # Get's the message
		await message.delete()  # Deletes the message

		vote_embed = d.Embed(color=d.Color(65408))  # Creates the initial discord embed
		vote_embed.title = "Vote for {0}".format(self.vote_subject.get(ctx.guild.id))  # Adds the title specifing the vote topic
		vote_embed.description = "Max number of votes: {}".format(self.votes.get(ctx.guild.id))  # Adds the description which includes the max vote
		vote_embed.add_field(name="For", value=self.for_vote.get(ctx.guild.id), inline=True)  # Adds the for field which will be updated with each new vote
		vote_embed.add_field(name="Against", value=self.against_vote.get(ctx.guild.id), inline=True)  # Adds the against field which will be updated with each new vote
		vote_embed.set_footer(text="Vote end time: {}".format(self.vote_timers[ctx.guild.id].strftime("%x %X")))

		self.vote_msg[ctx.guild.id] = await ctx.send(embed=vote_embed)  # Sends the vote embed

	@vote.command(aliases=["stop", "terminate"])  # Creates command group object with aliases
	async def cancel(self, ctx):  # Defines function to become a command
		message = self.vote_msg.get(ctx.guild.id)  # Get's the message
		await message.delete()  # Deletes the message

		vote_embed = d.Embed(color=d.Color(65408))  # Creates the initial discord embed
		vote_embed.title = "Vote for {0} cancelled!".format(self.vote_subject.get(ctx.guild.id))  # Adds the title specifing the vote topic
		self.vote_msg[ctx.guild.id] = await ctx.send(embed=vote_embed)  # Sends the vote embed

		self.guild_vote_reset(ctx.guild.id)

	@com.Cog.listener('on_message')  # When the message event is called
	async def vote_counter(self, message):  # Defines a function to be run whever the on message event is called

		if message.guild is None:  # If there is no guild object tied to the message
			return  # Exits the function
		elif message.author.bot:  # If the message is from a bot
			return  # Stops the function
		else:  # Otherwise
			vote_status = self.voteisrunning.get(message.guild.id)  # Get's the boolean which determines if a vote is running
			if vote_status is None:  # If there is no bollean
				return  # Stops the function
			else:  # If a vote is running
				already_voted = self.has_voted[message.guild.id]  # Get's the list value for users who have already voted

				if already_voted is None:  # If none then adds placeholder
					already_voted = ["placeholder"]  # Error I couldn't be bothered fixing properly

				if 'for!' in message.content.lower():  # If the message is for the vote
					if message.author.id in already_voted:  # If the user has already voted
						return await message.channel.send(embed=d.Embed(color=d.Color(65408), title="You have already voted!"))  # Send exit message
					self.for_vote[message.guild.id] += 1  # Adds one to the for counter

				elif 'against!' in message.content.lower():  # If the message is against the vote
					if message.author.id in already_voted:  # If the user has already voted
						return await message.channel.send(embed=d.Embed(color=d.Color(65408), title="You have already voted!"))  # Send exit message
					self.against_vote[message.guild.id] += 1  # Adds one to the against vote counter
				else:  # If the text isn't related to the vote
					return  # Stops the function

				already_voted.append(message.author.id)  # Appends to new list
				self.has_voted[message.guild.id] = already_voted  # Set's new list

				for_votes = self.for_vote.get(message.guild.id)  # Assigns for votes as local variable to save typing
				against_votes = self.against_vote.get(message.guild.id)  # Assigns against votes as local variable to save typing
				max_votes = self.votes.get(message.guild.id)  # Assigns vote limit as local variable to save typing

				if for_votes + against_votes == max_votes:  # If the vote has ended
					current_message = self.vote_msg.get(message.guild.id)  # Get's the current vote message
					await current_message.delete()  # Deletes the current vote message

					vote_embed = d.Embed(color=d.Color(65408))  # Creates the initial discord embed
					if for_votes > against_votes:  # If greater number of for votes
						vote_embed.title = "Vote for {0} has ended | Against Wins!".format(self.vote_subject.get(message.guild.id))  # Adds the title specifing the vote topic
					elif for_votes < against_votes:  # If greater number of against votes
						vote_embed.title = "Vote for {0} has ended | For Wins!".format(self.vote_subject.get(message.guild.id))  # Adds the title specifing the vote topic
					elif for_votes == against_votes:  # If equal number of for and against votes
						vote_embed.title = "Vote for {0} has ended | Tie!".format(self.vote_subject.get(message.guild.id))  # Adds the title specifing the vote topic

					vote_embed.description = "Max number of votes: {}".format(max_votes)  # Adds the description which includes the max vote
					vote_embed.add_field(name="For", value=for_votes, inline=True)  # Adds the for field which will be updated with each new vote
					vote_embed.add_field(name="Against", value=against_votes, inline=True)  # Adds the against field which will be updated with each new vote
					vote_embed.set_footer(text="Vote end time: {}".format(self.vote_timers[message.guild.id].strftime("%x %X")))

					self.guild_vote_reset(message.guild.id)  # Resets values since the vote has ended

				elif for_votes + against_votes < max_votes:
					current_message = self.vote_msg.get(message.guild.id)  # Get's the current vote message
					await current_message.delete()  # Deletes the current vote message

					vote_embed = d.Embed(color=d.Color(65408))  # Creates the initial discord embed
					vote_embed.title = "Vote for {0}".format(self.vote_subject.get(message.guild.id))  # Adds the title specifing the vote topic
					vote_embed.description = "Max number of votes: {}".format(max_votes)  # Adds the description which includes the max vote
					vote_embed.add_field(name="For", value=for_votes, inline=True)  # Adds the for field which will be updated with each new vote
					vote_embed.add_field(name="Against", value=against_votes, inline=True)  # Adds the against field which will be updated with each new vote
					vote_embed.set_footer(text="Vote end time: {}".format(self.vote_timers[message.guild.id].strftime("%x %X")))  # Shows vote end time
					self.vote_msg[message.guild.id] = await message.channel.send(embed=vote_embed)  # Sends the vote embed
				else:  # max number of votes has been reached
					return  # Stops the function



def setup(bot):  # Defines bot setup
	bot.add_cog(Vote(bot))  # Specifies class to be added as a cog
