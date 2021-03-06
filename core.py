# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import platform
import json
from options.opus_loader import load_opus_lib
import re
import csv
import asyncio
import aiohttp
import datetime
import psycopg2
import psycopg2.extras
import socket

try:
    from plugin.database import Database
except:
    pass

load_opus_lib()

### Core

tmp_config = json.loads(str(open('options/config.js').read()))
config = tmp_config['config']
emojiUnicode = tmp_config['unicode']
exchange = tmp_config['exchange']
botzillaChannels = tmp_config['channels']
bot = Bot(description="BotZilla is built / maintained / self hosted by PuffDip\nUserdata may be stored for better experience.\n\nUpvote would be appreciated:\nhttps://discordbots.org/bot/397149515192205324", command_prefix=config['prefix'], pm_help=False)
dbl = False
try:
    dbltoken = config['discordbotlist_api']
    headers = {"Authorization": dbltoken}
    dbl = True
except:
    print('Core: DiscordBotList api key not found')
    pass
database_file_found = False
database_settings = tmp_config['database']

try:
    database = Database(bot)
    database_file_found = True
except:
    print('Core: Database files not found')
    pass


async def dbimport():
    """
    Import CSV data from import folder
    """

    # Users
    try:
        with open(database.database_import_location_users, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            import_to_db = []
            for row in reader:
                row = str(row[0]).replace('(', '').replace(')', '')
                row = row.split(',')
                pattern = re.compile('[\W_]+')
                name = pattern.sub('', row[1])
                row = (row[0], '{}'.format(name))
                import_to_db.append(row)
            try:
                insert_query = 'insert into botzilla.users (ID, name) values %s'
                psycopg2.extras.execute_values(
                    database.cur, insert_query, import_to_db, template=None, page_size=1000000000
                )
                database.cur.execute("ROLLBACK;")
            except Exception as e:
                if 'duplicate key' in str(e.args):
                    pass
                else:
                    print(f'{type(e).__name__} : {e}')

    except Exception as e:
        if 'duplicate key' in str(e.args):
            pass
        else:
            print(f'{type(e).__name__} : {e}')


    try:
        with open(database.database_import_location_blacklist, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                try:
                    row = str(row).replace('["', '')
                    row = str(row).replace('"]', '')
                    print(row)
                    database.cur.execute("INSERT INTO botzilla.blacklist (ID, server_name, reason, total_votes) VALUES{};".format(row))
                    database.cur.execute("ROLLBACK;")
                except Exception as e:
                    if 'duplicate key' in str(e.args):
                        pass
                    else:
                        print(f'{type(e).__name__} : {e}')
    except Exception as e:
        if 'duplicate key' in str(e.args):
            pass
        else:
            print(f'{type(e).__name__} : {e}')


    # Blacklist
    try:
        database.cur.execute("SELECT ID from botzilla.blacklist;")
        rows = database.cur.fetchall()
        database.cur.execute("ROLLBACK;")
        for item in rows:
            item = str(item).replace('(', '')
            item = item.replace(',)', '')
            database.blacklist.append(item)
    except Exception as e:
        if 'duplicate key' in str(e.args):
            pass
        else:
            print(f'{type(e).__name__} : {e}')

    for command in bot.walk_commands():
        try:
            hel = command.__dict__
            safe_name = str(command.name).replace("'", "\'").replace(';', '')
            safe_cog = str(command.cog_name).replace("'", "\'").replace(';', '')
            safe_info = str(hel['help']).replace("'", "\'").replace(';', '<insert semicolon here>')
            database.cur.execute("INSERT INTO botzilla.help (name, cog, info) VALUES('{}', '{}', '{}');".format(safe_name, safe_cog, safe_info))
            database.cur.execute("ROLLBACK;")

        except Exception as e:
            if 'duplicate key' in str(e.args):
                pass
            else:
                print(f'{type(e).__name__} : {e}')

    print('DATABASE IMPORT BACKUP DONE')


async def get_users():
    """
    Update datebase with current active users
    """

    for server in bot.servers:
        for member in server.members:
            try:
                pattern = re.compile('[\W_]+')
                name = pattern.sub('', str(member.name))
                database.cur.execute("INSERT INTO botzilla.users (ID, name) VALUES ({}, '{}');".format(member.id, name))
                database.cur.execute("ROLLBACK;")

            except Exception as e:
                if 'duplicate key' in str(e.args):
                    pass
                else:
                    print(f'{type(e).__name__} : {e}')

    print('DATABASE USER IMPORT DONE')


async def get_new_server_users(server):
    """
    Update datebase with current active users
    """

    for member in server.members:
        try:
            pattern = re.compile('[\W_]+')
            name = pattern.sub('', str(member.name))
            database.cur.execute("INSERT INTO botzilla.users (ID, name) VALUES ({}, '{}');".format(member.id, name))
            database.cur.execute("ROLLBACK;")

        except Exception as e:
            if 'duplicate key' in str(e.args):
                pass
            else:
                print(f'{type(e).__name__} : {e}')

    print('DATABASE USER IMPORT DONE')


async def total_online_user_tracker():
    while True:
        game = discord.Game(name='{} online users'.format(sum(1 for m in set(bot.get_all_members()) if m.status != discord.Status.offline)), type=3)
        await bot.change_presence(game=game)
        await asyncio.sleep(8)
        game = discord.Game(name='{}help'.format(config['prefix']), type=2)
        await bot.change_presence(game=game)
        await asyncio.sleep(8)
        game = discord.Game(name='hendrikx-itc.com', type=1)
        await bot.change_presence(game=game)
        await asyncio.sleep(8)


@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + ' (ID:' + bot.user.id + ') | Connected to ' + str(
        len(bot.servers)) + ' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                               platform.python_version()))
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('--------')

    bot.remove_command('help')
    #plugins

    plugins = (
        "admin",
        "exchange",
        "database",
        "fun",
        "music",
        "games",
        "gamestats",
        "information",
        "python_code_in_dc",
        "test",
        "help"
    )

    # load plugins
    for p in plugins:
        bot.load_extension("plugin.{}".format(p))


    database.conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port='{}' password={}".format(
        database_settings['db_name'],
        database_settings['user'],
        database_settings['ip'],
        database_settings['port'],
        database_settings['password']
    ))

    if dbl is True:
        url = "https://discordbots.org/api/bots/{}/stats".format(bot.user.id)
        payload = {"server_count": len(bot.servers)}
        async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url=url, data=payload, headers=headers)

    bot.loop.create_task(dbimport())
    bot.loop.create_task(total_online_user_tracker())


