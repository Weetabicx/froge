from discord.ext import commands as com  # Import commands
import json

froge = com.Bot(command_prefix=["%"], case_insensitive=True)  # Specifies commands prefix and case sensativity

froge.remove_command("help")  # Removes the default help commmand

# Loading each cog in a loop
cogs = ["help","feeder", "hangman", "misc", "vote", "blacklivesmatter", "presence", 'music']  # Filename of each cog
for cog in cogs:  # For each specified filename
	froge.load_extension('cogs.{}'.format(cog))  # Load the file as an extension to the bot

with open("config.json", "r") as data:  # Opens a file in read mode
	config = json.load(data)  # Loads file as a json

froge.run(config["token"])  # Runs the bot with specified token
