import configparser
import discord
from discord.ext import commands

config = configparser.ConfigParser()
config.read('config.ini')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(config['DEFAULT']['Token'])