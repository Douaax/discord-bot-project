import os
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

    if content_lower.startswith('!trivia'):
        await send_trivia(message)

    await bot.process_commands(message)

async def send_quotes(channel):
    while send_quotes_flag:
        quote = get_random_quote("C:/Users/HP/Desktop/discord bot quotes/quotes.txt")
        msg = await channel.send(quote)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(10)

def get_random_quote(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        quotes = file.readlines()
        return random.choice(quotes).strip()

async def get_quote(channel):
    quote = get_random_quote("C:/Users/HP/Desktop/discord bot quotes/quotes.txt")
    await channel.send(quote)

async def send_trivia(message):
    special_quote = get_random_special_quote("C:/Users/HP/Desktop/discord bot quotes/algerianProverbs.txt")

    missing_word, masked_quote, choices = mask_quote(special_quote)
    await message.channel.send(f"Guess the missing word in the quote:\n\n{masked_quote}\n\nChoices: {', '.join(choices)}")

    def check(msg):
        return msg.author != bot.user and msg.channel == message.channel

    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await message.channel.send('Sorry, time is up!')
        return

    if msg.content.lower() == missing_word:
        await message.channel.send(f"Ya3tik sa7a! Correct! The missing word was '{missing_word}'. You earned 10 points!\nFull quote: {special_quote}")
    else:
        await message.channel.send(f"M3lich! Better luck next time.\nFull quote: {special_quote}")

    # Ask if the user wants to continue or stop
    await message.channel.send("Do you want to continue playing trivia? (yes/no)")

    def check_continue(msg):
        return msg.author == message.author and msg.channel == message.channel and msg.content.lower() in ['yes', 'no']

    try:
        response = await bot.wait_for('message', timeout=60.0, check=check_continue)
        if response.content.lower() == 'yes':
            await send_trivia(message)  # Continue playing trivia
        else:
            await message.channel.send("Okay, stopping trivia game.")
    except asyncio.TimeoutError:
        await message.channel.send("Sorry, you took too long to respond. Stopping trivia game.")

def get_random_special_quote(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        quotes = file.readlines()
        return random.choice(quotes).strip()

def mask_quote(quote):
    words = quote.split()
    missing_word = random.choice(words)
    masked_quote = ' '.join(['[** **]' if word == missing_word else word for word in words])

    # Generate three choices including the correct word
    choices = random.sample(words, 3)
    if missing_word not in choices:
        choices[random.randint(0, 2)] = missing_word

    return missing_word, masked_quote, choices

@bot.command()
async def stop(ctx):
    global send_quotes_flag
    send_quotes_flag = False
    await ctx.send("Quotes stopped.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I don't recognize that command.")

# Retrieve the bot token from the environment variable
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if BOT_TOKEN is None:
    print("Error: Discord bot token not found in environment variable DISCORD_BOT_TOKEN.")
    exit(1)

bot.run(BOT_TOKEN)