@bot.event
async def on_member_remove(member):
    # sebi server
    if member.server.id == '265828729970753537':
        welcome_channel = bot.get_channel('426860084161937410')
        join_date = member.joined_at
        created_at = member.created_at
        embed = discord.Embed(title='Bye!',
                              description=f'{member.mention}, :wave:\nJoined at **`{join_date.strftime("%Y-%m-%d %H:%M:%S")}`**',
                              colour=0xf20006)
        embed.add_field(name=f'**`{member.name}`**\'s additional information',
                        value=f'Joined at **`{join_date.strftime("%Y-%m-%d %H:%M:%S")}`**\nDisplay name **`{member.name}`**\nAccount created at **`{created_at.strftime("%Y-%m-%d %H:%M:%S")}`**')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Bot: {member.bot}')
        last_message = await bot.send_message(welcome_channel, embed=embed)
        await bot.add_reaction(last_message, emojiUnicode['succes'])

    #BotZilla server
    if member.server.id == '406908371246252052':
        welcome_channel = bot.get_channel('406908371808157697')
        join_date = member.joined_at
        created_at = member.created_at
        embed = discord.Embed(title='Bye!',
                              description=f'{member.mention}, :wave:\nJoined at **`{join_date.strftime("%Y-%m-%d %H:%M:%S")}`**',
                              colour=0xf20006)
        embed.add_field(name=f'**`{member.name}`**\'s additional information',
                        value=f'Joined at **`{join_date.strftime("%Y-%m-%d %H:%M:%S")}`**\nDisplay name **`{member.name}`**\nAccount created at **`{created_at.strftime("%Y-%m-%d %H:%M:%S")}`**')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Bot: {member.bot}')
        last_message = await bot.send_message(welcome_channel, embed=embed)
        await bot.add_reaction(last_message, emojiUnicode['succes'])


