import discord
import os
import requests 


client = discord.Client()

@client.event
async def on_ready():
  print('Im Online! as {0.user}'.format(client))
  message.channel.send(" ``` Hey Potato! I'm a Potato\n Thanks for adding me into your server ```")

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('pt'):
    await message.channel.send('Hello!')
  if message.content.startswith('pt cowin'):
    await message.channel.send('cowin')

client.run(os.getenv('TOKEN'))