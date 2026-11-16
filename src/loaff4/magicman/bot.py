import discord
from discord.ext import commands


from dotenv import load_dotenv
import os

from data import Data
import aiosqlite

class MagicManBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(command_prefix="!", intents=intents)
        

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded extension: {filename}")
        await Data.setup_tables()
        await Data.register_user(1173674023662657579)

    


bot = MagicManBot()

@bot.command()
async def join_voice(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def play(ctx):
    current_call = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if current_call == None:
        await ctx.send("I am not in a call right now")
        return
    audio_source = discord.FFmpegPCMAudio("C:/Users/Cole/Documents/MagicManPy/src/loaff4/magicman/Audio/music.mp3")
    current_call.play(audio_source)
    await ctx.send(f"Playing {audio_source}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


load_dotenv()

TOKEN = os.getenv("TOKEN")

bot.run(TOKEN) 