@bot.event
async def on_member_join(member):
    print('MEMBER JOINED {} | {} Joined: {}'.format(member.name, member.id, member.server))
    # sebi server
    if member.server.id == '265828729970753537':
        welcome_channel = bot.get_channel('426860084161937410')
        a = []
        for emoji in member.server.emojis:
            emoji = discord.utils.get(bot.get_all_emojis(), id=emoji.id)
            a.append(str(emoji))
        emojis = " - ".join(a)
        join_date = member.joined_at
        created_at = member.created_at
        embed = discord.Embed(title='Welcome!',
                              description=f'{member.mention}, Enjoy your stay!\n\nAll emoji\'s on this server:\n{emojis}',
                              colour=0xf20006)
        embed.add_field(name=f'**`{member.name}`**\'s additional information',
                        value=f'Joined at **`{join_date.strftime("%Y-%m-%d %H:%M:%S")}`**\nDisplay name **`{member.display_name}`**\nAccount created at **`{created_at.strftime("%Y-%m-%d %H:%M:%S")}`**')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Bot: {member.bot}')
        last_message = await bot.send_message(welcome_channel, embed=embed)
        await bot.add_reaction(last_message, emojiUnicode['succes'])

    #BotZilla server
    if member.server.id == '406908371246252052':
        welcome_channel = bot.get_channel('406908371808157697')
        a = []
        for emoji in member.server.emojis:
            emoji = discord.utils.get(bot.get_all_emojis(), id=emoji.id)
            a.append(str(emoji))
        emojis = " - ".join(a)
        join_date = member.joined_at
        created_at = member.created_at
        embed = discord.Embed(title='Welcome!',
                              description=f'{member.mention}, Enjoy your stay!\n\nAll emoji\'s on this server:\n{emojis}`**',
                              colour=0xf20006)
        embed.add_field(name=f'**`{member.name}`**\'s additional information',
                        value=f'Joined at **`{join_date.strftime("%Y-%m-%d %H:%M:%S")}`**\nDisplay name **`{member.display_name}`**\nAccount created at **`{created_at.strftime("%Y-%m-%d %H:%M:%S")}`**')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Bot: {member.bot}')
        last_message = await bot.send_message(welcome_channel, embed=embed)
        await bot.add_reaction(last_message, emojiUnicode['succes'])

    try:
        pattern = re.compile('[\W_]+')
        name = pattern.sub('', str(member.name))
        database.cur.execute("INSERT INTO botzilla.users (ID, name) VALUES ({}, '{}');".format(member.id, name))
        database.cur.execute("ROLLBACK;")
        print('DATABASE ADD {} | {} has been added to the database'.format(member.name, member.id))
    except Exception as e:
        if 'duplicate key' in str(e.args):
            pass
        else:
            print(f'{type(e).__name__} : {e}')




