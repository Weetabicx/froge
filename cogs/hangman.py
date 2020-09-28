# Imports libraries
from discord.ext import commands as com
import discord as d
import json
import random


class Hangman(com.Cog):  # Creates a class with inheritance
	def __init__(self, bot):  # Defines initalise
		"""Defines variables to be used in further functions/commands"""
		self.bot = bot

		self.guild_hangman_running = {}
		self.guild_hangman_word = {}
		self.guild_used_letters = {}
		self.guild_guesses = {}
		self.guild_message = {}

		self.user_hangman_running = {}
		self.user_hangman_word = {}
		self.user_used_letters = {}
		self.user_guesses = {}
		self.user_message = {}

	@com.command()  # Creates a command object
	async def hangman(self, ctx, category: str):  # Defines function to become a command

		with open("hangman.json", "r") as hangman_words:  # Opens a file in read mode
			category_words = json.load(hangman_words)[category]  # Get's list of words in category
			word = random.choice(list(category_words.items()))  # Picks a random word pair in the dict

		display_text = len(word[0]) * '-'  # For the length of the word replace with dashes

		if ctx.guild is not None:  # If command is used in a guild
			self.guild_hangman_running[ctx.guild.id] = True  # A hangman game is runing
			self.guild_hangman_word[ctx.guild.id] = str(word[0])  # Stores word in memory
			self.guild_guesses[ctx.guild.id] = 3  # Set's the number of guesses

			hangman_embed = d.Embed(colour=d.Color(65408))  # Creates the embed with a colour
			hangman_embed.title = "Hangman"
			hangman_embed.add_field(name="Word", value=display_text, inline=False)  # Hidden word
			hangman_embed.add_field(name="Stated Letters", value="-", inline=False)  # Add's field to record guessd letter
			hangman_embed.add_field(name="Guesses remaining: {}".format(3))  # Record the number of guesses
			self.guild_message[ctx.guild.id] = await ctx.send(embed=hangman_embed)  # Sends embed

	@com.Cog.listener('on_message')  # Creates a on message event listener
	async def word_checker(self, message):  # Defines function to run on each message
		if message.guild is None:  # If there is not guild
			return  # Stop the function
		else:  # If there is a guild
			if self.guild_hangman_running.get(message.guild.id):  # If a game is running
				if message.content.lower().startswith("guess "):  # If the message startswither "guess"
					guess = message.content.split(" ")
					guess = guess[1]

					if guess in self.guild_hangman_word.get(message.guild.id):
						new_display_text = ""

						for letter in range(len(self.guild_hangman_word.get(message.guild.id))):
							if letter != "-":
								new_display_text = new_display_text + letter
								continue
							if guess == letter:
								new_display_text = new_display_text + letter
								continue
							elif guess != letter:
								new_display_text = new_display_text + "-"
								continue



				else:  # If the message is not related to the game
					return  # Stops the function
			else:  # If a game isn't running
				return  # Stops the function


def setup(bot):  # Defines setup
	bot.add_cog(Hangman(bot))  # The class to be added as a cog
