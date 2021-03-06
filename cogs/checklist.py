from discord.ext import commands
from discord import Embed, tasks
import typing

class Checklist(commands.Cog):  # Creating class with comannds.Cog inheritance
	def __init__(self, bot):
		self.bot = bot
		self.list = {}  # Stores a list of dictionaries, eg userID :[{'title': 'title from user', 'description': 'description from user'}]

	@commands.group(name='checklist', aliases=['list', 'reminders', 'reminder'], case_insensitive=True)
	async def checklist(self, ctx):

		if ctx.invoked_subcommand:  # If a sub commands is called
			return  # Don't run this function, only the function tied to the subcommmand
		
		if self.list.get(ctx.author.id) is None:  # If the user doesn't have a 
			return await ctx.send('No items in list, use \'%checklist add\'')

		embed = Embed()
		for x in range(len(self.list.get(ctx.author.id))):
			value = self.list.get(ctx.author.id)[x]['description']
			name = self.list.get(ctx.author.id)[x]['title']
			embed.add_field(name=f'**{name}**', value=f'```{value}```', inline=False)

		await ctx.send(embed=embed)

	@checklist.command()  # Adds a subcommand to checklist command group
	async def add(self, ctx, title, *, description):

		if self.list.get(ctx.author.id) is None:  # If the user has not made a list yet
			self.list[ctx.author.id] = []  # Create an empty list
 
		if len(self.list.get(ctx.author.id)) == 10:  # If the list has ten items
			return await ctx.send('10 list items is the maximum.')  # Refuses the addition of another object eg max ten list items 

		dictionary = {'title': title, 'description': description}  # Creates the dict to add to the list
		self.list[ctx.author.id].append(dictionary)  # Adds the dict
		
		await ctx.message.add_reaction(emoji='✅')  # Confirms to the user the command has been used succesfully 

	@checklist.command(aliases=['rm', 'delete'])  # Adds a subcommand to checklist command group
	async def remove(self, ctx, value: str): 

		if len(value) > 1:
			# Deletes the list entry with the specified title
			title = value
			for index, dic in enumerate(self.list.get(ctx.author.id)):
				if dic['title'] == title:
					self.list[ctx.author.id].pop(index)
				if len(self.list.get(ctx.author.id)) == 0:
					self.list.pop(ctx.author.id)
		elif len(value) == 1:
			try:
				# Deletes the list entry with the specified index
				index = int(value) - 1
				self.list[ctx.author.id].pop(index)
				if len(self.list.get(ctx.author.id)) == 0:
					self.list.pop(ctx.author.id)
			except ValueError:
				# Deletes the list entry with the specified title
				title = value
				for index, dic in enumerate(self.list.get(ctx.author.id)):
					if dic['title'] == title:
						self.list[ctx.author.id].pop(index)
					if len(self.list.get(ctx.author.id)) == 0:
						self.list.pop(ctx.author.id)


			index = int(value) - 1
			self.list[ctx.author.id].pop(index)
			if len(self.list.get(ctx.author.id)) == 0:
				self.list.pop(ctx.author.id)

		await ctx.message.add_reaction(emoji='✅')  # Confirms to the user the command has been used succesfully


def setup(bot):
	bot.add_cog(Checklist(bot))