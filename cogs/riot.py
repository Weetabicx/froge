from discord.ext import commands
from discord import Embed, Color, File
import json
import aiohttp
import numpy
import matplotlib.pyplot as pyplot
import os

class riot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.get_riot_api()

	def get_riot_api(self):
		with open('config.json', 'r') as config:
			config = json.load(config)
			self.api_key = config['riot-key']

	def sorting(self, champ:list, points:list, mastery:list):

		highest = points[0]
		highest_pos = 0

		middle = points[0]
		middle_pos = 0

		lowest = points[0]
		lowest_pos = 0

		for index, point in enumerate(points):
			# Orders the parallel arrays based in decending order of points
			# As there are only three rows of values, we can find the highest, lowest adnd the value that is inbetween these is the middle
			if highest < point:
				highest = points[index]
				highest_pos = index
			if lowest > point:
				lowest = points[index]
				lowest_pos = index
			if point < max(points) and point > min(points):
				middle = points[index]
				middle_pos = index

		new_champ = [champ[highest_pos], champ[middle_pos], champ[lowest_pos]]
		new_points = [points[highest_pos], points[middle_pos], points[lowest_pos]]
		new_mastery = [mastery[highest_pos], mastery[middle_pos], mastery[lowest_pos]]
		return(new_champ, new_points, new_mastery)



	@commands.command()
	async def mastery(self, ctx, ign: str):

		embed = Embed(color=Color(65408))

		async with aiohttp.ClientSession() as sesh:
			async with sesh.get(f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ign}', params={'api_key': self.api_key}) as response:
				user = await response.json()
				summonerID = user['id']
				encryptedID = user['puuid']
				summonerLevel = user['summonerLevel']
				
		async with aiohttp.ClientSession() as sesh:
			async with sesh.get(f'https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerID}', params={'api_key': self.api_key}) as response:
				top_champs = await response.json()
				top_champs = top_champs[:3]

				top_champs_ids = []
				top_champs_mastery = []
				top_champs_level = []
				top_champ_names = [1,2,3]
				names_indexing = []

				for champ in top_champs:
					top_champs_ids.append(champ['championId'])
					top_champs_mastery.append(champ['championPoints'])
					top_champs_level.append(champ['championLevel'])

				top_champs_ids, top_champs_mastery, top_champs_level		
				top_champs_ids, top_champs_mastery, top_champs_level = self.sorting(top_champs_ids, top_champs_mastery, top_champs_level)	

		async with aiohttp.ClientSession() as sesh:
			async with sesh.get(f'https://ddragon.leagueoflegends.com/cdn/11.1.1/data/en_US/champion.json') as response:
				champions = await response.json()
				champions = champions['data']
				top_champs_ids, top_champs_mastery, top_champs_level = self.sorting(top_champs_ids, top_champs_mastery, top_champs_level)

				for champ in champions:
					for index, _id in enumerate(top_champs_ids):
						if int(champions[champ]['key']) == _id:
							top_champ_names[index] = champ
							names_indexing.append(index)


		for x in range(3):
			embed.add_field(name=f'#{x+1}-{top_champ_names[x]}', value=f'Mastery Points: {top_champs_mastery[x]}, Mastery Level: {top_champs_level[x]}')

		await ctx.send(embed=embed)


	@commands.command()
	async def rank(self, ctx, ign: str):
		async with aiohttp.ClientSession() as sesh:
			async with sesh.get(f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ign}', params={'api_key': self.api_key}) as response:
				user = await response.json()
				summonerID = user['id']
				encryptedID = user['puuid']

		async with aiohttp.ClientSession() as sesh:
			async with sesh.get(f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerID}', params={'api_key': self.api_key}) as response:
				data = await response.json()
				tier = data[0]['tier']
				rank = data[0]['rank']
				wins = data[0]['wins']
				losses = data[0]['losses']
				lp = data[0]['leaguePoints']
				wr = round((wins/(losses+wins)), 3) * 100

		embed = Embed(color=Color(65408))
		embed.title = f'Ranked season for {ign}'
		embed.description = f'Solo Queue: {tier} {rank} {lp}LP'
		embed.add_field(name='wins', value=wins, inline=True)
		embed.add_field(name='losses', value=losses, inline=True)
		embed.add_field(name="Winrate", value=wr, inline=True)
		await ctx.send(embed=embed)

	@commands.command()
	async def chart(self, ctx, ign: str):
		async with aiohttp.ClientSession() as sesh:
			async with sesh.get(f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{ign}', params={'api_key': self.api_key}) as response:
				user = await response.json()
				summonerID = user['id']
				encryptedID = user['puuid']

		async with aiohttp.ClientSession() as sesh:
			async with sesh.get(f'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerID}', params={'api_key': self.api_key}) as response:
				data = await response.json()
				wins = data[0]['wins']
				losses = data[0]['losses']

		labels = numpy.array(['wins', 'losses'])
		sizes = numpy.array([wins, losses])
		colors = numpy.array(['green', 'red'])
		pyplot.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', shadow=True, startangle=0)
		pyplot.axis('equal')
		pyplot.savefig(f'chart_{ctx.guild.id}_{ctx.author.id}.png', transparent=True, facecolor='pink', bbox_inches="tight")

		file = File(f'chart_{ctx.guild.id}_{ctx.author.id}.png')
		embed = Embed(color=Color(65408))
		embed.set_image(url=f'attachment://chart_{ctx.guild.id}_{ctx.author.id}.png')
		await ctx.send(file=file, embed=embed)
		os.remove(f'chart_{ctx.guild.id}_{ctx.author.id}.png')

def setup(bot):
	bot.add_cog(riot(bot))