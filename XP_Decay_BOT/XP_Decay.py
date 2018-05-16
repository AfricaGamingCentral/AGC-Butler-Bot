# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import discord.utils
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import sys

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="XP Bot", command_prefix="*", pm_help=False)

# open private key file
key_file = open('./key.txt', 'r')
if not key_file:
    print('File key.txt can\'t be found')
    sys.exit(0)

# read private key from file
api_key = key_file.read().splitlines()[0]
if not api_key:
    print('No API key in discord_key.txt')
    sys.exit(0)

# close private key file
key_file.close()


@client.event
async def on_ready():
    await client.wait_until_ready()
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to ' +
          str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(
        discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('You are running XP -bot v0.1-')
    print('Created by - bot steev -#0666')
    
    return await client.change_presence(game=discord.Game(name='Dont be afk for too long :smirk:'))

    

@client.event
async def on_message(message):
    await client.wait_until_ready()
    if message.content.startswith('*test'):
        server = client.get_server('380248307848577035')
        server_roles = server.roles
        server_members = server.members
        for role in server_roles:
            print (role)
        else:
            pass
        for member in server_members:
            if member.bot == False & "Gold" in member.roles == True:
                    print(member)
            else:
                pass
        await client.send_message(message.channel, 'Info printed to terminal')
    
    elif message.content.startswith('*msgcount'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=500):
            if log.author == message.author:
                counter += 1
        
        await client.edit_message (tmp, 'You have {} messages.'.format(counter))
client.run(str(api_key))