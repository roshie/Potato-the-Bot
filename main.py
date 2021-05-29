import os
import discord 
from keep_alive import keep_alive
from cowin import get_slots_availability
from search import google_search
from discord.ext import commands
import asyncio

prefix = "pt "

activity = discord.Activity(type=discord.ActivityType.watching, name="Cowin")

bot = commands.Bot(command_prefix=prefix, description="Hey Potato! I'm Potato", activity=activity, status=discord.Status.idle)

def formatResponse(available_slots, dose):
    msg = "\n**There are "+ str(len(available_slots)) + " Center(s) available at pincode " + str(available_slots[0]["center_pincode"]) + " For Dosage "+ str(dose) +"**\n" 
    for centre in available_slots:
      slot = '\n'
      slot += '\n**Center Id**     ' + str(centre["center_id"])
      slot += '\n**Center Name**   ' + centre["center_name"]
      slot += '\n**Address**       ' + centre["center_address"]
      slot += '\n**Fee**           ' + centre["fee"]

      for session in centre["session"]:
        slot += '\n```css\nDATE      : ' + session["date"]  
        slot += '\n' + 'VACCINE   : ' + session["vaccine"]
        slot += '\n' + 'AVAILABLE : ' + str(session["available"])+ '```'
      msg += slot
    return msg
class ErrorHandler(commands.CommandError):
   def __init__(self, text):
       self.text = text
   
   def __str__(self): #used to get string of error
      return self.text

@bot.event
async def on_ready():
    print("Everything's all ready to go~")


@bot.event
async def on_message(message):
  if message.author != bot.user:
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
    \n ◻ pt cowin <age> <pincode> <dose>\
    \n ◻ pt google \"<search-term>\""
  embed = discord.Embed(title= "Hey Potato! I'm Potato", description=msg, color=0xFFFFF)
  await ctx.send(embed=embed)

@bot.command()
async def cowin(ctx, age:str, pincode:str, dose:str):
  if dose is None: #missing argument
      raise ErrorHandler("A parameter is missing (dose).\n The command is pt cowin <age> <pincode> <dose>")
  else:
      title = "Potato says: "
      msg = "\n"+ctx.message.author.mention
      available_slots = get_slots_availability(age, pincode, dose)
      if available_slots == "wrong-args":
        msg += "\nThe Arguments provided were wrong"
      elif available_slots == "no-response":
        msg += "\nThere was a problem with Cowin. Please Try again later"
      elif available_slots == "no-slots":
        msg += "\nThere are no slots :("
      elif available_slots[0] == "exception":
        msg = available_slots[1]
      else:
        title = "Slot Available Centres"
        msg += formatResponse(available_slots, dose)
          
      embed = discord.Embed(title=title, description=msg, color=0x2AA198)
      await ctx.send(embed=embed)
  
@bot.command()
async def google(ctx, search:str):
  '''
  pt google <search-term>
  '''
  counter = 0
  title = "Potato Says.."
  msg = "\n"+ctx.message.author.mention+"\n"
  search_result = google_search(search)
  print(search_result)
  if search_result == "failed":
    msg += "\nSearch Failed :("
  else:
    title = "Here are the results.."
    for result in search_result["items"]:
      search = '\n'
      search += '\n**'+result["title"]+'**'
      search += '\n*'+result["link"]+'*'
      search += '\n```'+result["snippet"].replace('\n','')+'```'
      msg += search
      if counter == 5:
        break
      counter +=1
      
    
      
  embed = discord.Embed(title=title, description=msg, color=0x2AA198)
  await ctx.send(embed=embed) 


@bot.command()
async def ping(ctx):
    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(latency)


async def on_command_error(ctx, error): #error handler
  if isinstance(error, ErrorHandler):
      embed = discord.Embed(title="Potato Says..", description=error, color=0xFF0000)
      await ctx.send(embed=embed) 


class Notify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task = ""
        self.author = ""
    async def looper(self, author, channel, age, pincode, dose):
        await bot.wait_until_ready()
        channel = bot.get_channel(channel)
        msg = "\n"+author.mention+"\n"
        title = "Potato says: "

        while True:
            available_slots = get_slots_availability(age, pincode, dose)
            if available_slots == "wrong-args":
              msg += "The Arguments provided were wrong"
              break
            elif available_slots == "no-response" or available_slots == "no-slots":
              msg += ""
            elif available_slots[0] == "exception":
              msg += available_slots[1]
              break
            else: 
              title = "Slot Available Centres"
              msg += formatResponse(available_slots, dose)
              break
            await asyncio.sleep(120)
        embed = discord.Embed(title=title, description=msg, color=0x2AA198)
        await channel.send(embed=embed) 
        self.task.cancel()
        self.task = ""
        
    @commands.command()
    async def cowin_start(self, ctx, age:str, pincode:str, dose:str):
        """pt cowin_start <age> <pincode> <dose> \nStarts Loop. Notifies when a slot is available"""
        msg = ''
        if not self.task:
            self.task = self.bot.loop.create_task(self.looper(ctx.message.author, ctx.message.channel.id, age, pincode, dose))
            msg = 'The Request loop has started!'
            self.author = ctx.message.author
        else:
            msg = 'A loop has already initiated by '+self.author.mention+' and it is running\
            \n Stop the loop by using pt cowin_stop'
        embed = discord.Embed(title="Potato says..", description=msg, color=0x2AA198)
        await ctx.send(embed=embed) 

    @commands.command()
    async def cowin_stop(self, ctx):
        """pt cowin_stop \nStops a loop"""
        self.task.cancel()
        self.task = ""
        embed = discord.Embed(title="Potato says..", description="The loop is stopped", color=0x2AA198)
        await ctx.send(embed=embed) 


bot.add_cog(Notify(bot))
keep_alive()
bot.run(os.getenv('TOKEN'))  # Where 'TOKEN' is your bot token
