# Import modules
from discord.ext import commands, tasks  
import discord
from datetime import datetime
import feedparser
import re
import json

def read_last_chapter(key: str):  # Define function 
		"""Opens the file which contains the last chapter number and compares it to the latest update """
		f = open("latest.json", "r")  # Opens a file in read mode
		last_chapter = json.load(f)  # Loads file as a json
		f.close()  # Closes the last file
		last_chapter = last_chapter[key]  # Retrieves the last chapter number
		return last_chapter  # Returns the int value

class feeder(commands.Cog):  # Defines the command class with inheritance
	def __init__(self, bot):  # Initialise the class | Runs on class call
		self.bot = bot  # Assigns the bot var to the wider class level scope
		self.sololevelingRSS.start()  # Starts the loop on initialise 

	@tasks.loop(seconds=180)  # A loop that will run every 60 seconds
	async def sololevelingRSS(self):  # Define function to run every 60 seconds

		if datetime.now().strftime("%a") == "Sat":  # If the day is Wednesday

			feed = feedparser.parse("https://mangadex.org/rss/d7UC82PWhmxqfktNsVcTzFpvD53ygXuE/manga_id/31477?h=0")  # Opens RSS feed for Solo Leveling
			try:
				chapter = feed["entries"][1]  # Get's the latest chapter
			except IndexError:
				print("Website issues.") 
				return

			match = re.search(r"(?i)(chapter \d+)", chapter.title, re.IGNORECASE)  # Use REGEX to break up chapter title
			chapter_number = int(match.group().split(" ")[1])  # Specified number from broken down chapter title

			last_chapter = read_last_chapter("sololeveling")  # Runs function to get latest chapter number

			if chapter_number < last_chapter or chapter_number == last_chapter:  # If the chapter is an already uploaded chapter
				return  # Stop function
				
			if last_chapter < chapter_number:  # If uploaded chapter is 
				with open('latest.json', 'w') as outfile:  # Opens file to overwrite
					New_data = {}  # Creates datablock
					New_data['sololeveling'] = 1 + last_chapter  # Populates data block
					json.dump(New_data, outfile, indent=4)  # Writes to file

			await self.channel.send(f"@eveyone {chapter.link}")  # Sends message to user

	@sololevelingRSS.before_loop  # Runs the defined function before the loop starts
	async def before_sololevelingRSS(self):  # Defines function to run
		await self.bot.wait_until_ready()  # Waits until bot is ready
		self.channel = await self.bot.fetch_channel(800036058615906356)  # Fetches user object

		
def setup(bot): 
	bot.add_cog(feeder(bot))

