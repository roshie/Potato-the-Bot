import discord
import os
import requests 
from keep_alive import keep_alive


client = discord.Client()

@client.event
async def on_ready():
  print('Im Online! as {0.user}'.format(client))
  msg = "\n*Thanks for adding me into your server* \n My commands\
    \n ◻ pt hello - I would say hello back to you\
    \n ◻ pt cowin <age> <pincode> <dose> - This feature is building up. Stay tuned!"
  channel = client.get_channel(847721563175387187)
  embed = discord.Embed(title= "Hey Potato! I'm Potato", description=msg, color=0xFFFFF)
  await channel.send(embed=embed)

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('pt hello'):
    await message.channel.send('Hello!')
  if message.content.startswith('pt cowin'):
    await message.channel.send('This Feature is building up! stay tuned!')


keep_alive()
client.run(os.getenv('TOKEN'))