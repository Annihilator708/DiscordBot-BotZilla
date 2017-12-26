from discord.ext import commands
import json
import discord
import traceback
import sys
import io
try:
    from plugin.database import Database
except:
    pass

class AdminCommands:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']



    @commands.command(pass_context=True)
    async def kick(self, ctx, member:discord.Member):
        """Kicks a `Member` from the server they belong to.
        This function kicks the `Member` based on the server it belongs to,
        So you must have the proper permissions in that server."""
        if ctx.message.author.id not in self.owner_list:
            return
        await self.bot.kick(member)


    @commands.command(pass_context=True)
    async def game(self, ctx, game: str = None, *, url: str = None):
        """
        Change the bots game.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        if game is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You stupid! use `{}help game` instead'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        if not url:
            game = discord.Game(name=game, type=0)
        else:
            game = discord.Game(name=game, url=url, type=1)
        await self.bot.change_presence(game=game)

    # ===========================
    #   Module related commands
    # ===========================

    @commands.command(pass_context=True)
    async def load(self, ctx,  *, extension: str):
        """
        Load an extension.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        extension = extension.lower()
        try:
            self.bot.load_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            a = await self.bot.say("Could not load `{}` -> `{}`".format(extension, e))
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
        else:
            a = await self.bot.say("Loaded cog `plugin.{}`.".format(extension))
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def unload(self, ctx, *, extension: str):
        """
        Unload an extension.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        extension = extension.lower()
        try:
            self.bot.unload_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            a = await self.bot.say("Could not unload `{}` -> `{}`".format(extension, e))
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
        else:
            a = await self.bot.say("Unloaded `{}`.".format(extension))
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def reload(self, ctx, *, extension: str):
        """
        Reload an extension.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        extension = extension.lower()
        try:
            self.bot.unload_extension("plugin.{}".format(extension))
            self.bot.load_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            a = await self.bot.say("Could not reload `{}` -> `{}`".format(extension, e))
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
        else:
            a = await self.bot.say("Reloaded `{}`.".format(extension))
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def reloadall(self, ctx):
        """
        Reload all extensions.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        for extension in self.bot.extensions:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except Exception as e:
                a = await self.bot.say("Could not reload `{}` -> `{}`".format(extension, e))
                await self.bot.add_reaction(a, self.emojiUnicode['error'])

        a = await self.bot.say("Reloaded all.")
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, hiddewn=True)
    async def sendalldm(self, ctx, *, content: str = None):
        """
        Reload and reconnect music channels
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        if content is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may want to read **`{}help sendalldm`** for more info'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        try:
            database = Database(self.bot)
            clean_id = []
            database.cur.execute("select id from botzilla.users;")
            rows = database.cur.fetchall()
            for row in rows:
                row = str(row).replace('(', '')
                row = str(row).replace(',)', '')
                print(row)
                target = await self.bot.get_user_info('275280442884751360')
                embed = discord.Embed(title='{}:'.format('Announcement'),
                                      description='{}'.format(content),
                                      colour=0xf20006)
                a = await self.bot.send_message(target, embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        except Exception as e:
            print(e.args)


def setup(bot):
    bot.add_cog(AdminCommands(bot))