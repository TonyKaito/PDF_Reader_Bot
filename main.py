import os
import discord
from discord.ext import tasks
from pdf_handler import *
from json_handler import *

# with open('data.json', 'r') as x:
#   # Reading from json file
#   y = json.load(x)

# intent = discord.intents.Default()
# intent.members = True

n=60

client = discord.Client(intents=discord.Intents.all())

@tasks.loop(minutes=n)
async def test(json_dict, serverID):
  channelID = json_dict[serverID]["channelID"]
  channel = client.get_channel(channelID)
  
  for i in range(0, json_dict[serverID]["PgPerLoop"]):

    if len(json_dict[serverID]["BookQueue"]) == 0:
      await channel.send('Reading Queue Empty')
      test.cancel()
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

  
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  json_dict = read_file('./data.json')
  serverID = str(message.guild.id)
  channelID = message.channel.id
  
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    # Say hi lol
    await message.channel.send('Hello!')

  if message.content.startswith('$start'):
    # Start the task.loop
    await message.channel.send('Start')
    test.start(json_dict, serverID)

  if message.content.startswith('$pause'):
    # Pause the task.loop
    await message.channel.send('Pause')
    test.cancel()

  
  if message.content.startswith('$list'):
    # Get Current Reading List
    book_data = get_book_list(json_dict, serverID)
    await message.channel.send(book_data)
    pass
  

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

  # TO-DO LATER
  # if message.content.startswith('$interval'):
  #   # Set task.loop frequency
  #   pass

  if message.content.startswith('$pagePerInt'):
    # Set Amount of Pages Per task.loop
    pass

  if message.content.startswith('$current'):
    # Get Page Info
    title, author, curPage = get_page_info(json_dict, serverID)
    
    await message.channel.send('We are currently on Page {} of {}\'s {}.'.format(curPage, author, title))

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
  
    
client.run(os.environ['discord_key'])
