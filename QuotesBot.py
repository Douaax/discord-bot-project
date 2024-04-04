import discord
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)

send_quotes_flag = False

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    global send_quotes_flag

    if message.author == bot.user:
        return

    content_lower = message.content.lower()
    if not send_quotes_flag:
        if content_lower.startswith(('hello', 'hi', 'hey')):
            await message.channel.send('Hello there! Welcome where studying is made more fun with motivational quotes. You will receive a quote every 15 mins, or you can get one by sending !quote as well as stop them with !stop. So are you ready? (yes/no)')

            def check(msg):
                return msg.author == message.author and msg.channel == message.channel and msg.content.lower() in ['yes', 'no']

            try:
                msg = await bot.wait_for('message', timeout=300.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send('Sorry, you took too long to respond.')
                return

            if msg.content.lower() == 'yes':
                send_quotes_flag = True
                await message.channel.send('Good Luck and Have Fun!')
                await send_quotes(message.channel)
            elif msg.content.lower() == 'no':
                await message.channel.send("Alright, call me again once you are.")

    if content_lower.startswith('!quote'):
        await get_quote(message.channel)

    await bot.process_commands(message)

async def send_quotes(channel):
    while send_quotes_flag:
        quote_file_paths = [
            "C:/Users/HP/Desktop/discord bot quotes/quotes.txt",
            "C:/Users/HP/Desktop/discord bot quotes/algerianProverbs.txt"
        ]
        for file_path in quote_file_paths:
            quote = get_random_quote(file_path)
            msg = await channel.send(quote)
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
            await asyncio.sleep(10)

def get_random_quote(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        quotes = file.readlines()
        return random.choice(quotes).strip()

async def get_quote(channel):
    quote_file_paths = [
        "C:/Users/HP/Desktop/discord bot quotes/quotes.txt",
        "C:/Users/HP/Desktop/discord bot quotes/algerianProverbs.txt"
    ]
    for file_path in quote_file_paths:
        quote = get_random_quote(file_path)
        await channel.send(quote)

@bot.command()
async def stop(ctx):
    global send_quotes_flag
    send_quotes_flag = False
    await ctx.send("Quotes stopped.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I don't recognize that command.")

bot.run('MTIyMTMxMDQ0Njc0MTc1MzkzNw.GS2bZl.oAOQtlL6iFNYEywVA8-RmHhwJYTU9P0xlWnio4')
