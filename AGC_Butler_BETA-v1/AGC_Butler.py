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
import json
from pprint import pprint

client = Bot(description="Butler utility for AGC Server",
             command_prefix="*", pm_help=False)

@client.event
async def on_ready():
    await client.wait_until_ready()
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(
        discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('You are running AGC Butler[BETA]')
    print('Created by bot-steev0#0420')
    game = discord.Game("At your service, master")
    return await client.change_presence(status=discord.Status.idle, activity=game)

#! GLOBAL VARIABLES FOR SERVER

AGC_user_sqlite_file = './AGC_user_db.sqlite'
conn = sqlite3.connect(AGC_user_sqlite_file)
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

spawn_date = datetime.datetime.today().date().__format__("%Y-%m-%d")
server = None
server_members = None
dev_spam = client.get_channel(444385387109023745)


async def spin_db(message):
    await client.wait_until_ready()
    today = datetime.datetime.today().date().__format__("%Y-%m-%d")
    server_member_total = 0
    c.execute('DELETE from user_info')
    async for member in server_members:
        if member.bot == False:
            c.execute('INSERT INTO user_info VALUES(?,?)', (member.id, today))
            server_member_total += 1
            print(member.id, today)
    conn.commit()
    c.execute('SELECT count("user_id") FROM user_info')
    db_count = c.fetchall()
    (user_id,) = db_count[0]
    await client.send_message(message.channel, 'Database has been filled with members from Server: '+str(server)+'\nServer Member Count: '+str(server_member_total)+'\nDatabase Member Count: '+str(user_id))

# async def backup_db(message):

# async def spawn_webclient(message):
# https://discord.gg/tC4EedV


async def db_update(message, msg_buffer):

    await client.wait_until_ready()

    while not client.is_closed:

        await client.send_message(message.channel, msg_buffer)

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
            new_date = '2018-05-10'  # user_data[1]

            # SQL Info
            c.execute('SELECT * FROM user_info WHERE user_id == (?)',
                      (buffer_user_id,))
            user_entry = c.fetchall()

            if len(user_entry) == 0:
                c.execute('INSERT INTO user_info VALUES(?,?)',
                          (buffer_user_id, new_date))
                await client.send_message(message.channel, 'UserID: '+buffer_user_id+' has been inserted into the DB with the latest date of: ' + new_date)
                conn.commit()
            else:
                c.execute(
                    'UPDATE user_info SET date_time = (?) WHERE user_id == (?)', (new_date, buffer_user_id))
                await client.send_message(message.channel, 'UserID: '+buffer_user_id+' has been updated in the DB with the latest date of: '+new_date)
                conn.commit()

        de_duped_buffer.clear()

        if len(de_duped_buffer) == 0:
            print('Auxiliary Buffer Cleared')
        else:
            print('Failed to clear Auxiliary Buffer')

        await asyncio.sleep(120)

@client.event
async def on_message(message):
    await client.wait_until_ready()

    # if message.content.startswith('*'):
    #   pass
    # else
    #   msg_buffer.append(message.author.id+'_'+today)
    # if bool(server) == False:
    #    await client.send_message(dev_spam,'Apologies sir, but it would seem that you have not yet #configured the server parameters, please do so by executing the `*init` command.')
    #else:

    if message.content.startswith('*bot'):
        await client.send_message(message.channel, 'Beep Boop Beep')

    elif message.content.startswith('*update'):
        client.loop.create_task(db_update(message, msg_buffer))
        await client.send_message(message.channel, 'Database Update Task Initialised')

    elif message.author.id == 116275390695079945 and len(message.embeds)>0:
        #~ Piece of shit emojis to handle Nadeko's leaderboard interaction
        #~ U+2B05 	\xE2\xAC\x85 ⬅
        #~ U+27A1 	\xE2\x9E\xA1 ➡
        me = discord.utils.get(server_members, name='- bot steev -')
        await asyncio.sleep(4)
        nadeko_lb.append(message.embeds)
        print('page: 1')
        print(nadeko_lb)
        for x in range(10):
            await client.wait_for_reaction(emoji='\u27A1')
            await asyncio.sleep(2)
            nadeko_lb.append(message.embeds)
            print('page:'+str(x+x))
            print(message.embeds)
            await client.remove_reaction(message,'\u27A1',me)            
            await asyncio.sleep(2)
            nadeko_lb.append(message.embeds)
            print('page:'+str((x+x)-1))
            print(message.embeds)
        
    elif message.content.startswith('*write'):
        print('\n\n\n')
        with open('AGC_Leaderboard_JSON.txt', 'a') as f: 
            for nadeko_lb_page in nadeko_lb:
                for page_info in nadeko_lb_page:
                    f.write(json.dumps(page_info))
        f.close

    elif message.content.startswith('*parse'):
        with open('AGC_Leaderboard.JSON', 'r') as f:
            json_data = json.load(f)
            cntr = 0
            for x in json_data:
                raw_fields = json_data[cntr]['fields']
                cntr2 = 0
                for y in raw_fields:
                    raw_entry_value = raw_fields[cntr2]['value']
                    raw_entry_name = raw_fields[cntr2]['name']
                    
                    split_entry_value = raw_entry_value.split('-')

                    final_entry_value = split_entry_value[1].lstrip()
                    final_entry_name = raw_entry_name[3:].lstrip()

                    print(final_entry_name + ' ' + final_entry_value)
                    cntr2 += 1
                cntr += 1
        f.close()

    elif message.content.startswith('*clfilelb'):
        with open('AGC_Leaderboard_JSON.txt', 'w') as f:
            f.write('')
        f.close()    
        nadeko_lb.clear()

    elif message.content.startswith('*spindb'):
        await spin_db(message)

    #elif message.content.startswith('*test'):
    #    for member in server_members:
    #        if member.bot == False:
    #            mem_roles = server.get_member(member.id).roles
    #            for role in mem_roles:
    #                if role.id == '446281091603628033':
    #                    print(member, role, today)
    #                elif role.id == '446281026894037003':
    #                    print(member, role)
    #                elif role.id == '446280876658262017':
    #                    print(member, role)
    #                elif role.id == '446280757183512586':
    #                    print(member, role)
    #        else:
    #            pass
    #    conn.commit()
    #    await client.send_message(message.channel, 'Info to terminal')
    
client.run(str(api_key))
