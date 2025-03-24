import discord
import re
from discord.ext import commands
import requests
import os
# Bot setup
intents = discord.Intents.default()
# intents.message_content = True  # Enable message content intent
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
    pattern = r"^-> post: \| (.+) \| (.+)$"
    match = re.match(pattern, message.content.strip())
    if match:
        title = match.group(1)
        content = match.group(2)
        display_name = message.author.display_name
        
        print(title, content, display_name)
        
        location = "https://apps.ginastic.co/200/q&aapp/"
        params = {
            "title": title,
            "question": content,
            "sender": display_name
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response_type = requests.head(location, headers=headers)
            
        response = requests.get(location, headers=headers, params=params)
        
        sendmsg = ""
        
        if response.text == "success":
            sendmsg = "Your question has been posted successfully as a discord user. Check Q&A App for answer."
            
        elif response.text == "incorrectinput":
            sendmsg = "Your question was not posted, due to exceeded word limit (title: 50, question: 1000)"
            
        elif response.text == "notset":
            sendmsg = "Your question was not posted, due to missing parameters."   
        
        
        print(sendmsg, response.text)
        # # Send the formatted message
        
        await message.channel.send(sendmsg)
    else:
        await message.channel.send("Incorrect format")
    # Process commands normally
    await bot.process_commands(message)
# Run bot
bot.run(os.getenv("SECRET"))  # Replace with your bot token
  
