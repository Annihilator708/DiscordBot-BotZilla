import discord
from discord.ext import commands
import json
try:
    from plugin.database import Database
except:
    pass


tmp_config = json.loads(str(open('./options/config.js').read()))
config = tmp_config['config']
owner_list = config['owner-id']


class Help:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']
        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except:
            print('Help: Database files not found')
            pass

    @commands.command(pass_context=True, hidden=True)
    async def t(self, ctx, command: str = None):
        """
        Show this message
        """

        self.database.cur.execute("select name from botzilla.help where cog = 'Games';")
        Games_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Games_commands = []
        for i in Games_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            Games_commands.append(i)
        Games_name = "\n".join(Games_commands)
        Games_name = Games_name + '\n'

        self.database.cur.execute("select name from botzilla.help where cog = 'GameStats';")
        GameStats_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        GameStats_commands = []
        for i in GameStats_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            GameStats_commands.append(i)
        GameStats_name = "\n".join(GameStats_commands)
        GameStats_name = GameStats_name + '\n'

        self.database.cur.execute("select name from botzilla.help where cog = 'Fun';")
        Fun_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Fun_commands = []
        for i in Fun_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            Fun_commands.append(i)
        Fun_name = "\n".join(Fun_commands)
        Fun_name = Fun_name + '\n'

        self.database.cur.execute("select name from botzilla.help where cog = 'Information';")
        Information_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Information_commands = []
        for i in Information_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            Information_commands.append(i)
        Information_name = "\n".join(Information_commands)
        Information_name = Information_name + '\n'

        self.database.cur.execute("select name from botzilla.help where cog = 'Music';")
        Music_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Music_commands = []
        for i in Music_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            Music_commands.append(i)
        Music_name = "\n".join(Music_commands)
        Music_name = Music_name + '\n'

        self.database.cur.execute("select name from botzilla.help where cog = 'Utils';")
        Utils_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Utils_commands = []
        for i in Utils_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            Utils_commands.append(i)
        Utils_name = "\n".join(Utils_commands)
        Utils_name = Utils_name + '\n'

        self.database.cur.execute("select name from botzilla.help where cog = 'Images';")
        Images_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Images_commands = []
        for i in Images_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            Images_commands.append(i)
        Images_name = "\n".join(Images_commands)
        Images_name = Images_name + '\n'

        self.database.cur.execute("select name from botzilla.help where cog = 'Exchange';")
        Exchange_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Exchange_commands = []
        for i in Exchange_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            Exchange_commands.append(i)
        Exchange_name = "\n".join(Exchange_commands)
        Exchange_name = Exchange_name + '\n'

        if ctx.message.author.id in self.owner_list:
            self.database.cur.execute("select name from botzilla.help where cog = 'Admin';")
            Admin_cog = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            Admin_commands = []
            for i in Utils_cog:
                i = '`{}{}`'.format(self.config['prefix'], i[0])
                Admin_commands.append(i)
            Admin_name = "\n".join(Admin_commands)
            Admin_name = Admin_name + '\n'

        embed = discord.Embed(title="Help for {}:".format(ctx.message.author.name),
                              color=0xf20006)


        embed.add_field(name='Games', value=Games_name, inline=True)
        embed.add_field(name='GameStats', value=GameStats_name, inline=True)
        embed.add_field(name='Fun', value=Fun_name, inline=True)
        embed.set_image(url='https://github.com/Annihilator708/DiscordBot-BotZilla/blob/master/hl.png')
        embed.add_field(name='Information', value=Information_name, inline=True)
        embed.add_field(name='Music', value=Music_name, inline=True)
        embed.add_field(name='Utils', value=Utils_name, inline=True)
        embed.set_image(url='https://github.com/Annihilator708/DiscordBot-BotZilla/blob/master/hl.png')
        embed.add_field(name='Images', value=Images_name, inline=True)
        embed.add_field(name='Exchange', value=Exchange_name, inline=True)
        if ctx.message.author.id in self.owner_list:
            embed.add_field(name='Admin', value=Admin_name, inline=True)

        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Help(bot))