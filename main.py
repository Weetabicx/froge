from discord.ext import commands # Import commands
from discord import Intents
from cogs.utils.misc import ReadToken
import aiohttp, asyncio

client = commands.Bot(command_prefix=["?"], intents=Intents.all())  # Specifies commands prefix and case sensativity

# async def main():
#     async with client:
#         bot.loop.create_task(background_task())
#         await client.load_extension("cogs.blacklivesmatter")
#         await client.start(ReadToken())

# asyncio.run(main())

async def main():
    async with aiohttp.ClientSession() as session:
        async with client:
            client.session = session
            await client.start(ReadToken())
            
asyncio.run(main())