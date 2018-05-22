import discord
import discord.utils
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import sys
import sqlite3
import datetime
import os

client = Bot(description="Butler utility for AGC Server", command_prefix="*", pm_help=False)

sqlite_file = './AGC_user_db.sqlite'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

key_file = open('./key.txt', 'r')
if not key_file:
    print('File key.txt can\'t be found')
    sys.exit(0)

api_key = key_file.read().splitlines()[0]
if not api_key:
    print('No API key in discord_key.txt')
    sys.exit(0)

key_file.close()

msg_buffer = []
nadeko_lb = []

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

async def spin_db(message):
    await client.wait_until_ready()
    today = datetime.datetime.today().date().__format__("%Y-%m-%d")
    server = client.get_server('380248307848577035')
    server_members = server.members                                  
    server_member_total = 0
    c.execute('DELETE from user_info')
    async for member in server_members:
        if member.bot == False:
            c.execute('INSERT INTO user_info VALUES(?,?)',(member.id,today))
            server_member_total += 1
            print(member.id,today)
    conn.commit()
    c.execute('SELECT count("user_id") FROM user_info')
    db_count = c.fetchall()
    (user_id,) = db_count[0]
    await client.send_message(message.channel,'Database has been filled with members from Server: '+str(server)+'\nServer Member Count: '+str(server_member_total)+'\nDatabase Member Count: '+str(user_id))

#async def backup_db(message):

#async def spawn_webclient(message):
#https://discord.gg/tC4EedV

async def db_update(message,msg_buffer):
    
    await client.wait_until_ready()
    
    while not client.is_closed:
        
        await client.send_message(message.channel,msg_buffer)
        
        print('CURRENT BUFFER\n')
        de_duped_buffer = list(set(msg_buffer))
        print(de_duped_buffer)
        print('\n')
        msg_buffer.clear()
        if len(msg_buffer) == 0:
            print('Main Buffer Cleared')
        else:
            print('Failed to clear Main Buffer')
                
        for user_data in de_duped_buffer:
          
          # Message Buffer Info
           user_data = user_data.split('_')
           buffer_user_id = user_data[0]
           new_date = '2018-05-10'#user_data[1]
           
           # SQL Info
           c.execute('SELECT * FROM user_info WHERE user_id == (?)',(buffer_user_id,))
           user_entry = c.fetchall()
           
           if len(user_entry) == 0:
                c.execute('INSERT INTO user_info VALUES(?,?)',(buffer_user_id,new_date))                              
                await client.send_message(message.channel,'UserID: '+buffer_user_id+' has been inserted into the DB with the latest date of: '+ new_date)
                conn.commit()
           else:
                c.execute('UPDATE user_info SET date_time = (?) WHERE user_id == (?)',(new_date,buffer_user_id))
                await client.send_message(message.channel,'UserID: '+buffer_user_id+' has been updated in the DB with the latest date of: '+new_date)
                conn.commit()
        
        de_duped_buffer.clear()
        
        if len(de_duped_buffer) == 0:
            print('Auxiliary Buffer Cleared')
        else:
            print('Failed to clear Auxiliary Buffer')
        
        await asyncio.sleep(120)



async def sleep_test(message):
    await client.wait_until_ready()

    while not client.is_closed:

        today = datetime.datetime.today().date().__format__("%Y-%m-%d")
        await client.send_message(message.channel,'Todays date is: ' + today)

        await asyncio.sleep(10)
        
        

@client.event
async def on_message(message):
    await client.wait_until_ready()

    today = datetime.datetime.today().date().__format__("%Y-%m-%d")
    server = client.get_server('380248307848577035')
    server_members = server.members 

    if message.content.startswith('*'):
        pass
    else:
        msg_buffer.append(message.author.id+'_'+today)

    if message.content.startswith('*bot'):
        await client.send_message(message.channel,'Beep Boop Beep')

    elif message.content.startswith('*update'):
        client.loop.create_task(db_update(message,msg_buffer))
        await client.send_message(message.channel,'Database Update Task Initialised')
        
    elif message.content.startswith('*decay'):
        #c.execute('SELECT * FROM user_info')
        #db_info = c.fetchall()
        await client.delete_message(message)
        await client.send_message(message.channel,'EC2 Response')
        msg_log = client.logs_from(client.get_channel('433532452653367296'),limit=5)
       # async for msg in msg_log:
       #     if msg.author.id == '116275390695079945':
       #        if len(msg.embeds) > 0:
       #            nadeko_lb.append(msg.embeds)
       #            print(nadeko_lb)
       #     else:
       #         pass
            
        #for db_entry in db_info:
         #   (user_id,date_time) = db_entry
            #if date_time < today:
                #await client.send_message(message.channel,'.xpadd '+str(-50)+' '+str(user_id))
                 
    elif message.content.startswith('*addxp'):
        await client.send_message(message.channel,'.xpadd 20 144326867275612162')

    elif message.content.startswith('*lbxp'):
        await client.send_message(message.channel,'.xplb')

    elif message.content.startswith('*sleeptest'):
        client.loop.create_task(sleep_test(message))
        await client.send_message(message.channel,'Sleep Task Started')
#448203968733118506

    elif message.content.startswith('*spindb'):
        await spin_db(message)

    elif message.content.startswith('*test'):                                                       
        for member in server_members:
            if member.bot == False:
                mem_roles = server.get_member(member.id).roles                
                for role in mem_roles:
                    if role.id == '446281091603628033':
                        
                        print(member, role, today)
                    elif role.id == '446281026894037003':
                        
                        print(member, role)
                    elif role.id == '446280876658262017':
                        
                        print(member, role)
                    elif role.id == '446280757183512586':
                        
                        print(member, role)
            else:
                pass
        conn.commit()        
        await client.send_message(message.channel, 'Info to terminal')

client.run(str(api_key))