@bot.event
async def on_message_edit(before, message):
    if message.author.bot: return
    if str(message.content).startswith('{}play'.format(config['prefix'])): return

    database.cur.execute("SELECT ID FROM botzilla.blacklist;")
    row = database.cur.fetchall()
    row = str(row).replace('[', '').replace('(', '').replace(']', '').replace(',', '').replace(')', '')
    database.cur.execute("ROLLBACK;")
    database.cur.execute("SELECT * FROM botzilla.mute;")
    muted = database.cur.fetchall()
    database.cur.execute("ROLLBACK;")
    if str(message.author.id) in row:
        if str(message.content).startswith('{}'.format(config['prefix'])):
            database.cur.execute("SELECT reason FROM botzilla.blacklist where ID = {};".format(message.author.id))
            reason = database.cur.fetchall()
            database.cur.execute("ROLLBACK;")
            reason = str(reason).replace("'", '').replace('[', '').replace('(', '').replace(',', '').replace(')', '').replace(']', '')

            database.cur.execute("SELECT total_votes FROM botzilla.blacklist where ID = {};".format(message.author.id))
            votes = database.cur.fetchall()
            database.cur.execute("ROLLBACK;")
            votes = str(votes).replace('(', '').replace('[', '').replace(',', '').replace(')', '').replace(']', '')

            embed = discord.Embed(title='{}:'.format(message.author.name),
                                  description='You have been blacklisted with **`{}`** votes,\n\nReason:\n```{}```'.format(votes, reason),
                                  colour=0xf20006)
            last_message = await bot.send_message(message.channel, embed=embed)
            await bot.add_reaction(last_message, emojiUnicode['warning'])
            return
        else:
            return

    try:
        if str(message.author.id) in str(muted[0]):
            try:
                await bot.delete_message(message)
                return
            except Exception as e:
                return
    except Exception as e:
        pass


    low_key_message = str(message.content).lower()
    if 'shit' in low_key_message:
        total = str(message.content).lower().count('shit')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'shit', total = (total+{}) where swearword = 'shit';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'fuck' in low_key_message:
        total = str(message.content).lower().count('fuck')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'fuck', total = (total+{}) where swearword = 'fuck';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'damn' in low_key_message:
        total = str(message.content).lower().count('damn')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'damn', total = (total+{}) where swearword = 'damn';".format(total))
        database.cur.execute("ROLLBACK;")

    if '?' in low_key_message:
        total = str(message.content).lower().count('?')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'questionmark', total = (total+{}) where swearword = 'questionmark';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'crap' in low_key_message:
        total = str(message.content).lower().count('crap')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'crap', total = (total+{}) where swearword = 'crap';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'pussy' in low_key_message:
        total = str(message.content).lower().count('pussy')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'pussy', total = (total+{}) where swearword = 'pussy';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'wtf' in low_key_message:
        total = str(message.content).lower().count('wtf')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'wtf', total = (total+{}) where swearword = 'wtf';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'fag' in low_key_message:
        total = str(message.content).lower().count('fag')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'fag', total = (total+{}) where swearword = 'fag';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'gay' in low_key_message:
        total = str(message.content).lower().count('gay')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'gay', total = (total+{}) where swearword = 'gay';".format(total))
        database.cur.execute("ROLLBACK;")

    sp = message.content.split(None, 1)
    if sp:
        sp[0] = sp[0].lower()
        message.content = ' '.join(sp)
        await bot.process_commands(message)


