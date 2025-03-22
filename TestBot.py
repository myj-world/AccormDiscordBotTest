import discord
import re
import requests
from discord.ext import commands

# Bot setup
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix="->", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Prevent bot from responding to itself
    if message.author == bot.user:
        return

    # Regular expression pattern to match: -> post: | title | content
    pattern = r"^-> post: \| (.*?) \| (.*?)$"
    match = re.match(pattern, message.content.strip())

    if match:
        title = match.group(1)
        content = match.group(2)
        display_name = message.author.display_name

        location = "https://apps.ginastic.co/200/q&aapp/"
        params = {
            "title": title,
            "question": content,
            "sender": display_name
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # Make request to post the question
        requests.head(location, headers=headers)  # Not used, consider removing if unnecessary
        response = requests.get(location, headers=headers, params=params)

        if response.text == "success":
            sendmsg = ("Your question has been posted successfully as a Discord user. "
                       "Check [Q&A App](https://apps.ginastic.co/apps/q&a) for an answer.")
        elif response.text == "incorrectinput":
            sendmsg = ("Your question was not posted due to exceeding the word limit "
                       "(title: 50, question: 1000).")
        elif response.text == "notset":
            sendmsg = "Your question was not posted due to missing parameters."
        else:
            sendmsg = "An error occurred while posting your question."

        # Send the formatted message
        await message.channel.send(sendmsg)
    else:
        await message.channel.send("Incorrect format")

    # Process commands normally
    await bot.process_commands(message)

# Run bot
bot.run("MTM0NzM2NzQ4OTg3NjY2MDI0NA.G9E8CW.2m7WAKP1TRcjhIXR0mKUCDci7KbMOUOQLMTF6c")  # Replace with your bot token
