import discord
import asyncio
from discord.ext import tasks
from discord.ext import commands
from pdf_handler import *
from json_handler import *
from LED import *

class TaskHandler(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._tasks = {}
    

  async def static_loop(self, json_dict, serverID):
    channelID = json_dict[serverID]["channelID"]
    channel = self.bot.get_channel(channelID)

    for i in range(0, json_dict[serverID]["PgPerLoop"]):
      
      if len(json_dict[serverID]["BookQueue"]) == 0:
        static_loop.cancel()
        break
        
      curPageNo = get_page_no(json_dict, serverID)
      curPageLink = get_page(json_dict, serverID)
      curPage = pdf_to_img(curPageLink, curPageNo)
      PageTotal = get_page_total(json_dict, serverID)
      
      await channel.send(file=discord.File(curPage, 'image.png'))
    
      if curPageNo == PageTotal - 1:
        del_cur_book(json_dict, serverID)
      else:
        next_page(json_dict, serverID)

  
  def task_launcher(self, json_dict, serverID, **interval): 
    """Creates new instances of `tasks.Loop`"""
    # Creating the task
    new_task = tasks.loop(**interval)(self.static_loop)
    self._tasks[serverID] = new_task
    # Starting the task
    self._tasks[serverID].start(json_dict, serverID)
    

  @commands.command()
  async def start_task(self, json_dict, serverID):
    """Command that launches a new task with the arguments given"""
    interval = get_interval(json_dict, serverID)
    self.task_launcher(json_dict, serverID, seconds=interval)
    
    channelID = json_dict[serverID]["channelID"]
    channel = self.bot.get_channel(channelID)
    await channel.send('Task started!')

  @commands.command()
  async def cancel_task(self, json_dict, serverID):
    self._tasks[serverID].cancel()
    del self._tasks[serverID]
    
    channelID = json_dict[serverID]["channelID"]
    channel = self.bot.get_channel(channelID)
    await channel.send('')

  @commands.Cog.listener()
  async def on_ready(self):
    print('We have logged in as {0.user}'.format(self.bot))
    await bot_ready()
  
  
  @commands.Cog.listener()
  async def on_message(self, message):
    json_dict = read_file('./data.json')
    serverID = str(message.guild.id)
    channelID = message.channel.id
    
    
    if message.author == self.bot.user:
      return

    
    if self.bot.user.mentioned_in(message):
      #turn on light for fun lol
      print("Let there be light")
      await asyncio.gather(bot_called(), message.channel.send('You mentioned me!'))

    
    if message.content.startswith('$hello'):
      # Say hi lol
      await message.channel.send('Hello!')

    
    if message.content.startswith('$start'):
      # Start the task.loop
      await message.channel.send('Start')
      await self.start_task(json_dict, serverID)

    
    if message.content.startswith('$pause'):
      # Pause the task.loop
      await message.channel.send('Pause')
      await self.cancel_task(json_dict, serverID)
  
    
    if message.content.startswith('$list'):
      # Get Current Reading List
      book_data = get_book_list(json_dict, serverID)
      await message.channel.send(book_data)
    
  
    if message.content.startswith('$next'):
      # Get Rid of Current Book
      if not len(json_dict[serverID]["BookQueue"]) < 2: # List is not empty
        del_cur_book(json_dict, serverID)
      else:
        await message.channel.send('There is no next.')
  
    
    if message.content.startswith('$here'):
      # Set Target Channel Directory
      if serverID in json_dict.keys():
        set_channel(json_dict, serverID, channelID)
      else:
        add_new_server(json_dict, serverID, channelID)

      await message.channel.send('Updated New Target Channel.')
  
    
    if message.content.startswith('$interval'):
      # Set task.loop frequency
      message_content = message.content.split(' ')
      if len(message_content) == 2:
        print(message_content)
        if message_content[1].isdecimal():
          set_interval(json_dict, serverID, int(message_content[1]))

          await message.channel.send('Changed Page Frequency/Interval')
        else:
          await message.channel.send('Enter a number')
      else:
        await message.channel.send('Enter with the following format: "$interval (Number)"')

    
    if message.content.startswith('$pagePerInt'):
      # Set Amount of Pages Per task.loop
      message_content = message.content.split(' ')
      if len(message_content) == 2:
        if message_content[1].isdecimal():
          set_per_loop(json_dict, serverID, int(message_content[1]))

          await message.channel.send('Changed Amout of Pages per Interval')
        else:
          await message.channel.send('Enter a number')
      else:
        await message.channel.send('Enter with the following format: "$pagePerInt (Number)"')

    
    if message.content.startswith('$current'):
      # Get Page Info
      title, author, curPage = get_page_info(json_dict, serverID)

      if author != "":
        await message.channel.send('We are currently on Page {} of {}\'s {}.'.format(curPage, author, title))
      else:
        await message.channel.send('We are currently on Page {} of {}.'.format(curPage, title))
      

    
    if message.content.startswith('$book'):
      # Add attached PDF into DB
      if len(message.attachments) > 0:
        if serverID in json_dict.keys():
          for attachment in message.attachments:
            print(attachment.content_type)
            if attachment.content_type == 'application/pdf':
              await message.channel.send('Got PDF.')
              
              url_to_pdf = attachment.url
              title = attachment.filename
              page_count = get_page_count(url_to_pdf)
              print(attachment.url)
              add_book(json_dict, url_to_pdf, serverID, page_count, title)
            else:
              await message.channel.send('Please Upload a PDF.')
        else:
          await message.channel.send('No Target Channel Specified. Use \'$here\' to specify a channel to target.')
      else:
        await message.channel.send("No File was Attached.")

async def setup(bot):
  await bot.add_cog(TaskHandler(bot))