@bot.event
async def on_message(message):
    # infect system
    database.cur.execute(f"SELECT * FROM botzilla.infect WHERE ID = {message.author.id}")
    infect = database.cur.fetchone()
    database.cur.execute("ROLLBACK;")
    now = str(datetime.datetime.now())
    if infect is not None:
        if now < infect[1]:
            try:
                try:
                    int(infect[2])
                    infected_emoji = discord.utils.get(bot.get_all_emojis(), id=infect[2])
                except Exception as e:
                    infected_emoji = infect[2]
                await bot.add_reaction(message, infected_emoji)
            except Exception as e:
                database.cur.execute(f"DELETE FROM botzilla.infect WHERE ID = {message.author.id}")
                database.conn.commit()
                database.cur.execute("ROLLBACK;")
        else:
            database.cur.execute(f"DELETE FROM botzilla.infect WHERE ID = {message.author.id}")
            database.conn.commit()
            database.cur.execute("ROLLBACK;")

    # If bot, ignore message
    if message.author.bot: return
    database.cur.execute("SELECT ID FROM botzilla.blacklist;")
    row = database.cur.fetchall()
    row = str(row).replace('[', '').replace('(', '').replace(']', '').replace(',', '').replace(')', '')
    database.cur.execute("ROLLBACK;")
    database.cur.execute(f"SELECT * FROM botzilla.mute;")
    muted = database.cur.fetchall()
    database.cur.execute("ROLLBACK;")
    if str(message.author.id) in row:
        if str(message.content).startswith('{}'.format(config['prefix'])):
            database.cur.execute("SELECT reason FROM botzilla.blacklist where ID = {};".format(message.author.id))
            reason = database.cur.fetchall()
            database.cur.execute("ROLLBACK;")
            reason = str(reason).replace("'", '').replace('[', '').replace('(', '').replace(',', '').replace(')', '').replace(']', '')

            database.cur.execute("SELECT total_votes FROM botzilla.blacklist where ID = {};".format(message.author.id))
            votes = database.cur.fetchall()
            database.cur.execute("ROLLBACK;")
            votes = str(votes).replace('(', '').replace('[', '').replace(',', '').replace(')', '').replace(']', '')

            embed = discord.Embed(title='{}:'.format(message.author.name),
                                  description='You have been blacklisted with **`{}`** votes,\n\nReason:\n```{}```'.format(votes, reason),
                                  colour=0xf20006)
            last_message = await bot.send_message(message.channel, embed=embed)
            await bot.add_reaction(last_message, emojiUnicode['warning'])
            return
        else:
            return

    try:
        if str(message.author.id) in str(muted[0]):
            try:
                await bot.delete_message(message)
                return
            except Exception as e:
                return
    except Exception as e:
        pass

    low_key_message = str(message.content).lower()
    if 'shit' in low_key_message:
        total = str(message.content).lower().count('shit')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'shit', total = (total+{}) where swearword = 'shit';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'fuck' in low_key_message:
        total = str(message.content).lower().count('fuck')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'fuck', total = (total+{}) where swearword = 'fuck';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'damn' in low_key_message:
        total = str(message.content).lower().count('damn')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'damn', total = (total+{}) where swearword = 'damn';".format(total))
        database.cur.execute("ROLLBACK;")

    if '?' in low_key_message:
        total = str(message.content).lower().count('?')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'questionmark', total = (total+{}) where swearword = 'questionmark';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'crap' in low_key_message:
        total = str(message.content).lower().count('crap')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'crap', total = (total+{}) where swearword = 'crap';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'pussy' in low_key_message:
        total = str(message.content).lower().count('pussy')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'pussy', total = (total+{}) where swearword = 'pussy';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'wtf' in low_key_message:
        total = str(message.content).lower().count('wtf')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'wtf', total = (total+{}) where swearword = 'wtf';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'fag' in low_key_message:
        total = str(message.content).lower().count('fag')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'fag', total = (total+{}) where swearword = 'fag';".format(total))
        database.cur.execute("ROLLBACK;")

    if 'gay' in low_key_message:
        total = str(message.content).lower().count('gay')
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'gay', total = (total+{}) where swearword = 'gay';".format(total))
        database.cur.execute("ROLLBACK;")

    sp = message.content.split(None, 1)
    if sp:
        sp[0] = sp[0].lower()
        message.content = ' '.join(sp)
        await bot.process_commands(message)


@bot.event
async def on_server_join(server):
    print('SERVER ADDED {} | {} BotZilla has been added'.format(server.name, server.id))
    if database_file_found:
        if database.database_online:
            await get_new_server_users(server)

    if dbl is True:
        url = "https://discordbots.org/api/bots/{}/stats".format(bot.user.id)
        payload = {"server_count": len(bot.servers)}
        async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url=url, data=payload, headers=headers)


@bot.event
async def on_server_remove(server):
    print('SERVER REMOVED {} | {} BotZilla has been removed'.format(server.name, server.id))
    if dbl is True:
        url = "https://discordbots.org/api/bots/{}/stats".format(bot.user.id)
        payload = {"server_count": len(bot.servers)}
        async with aiohttp.ClientSession() as aioclient:
            await aioclient.post(url=url, data=payload, headers=headers)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description=f'{error}',
                              colour=0xf20006)
        last_message = await bot.send_message(ctx.message.channel, embed=embed)
        await bot.add_reaction(last_message, emojiUnicode['warning'])
        return

if __name__ == '__main__':
    bot.run(config['bot-key'])