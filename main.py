import os
import discord 
from keep_alive import keep_alive
from cowin import get_slots_availability
from discord.ext import commands

prefix = "pt "

activity = discord.Activity(type=discord.ActivityType.watching, name="Cowin")

bot = commands.Bot(command_prefix=prefix, description="Hey Potato! I'm Potato", activity=activity, status=discord.Status.idle)


@bot.event
async def on_ready():
    print("Everything's all ready to go~")


@bot.event
async def on_message(message):
    print("The message's content was", message.content)
    await bot.process_commands(message)


@bot.command()
async def hello(ctx):
  await ctx.send("> Hello!")

@bot.command()
async def about(ctx):
  msg = "\n*Thanks for adding me into your server* \n My commands\
    \n ◻ pt hello - I would say hello back to you\
    \n ◻ pt ping - Latency of the bot\
    \n ◻ pt cowin <age> <pincode> <dose> - This feature is building up. Stay tuned!"
  embed = discord.Embed(title= "Hey Potato! I'm Potato", description=msg, color=0xFFFFF)
  await ctx.send(embed=embed)

@bot.command()
async def cowin(ctx, age:str, pincode:str, dose:str):
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
    msg = "\n**There are "+ str(len(available_slots)) + " Centers available at pincode " + str(available_slots[0]["center_pincode"]) + " For Dosage "+ str(dose) +"**\n" 
    for centre in available_slots:
      slot = '\n'
      slot += '\n**Center Id**     ' + str(centre["center_id"])
      slot += '\n**Center Name**   ' + centre["center_name"]
      slot += '\n**Address**       ' + centre["center_address"]
      slot += '\n**Fee**           ' + centre["fee"]

      for session in centre["session"]:
        slot += '\n ``` DATE      : ' + session["date"]  
        slot += '\n' + 'VACCINE   : ' + session["vaccine"]
        slot += '\n' + 'AVAILABLE : ' + str(session["available"])+ '```'
      msg += slot
      
  embed = discord.Embed(title=title, description=msg, color=0xFFFFF)
  await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(ctx.message.author, "> "+str(latency))


keep_alive()
bot.run(os.getenv('TOKEN'))  # Where 'TOKEN' is your bot token