import configparser
import discord
import csv
import requests
from discord.ext import commands


config = configparser.ConfigParser()
config.read('config.ini')

intents = discord.Intents.default()  # Create a new Intents object with default settings
intents.messages = True  # Ensure the bot listens to messages
intents.message_content = True  # This line declares the "Message Content" intent

bot = commands.Bot(command_prefix='!', intents=intents)  # Pass the Intents object to the Bot constructor

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command()
async def ping(ctx):
    print("Ping command received!")  # Print a message whenever the ping command is triggered
    await ctx.send('Pong!')

@bot.command()
async def price(ctx, *, item):
    item_id = get_item_id(item, 'data.csv')
    api_url = f"https://prices.runescape.wiki/api/v1/osrs/latest?id={item_id}"
    headers = {
        'User-Agent': 'Price_checker_dicord_bot - @Xaphins#4508'
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data["data"])
        item_price = data["data"][item_id]["high"]
        await ctx.send(f"The current price of {item.capitalize()} is {item_price} gp.")
    else:
        await ctx.send("Sorry, an error occurred while fetching the item price.")

def get_item_id(item_name, csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'].lower() == item_name.lower():
                return row['id']
    return None

def main():
    bot.run(config['DEFAULT']['Token'])  # Read the token from the configuration file

if __name__=="__main__":
    main()