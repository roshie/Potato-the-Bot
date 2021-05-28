import discord
import os
import requests 
from keep_alive import keep_alive
from discord.ext import commands
from cowin import get_slots_availability

bot = commands.Bot(command_prefix='pt')


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
    await message.channel.send('> Hello!')
  if message.content.startswith('pt cowin'):
    await message.channel.send('> This Feature is building up! stay tuned!')


@bot.command()
async def cowin(ctx, cmd, age, pincode, dose):
  if cmd == "cowin":
    title = "Potato says: "
    msg = ''
    available_slots = get_slots_availability(age, pincode, dose)
    if available_slots == "wrong-args":
      msg = "\nThe Arguments provided were wrong"
    elif available_slots == "no-response":
      msg = "\nThere was a problem with Cowin. Please Try again later"
    elif available_slots == "no-slots":
      msg = "\nThere are no slots :("
    else:
      title = "Slot Available Centres"
      msg = "\n**There are "+ str(len(available_slots)) + " Centers available at pincode " + available_slots[0]["center_pincode"] + " For Dosage "+ dose +"**\n" 
      for centre in available_slots:
        slot = '\n'
        slot += '\n**Center Id**     ' + centre["center_id"]
        slot += '\n**Center Name**   ' + centre["center_name"]
        slot += '\n**Address**       ' + centre["center_address"]
        slot += '\n**Fee**           ' + centre["fee"]

        for session in available_slots["session"]:
          slot += '\n ``` DATE      : ' + session["date"]  
          slot += '\n' + 'VACCINE   : ' + session["vaccine"]
          slot += '\n' + 'AVAILABLE : ' + session["available"]+ '```'
        msg += slot
        
    embed = discord.Embed(title=title, description=msg, color=0xFFFFF)
    await ctx.send(embed=embed)


bot.add_command(cowin)

keep_alive()
client.run(os.getenv('TOKEN'))