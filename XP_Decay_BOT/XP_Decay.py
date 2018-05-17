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

key_file = open('./key.txt', 'r')
if not key_file:
    print('File key.txt can\'t be found')
    sys.exit(0)

api_key = key_file.read().splitlines()[0]
if not api_key:
    print('No API key in discord_key.txt')
    sys.exit(0)

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
    server = client.get_server('380248307848577035')
    if message.content.startswith('*test'):
        server_members = server.members                     #? List of Members ON SERVER                            
        for member in server_members:
            if member.bot == False:
                mem_roles = server.get_member(member.id).roles
                for role in mem_roles:
                    if role.name == 'Master' or role.name == 'Platinum' or role.name == 'Diamond' or role.name == 'Gold':
                        print(member,role)
            else:
                pass
        await client.send_message(message.channel, 'Info printed to terminal')

    elif message.content.startswith('*embed'):
        nadeko = server.get_member('116275390695079945')
        async for message in client.logs_from(message.channel):
            if user.member.id == '116275390695079945'


client.run(str(api_key))