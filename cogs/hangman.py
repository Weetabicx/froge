# Imports libraries
from discord.ext import commands
import discord
import json
import random 
import typing

class Hangman(commands.Cog):  # Creates a class with inheritance from Cog class of commands
	def __init__(self, bot):  # Defines initialise function to setup initial variables 
		self.bot = bot  # Assigns the bot variable to a wider class scope
		self.word = {}  # Stores the word specific to the user (Potentionally guild)
		self.hints = {}  # Stores the hints specific to the user (Potentionally guild)
		self.current_hint = {}
		self.hidden_word = {}  # Stores the displayed word to the user (Potentionally guild)
		self.guessed = {}  # Stores the guessed word to the user (Potentionally guild)
		self.guesses = {}  # Stores the guesses remaining to the user (Potentionally guild)
		self.running = {}  # Stores a boolean to determine if a game is running to prevent errors
		self.message = {}  # Stores a discord message object to be assigned and deleted to prevent clutter
		self.categories = ("movies", "character", "series")  # The possible categories

	def game_end(self, uid: int):
		self.word.pop(uid)
		self.hints.pop(uid)
		self.hidden_word.pop(uid)
		self.guessed.pop(uid)
		self.guesses.pop(uid)
		self.running.pop(uid)
		self.message.pop(uid)

	def read_in_word(self, category: str):  # Defines function
		"""This will read in words and hints from a local json file"""
		with open("hangman.json", "r") as file:  # Opens file to automatically close
			data = json.load(file)  # Loads file as json
			word_dict = data[category]  # Picks the specified category
			word = random.choice(list(word_dict.keys()))
			return (word, word_dict[word])  # Returns a randomly selected word and the corrosponding hints

	@commands.command()  # A decorator which turns an asyncronus function into a command object
	async def hangman(self, ctx, category: typing.Optional[str] = "n/a"):  # Defines the function run on command call

		if ctx.guild or self.running.get(ctx.author.id):  # If a scenario were the command cannot be run is in play
			if ctx.guild:  # If the command is used in a guild
				return await ctx.author.send("This command is DM only for now.")  # Returns the function and sends the error message
			elif self.running.get(ctx.author.id):  # If the command has already been used and a game is still running
				return await ctx.send("A game of hangman is currently running")  # Returns the function and send the error message

		if category == "n/a":  # If no category was specified by the user
			category = random.choice(self.categories)  # Randomly select a category

		self.word[ctx.author.id], self.hints[ctx.author.id] = self.read_in_word(category)  # Assigns the word and hints for this game
		self.running[ctx.author.id] = True  # Assigns the running check to true
		self.guesses[ctx.author.id] = 6  # Assigns the number of guesses to the same number of attempts as a regular hangman game
		self.hidden_word[ctx.author.id] = ""  # Creates the inital empty string
		self.guessed[ctx.author.id] = []  # Creates the initall empty list
		self.current_hint[ctx.author.id] = 0

		for index, char in enumerate(self.word.get(ctx.author.id)):  # For each character in the stored word
			if char == " ":  # If the character is a space
				self.hidden_word[ctx.author.id] += " "  # Add a space to the hidden word
			elif char != " ":  # If the character is not a space
				self.hidden_word[ctx.author.id] += "\*"  # Hides the letter
			else:  # Otherwise (This line is unnecessary, and is used only for clarification)
				continue  # Cycles to the next iteration of loop

		embed = discord.Embed(color=discord.Color(65408))  # Creates inital embed with coloured sidebar
		embed.description = f"Word: {self.hidden_word.get(ctx.author.id)}"  # Adds description
		embed.add_field(name="Guesses", value=self.guesses.get(ctx.author.id), inline=False)  # Adds a filed
		embed.add_field(name="Guessed", value=self.guessed.get(ctx.author.id), inline=False)  # Adds a filed
		self.message[ctx.author.id] = await ctx.send(embed=embed)  # Sends and assigns the embed

	@commands.Cog.listener("on_message")  # A decorator which runs the function on every message send the bot can see
	async def guess_processing(self, message):  # Defines function to run on every message


		if message.guild:  # If the message is from a server
			return  # Ignore and stop running
		if not(self.running.get(message.author.id)):  # If there is no game tied to this user
			return  # Ignore and stop running

		if message.content.lower().startswith("guess"):

			try:  # Tries to get a guessed letter
				attempt = message.content.lower().split(" ")  # Splits the message into words
				if len(attempt) > 2:  # If the guess is for the whole word
					attempt = " ".join(attempt[1:])  # Join the seperate words into one attempt
				else:  # If only a letter is guessed
					attempt = attempt[1]  # Assign it to the letter
			except ValueError:  # If the message only containted "guess"
				return await message.author.send("A letter or word was not specified")  # Send error message

			if attempt in self.guessed.get(message.author.id):  # If the guess has already been submitted
				return await message.author.send("You have already guessed this!")  # Sends error message

			if len(attempt) > 1:  # If the guess was a word
				if attempt.lower() == self.word.get(message.author.id):  # Checks if the guess is correct
					await message.author.send("The guess was correct!")  # Send final confirmation message
					self.game_end(message.author.id)  # Ends the game
					return  # Stops the function
				else:
					await message.author.send(f"You guessed the whole word... but it was *{self.word.get(message.author.id)}*. Game over!")  # Send final confirmation message
					self.game_end(message.author.id)  # Ends the game
					return  # Stops the function

			if attempt in self.word.get(message.author.id):  # If the guess is correct
				self.guessed[message.author.id].append(attempt)  # Adds to guessed list
				self.hidden_word[message.author.id] = ""  # Clears the current hidden word
				for index, char in enumerate(self.word.get(message.author.id)):  # For each character in the word
					if char in self.guessed.get(message.author.id):  # If the character has been previouly guessed it will display it
						self.hidden_word[message.author.id] += char  # Adds the character
					elif char == " ":  # If a space
						self.hidden_word[message.author.id] += " "  # Leave as space
					elif char != " ":  # If not a space
						self.hidden_word[message.author.id] += "\*"  # Hide character
					else:  # Any other unknown circumstance
						continue  # Continue loop
				if self.hidden_word.get(message.author.id) == self.word.get(message.author.id):
					self.game_end(message.author.id)
					return await message.author.send("You win!")  # Sends the win condition message
			else:  # If the guess is wrong and/or invalid
				self.guessed[message.author.id].append(attempt)  # Add to guessed list
				self.guesses[message.author.id] -= 1  # Removes a guess attmept as the guess was incorrect 
				if self.guesses.get(message.author.id) == 0:  # The user has run out of guesses
					await message.author.send(f"The word was *{self.word.get(message.author.id)}*. Game over! You lost!")  # Sends game over message
					self.game_end(message.author.id)  # Ends game
					self.game_end(message.author.id)  # Ends game

			await self.message[message.author.id].delete()  # Deletes initial embed
			self.message.pop(message.author.id)  # Clears dict value for embed

			embed = discord.Embed(color=discord.Color(65408))  # Creates inital embed with coloured sidebar
			embed.description = f"Word: {self.hidden_word.get(message.author.id)}"  # Adds description
			embed.add_field(name="Guesses", value=self.guesses.get(message.author.id), inline=False)  # Adds a filed
			embed.add_field(name="Guessed", value=self.guessed.get(message.author.id), inline=False)  # Adds a filed
			self.message[message.author.id] = await message.author.send(embed=embed)  # Sends and assigns the embed

		elif message.content.lower().startswith("hint"):
			if self.current_hint[message.author.id] > 3:
				return await message.author.send("No more hints available")
			try:
				await message.author.send(self.hints.get(message.author.id)[self.current_hint.get(message.author.id)])
				self.current_hint[message.author.id] += 1
				return
			except IndexError:
				return await message.author.send("No hints available")
		else:
			return
def setup(bot):  # Defines setup for command class
	bot.add_cog(Hangman(bot))  # Adds the class to become a command class/cog