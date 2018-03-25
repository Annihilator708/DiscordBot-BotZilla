import discord
from discord.ext import commands
import json
import datetime
import asyncio

try:
    from plugin.database import Database
except Exception as e:
    pass


tmp_config = json.loads(str(open('./options/config.js').read()))
config = tmp_config['config']
owner_list = config['owner-id']


class Help:
    def __init__(self, bot):
        self.bot = bot
        bot_version = 'V0.7'
        self.version = bot_version
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']
        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except Exception as e:
            print('Help: Database files not found - {}'.format(e.args))
            pass

    @commands.command(pass_context=True, hidden=True)
    async def help(self, ctx, command: str = None):
        """
        Show this message
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!help <{command}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        self.database.cur.execute("select name from botzilla.help where cog = 'Games';")
        Games_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Games_commands = []
        Games_commands.append('**------**')
        for i in Games_cog:
            i = '-`{}{}`'.format(self.config['prefix'], i[0])
            Games_commands.append(i)
        Games_commands.sort()
        Games_commands.append('**------**')
        Games_name = "\n".join(Games_commands)

        self.database.cur.execute("select name from botzilla.help where cog = 'GameStats';")
        GameStats_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        GameStats_commands = []
        GameStats_commands.append('**------**')
        for i in GameStats_cog:
            i = '-`{}{}`'.format(self.config['prefix'], i[0])
            GameStats_commands.append(i)
        GameStats_commands.sort()
        GameStats_commands.append('**------**')
        GameStats_name = "\n".join(GameStats_commands)

        self.database.cur.execute("select name from botzilla.help where cog = 'Fun';")
        Fun_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Fun_commands = []
        Fun_commands.append('**------**')
        for i in Fun_cog:
            i = '-`{}{}`'.format(self.config['prefix'], i[0])
            Fun_commands.append(i)
        Fun_commands.sort()
        Fun_commands.append('**------**')
        Fun_name = "\n".join(Fun_commands)

        self.database.cur.execute("select name from botzilla.help where cog = 'Information';")
        Information_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Information_commands = []
        Information_commands.append('**------**')
        for i in Information_cog:
            i = '-`{}{}`'.format(self.config['prefix'], i[0])
            Information_commands.append(i)
        Information_commands.sort()
        Information_commands.append('**------**')
        Information_name = "\n".join(Information_commands)

        self.database.cur.execute("select name from botzilla.help where cog = 'Music';")
        Music_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Music_commands = []
        Music_commands.append('**------**')
        for i in Music_cog:
            i = '-`{}{}`'.format(self.config['prefix'], i[0])
            Music_commands.append(i)
        Music_commands.sort()
        Music_commands.append('**------**')
        Music_name = "\n".join(Music_commands)

        self.database.cur.execute("select name from botzilla.help where cog = 'Utils';")
        Utils_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Utils_commands = []
        Utils_commands.append('**------**')
        for i in Utils_cog:
            i = '-`{}{}`'.format(self.config['prefix'], i[0])
            Utils_commands.append(i)
        Utils_commands.sort()
        Utils_commands.append('**------**')
        Utils_name = "\n".join(Utils_commands)

        self.database.cur.execute("select name from botzilla.help where cog = 'Images';")
        Images_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Images_commands = []
        Images_commands.append('**------**')
        for i in Images_cog:
            i = '-`{}{}`'.format(self.config['prefix'], i[0])
            Images_commands.append(i)
        Images_commands.sort()
        Images_commands.append('**------**')
        Images_name = "\n".join(Images_commands)

        self.database.cur.execute("select name from botzilla.help where cog = 'Exchange';")
        Exchange_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Exchange_commands = []
        Exchange_commands.append('**------**')
        for i in Exchange_cog:
            i = '-`{}{}`'.format(self.config['prefix'], i[0])
            Exchange_commands.append(i)
        Exchange_commands.sort()
        Exchange_commands.append('**------**')
        Exchange_name = "\n".join(Exchange_commands)

        if ctx.message.author.id in self.owner_list:
            self.database.cur.execute("select name from botzilla.help where cog = 'AdminCommands';")
            Admin_cog = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            Admin_commands = []
            Admin_commands.append('**------**')
            for i in Admin_cog:
                i = '-`{}{}`'.format(self.config['prefix'], i[0])
                Admin_commands.append(i)
            Admin_commands.sort()
            Admin_commands.append('**------**')
            Admin_name = "\n".join(Admin_commands)

        if command is None:
            embed = discord.Embed(title="Help for {}:".format(ctx.message.author.name),
                                  description='**`BotZilla is built / maintained / self hosted by PuffDip\nUserdata may be stored for better experience.`**\t   **`{}`**'.format(self.version),
                                  color=0xf20006)

            embed.add_field(name='Games', value=Games_name, inline=True)
            embed.add_field(name='GameStats', value=GameStats_name, inline=True)
            embed.add_field(name='Fun', value=Fun_name, inline=True)

            embed.add_field(name='Information', value=Information_name, inline=True)
            embed.add_field(name='Music', value=Music_name, inline=True)
            embed.add_field(name='Utils', value=Utils_name, inline=True)

            embed.add_field(name='Images', value=Images_name, inline=True)
            embed.add_field(name='Exchange', value=Exchange_name, inline=True)
            if ctx.message.author.id in self.owner_list:
                embed.add_field(name='Admin', value=Admin_name, inline=True)
            else:
                embed.add_field(name='-', value='-')

            embed.add_field(name='More info?', value='**`{}help [command]`**'.format(self.config['prefix']), inline=False)
            embed.add_field(name='On the internet:', value='***Discord Bot List, Upvote would be appreciated :heart:***\n**https://discordbots.org/bot/397149515192205324**\n\n***Official BotZilla Server:***\n**https://discord.gg/ybgfVQA**', inline=False)

            #embed.set_thumbnail(url='https://raw.githubusercontent.com/Annihilator708/DiscordBot-BotZilla/master/icon.png')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            return

        command = str(command).replace(';', '').replace("'", '').lower()
        try:
            self.database.cur.execute("select * from botzilla.help where name = '{}';".format(command))
            cog = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            if '<insert semicolon here>' in str(cog[0][2]):
                name = cog[0][0]
                cog = str(cog[0][2]).replace('<insert semicolon here>', ';')
                embed = discord.Embed(title="Help for {}:".format(ctx.message.author.name),
                                      description='**`BotZilla is built / maintained / self hosted by PuffDip\nUserdata may be stored for better experience.`**\t   **`{}`**'.format(self.version),
                                      color=0xf20006)
                embed.add_field(name='Command name', value='**`{}`**'.format(name), inline=False)
                embed.add_field(name='Description', value='**`{}`**'.format(cog), inline=False)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                return

            embed = discord.Embed(title="Help for {}:".format(ctx.message.author.name),
                                  color=0xf20006)
            embed.add_field(name='Command name', value='**`{}`**'.format(cog[0][0]), inline=False)
            embed.add_field(name='Description', value='**`{}`**'.format(cog[0][2]), inline=False)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

        except Exception as e:
            print(e.args)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Command **`{}`** not found. You can use **`{}help`** to see all the commands available.\nTo get more info about a command listed in **`{}help`**, use **`{}help [command]`** instead.\nFor Example: **`{}help inv`**'.format(
                                      command, self.config['prefix'], self.config['prefix'], self.config['prefix'], self.config['prefix']
                                  ),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])


    @commands.command(pass_context=True)
    async def test(self, ctx):
        """
        Show this message
        """

        #init
        self.emoji_start = '\u23ee'
        self.emoji_five_back = '\u23ea'
        self.emoji_oneback = '\u25c0'
        self.emoji_oneahead = '\u25b6'
        self.emoji_five_ahead = '\u23e9'
        self.emoji_end = '\u23ed'

        def get_command_by_name(command_name):
            self.database.cur.execute("select * from botzilla.help where name = '{}';".format(command_name))
            command_object = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            return command_object

        def get_commands_by_cog(cog_name):
            self.database.cur.execute("select * from botzilla.help where cog = '{}';".format(cog_name))
            command_object = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            return command_object

        def get_short_desc(command_object):
            command_desc = command_object[2]
            split_lines = command_desc.splitlines(keepends=True)
            list_desc = [i.strip() for i in split_lines if i != '\n']
            print(list_desc)
            try:
                short_desc = f'**```\n{list_desc[0]}\n{list_desc[1]}```**'
            except Exception as e:
                short_desc = f'**```\n{split_lines}\n```**'
            print(short_desc)
            return short_desc

        def embed_help(content, reaction):
            embed = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
                                  description='{1}\n{0.user.name} : {0.reaction.emoji}'.format(reaction, content),
                                  colour=0xf20006)
            return embed

        async def wait_for_reaction(message, new_page):
            reaction = await self.bot.wait_for_reaction([self.emoji_start, self.emoji_five_back, self.emoji_oneback, self.emoji_oneahead, self.emoji_five_ahead, self.emoji_end], message=message)
            if ctx.message.author.id == reaction.user.id:
                return await self.bot.edit_message(message, embed=new_page), reaction
            else:
                await wait_for_reaction(message, new_page)

        def new_page(cog):
            data = get_commands_by_cog(cog)
            data = sorted(data)
            pages = []
            new_page = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
                                     colour=0xf20006)
            split = lambda x, n: x if not x else [x[:n]] + [split([] if not -(len(x) - n) else x[-(len(x) - n):], n)][0]

            self.database.cur.execute("select count(cog) from botzilla.help where cog = '{}';".format(cog))
            count_cog = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

            if count_cog[0] > 3:
                count = int(count_cog[0] // 3)
            else:
                count = 1
            page_number = 0
            for item in range(count):
                if count <= 1 :
                    new_list = data
                else:
                    new_list = split(data, 3)[page_number]
                page_number += 1
                for item in new_list:
                    new_page.add_field(name=f"Category: **`{cog}`**\n{self.config['prefix']}{item[0]}\n\n",
                                    value=get_short_desc(item[0]),
                                    inline=False)
                    pages.append(new_page)
            return pages

        def generate_pages():
            all = []
            all.append(new_page('Games'))
            all.append(new_page('GameStats'))
            all.append(new_page('Fun'))
            all.append(new_page('Music'))
            all.append(new_page('Utils'))
            all.append(new_page('Images'))
            all.append(new_page('Exchange'))

            paginator = {}
            page_number = 0
            for items in all:
                for item in items:
                    page_number += 1
                    paginator[str(page_number)] = item
            return paginator

        #test

        # Pages
        page0 = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
                              description='This command is under construction and may not work correctly',
                              colour=0xf20006)
        start = await self.bot.say(embed=page0)

        generate_pages = generate_pages()

        # # Games
        # Games = get_commands_by_cog('Games')
        # Games = sorted(Games)
        # page1 = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
        #                       description='Category: **`Games`**',
        #                       colour=0xf20006)
        # for i in Games:
        #     page1.add_field(name=f"{self.config['prefix']}{i[0]}",
        #                     value=get_short_desc(i),
        #                     inline=False)
        #
        # # Game Stats
        # Gamestats = get_commands_by_cog('GameStats')
        # Gamestats = sorted(Gamestats)
        # page2 = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
        #                       description='Category: **`Games Stats`**',
        #                       colour=0xf20006)
        # for i in Gamestats:
        #     page2.add_field(name=f"{self.config['prefix']}{i[0]}",
        #                     value=get_short_desc(i),
        #                     inline=False)
        #
        # # Fun
        # Fun = get_commands_by_cog('Fun')
        # Fun = sorted(Fun)
        # page3 = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
        #                       description='Category: **`Fun`**',
        #                       colour=0xf20006)
        # for i in Fun:
        #     page3.add_field(name=f"{self.config['prefix']}{i[0]}",
        #                     value=get_short_desc(i),
        #                     inline=False)
        #
        # # Information
        # Information = get_commands_by_cog('Information')
        # Information = sorted(Information)
        # page4 = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
        #                       description='Category: **`Information`**',
        #                       colour=0xf20006)
        # for i in Information:
        #     page4.add_field(name=f"{self.config['prefix']}{i[0]}",
        #                     value=get_short_desc(i),
        #                     inline=False)
        #
        # # Music
        # Music = get_commands_by_cog('Music')
        # Music = sorted(Music)
        # page5 = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
        #                       description='Category: **`Music`**',
        #                       colour=0xf20006)
        # for i in Music:
        #     page5.add_field(name=f"{self.config['prefix']}{i[0]}",
        #                     value=get_short_desc(i),
        #                     inline=False)
        #
        # # Utils
        # Utils = get_commands_by_cog('Utils')
        # Utils = sorted(Utils)
        # page6 = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
        #                       description='Category: **`Utils`**',
        #                       colour=0xf20006)
        # for i in Utils:
        #     page6.add_field(name=f"{self.config['prefix']}{i[0]}",
        #                     value=get_short_desc(i),
        #                     inline=False)
        #
        # # Images
        # Images = get_commands_by_cog('Images')
        # Images = sorted(Images)
        # page7 = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
        #                       description='Category: **`Images`**',
        #                       colour=0xf20006)
        # for i in Images:
        #     page7.add_field(name=f"{self.config['prefix']}{i[0]}",
        #                     value=get_short_desc(i),
        #                     inline=False)
        #
        # # Exchange
        # Exchange = get_commands_by_cog('Exchange')
        # Exchange = sorted(Exchange)
        # page8 = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
        #                       description='Category: **`Exchange`**',
        #                       colour=0xf20006)
        # for i in Exchange:
        #     page8.add_field(name=f"{self.config['prefix']}{i[0]}",
        #                     value=get_short_desc(i),
        #                     inline=False)

        await self.bot.add_reaction(start, self.emoji_start)
        await self.bot.add_reaction(start, self.emoji_five_back)
        await self.bot.add_reaction(start, self.emoji_oneback)
        await self.bot.add_reaction(start, self.emoji_oneahead)
        await self.bot.add_reaction(start, self.emoji_five_ahead)
        await self.bot.add_reaction(start, self.emoji_end)

        await asyncio.sleep(0.6)
        await self.bot.say('Ready...')

        for t in generate_pages.keys():
            new_page, reaction = await wait_for_reaction(start, generate_pages[t])
            await self.bot.say(reaction.reaction.emoji)
        # new_page, reaction = await wait_for_reaction(new_page, page2)
        # await self.bot.say(reaction.reaction.emoji)
        # new_page, reaction = await wait_for_reaction(new_page, page3)
        # await self.bot.say(reaction.reaction.emoji)
        # new_page, reaction = await wait_for_reaction(new_page, page4)
        # await self.bot.say(reaction.reaction.emoji)
        # new_page, reaction = await wait_for_reaction(new_page, page5)
        # await self.bot.say(reaction.reaction.emoji)
        # new_page, reaction = await wait_for_reaction(new_page, page6)
        # await self.bot.say(reaction.reaction.emoji)
        # new_page, reaction = await wait_for_reaction(new_page, page7)
        # await self.bot.say(reaction.reaction.emoji)
        # new_page, reaction = await wait_for_reaction(new_page, page8)
        # await self.bot.say(reaction.reaction.emoji)
        # await self.bot.say(ascii(reaction.reaction.emoji))


def setup(bot):
    bot.add_cog(Help(bot))
