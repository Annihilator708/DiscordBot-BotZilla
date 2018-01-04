"""
Informative commands for the bot.
"""
import time
import json
import discord
from discord.ext import commands
import asyncio
import re
import random
import ddg3 as duckduckgo3
try:
    from plugin.database import Database
except:
    pass


def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)


class NoPrivateMessages(commands.CheckFailure):
    pass

def guild_only():
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessages('Hey no DMs!')
        return True
    return commands.check(predicate)


class Information:
    """
    Informative commands for the bot.
    """

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
            print('Information: Database files not found')
            pass

    # ========================
    #   Bot related commands


    @commands.command(pass_context=True)
    async def poll(self, ctx, *questions_and_choices: str):
        """
        Makes a poll quickly for your server.
        The first argument is the question and the rest are the choices.
        You can only have up to 20 choices and one question.
        Use `;` as a delimiter.
        Example: question? answerA; answer B; answerC
        """

        if str(questions_and_choices) == '()':
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='It\'s not a bad idea to read `{}help poll` first'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        try:
            question = re.search(r'(.*?)\?', str(questions_and_choices)).group(0)
            question = re.sub(r'[(|$|.|!|\'|,]', r'', str(question))
            left_over = re.search(r'\?(.*$)', str(questions_and_choices)).group(0)
            choices = re.sub(r'[(|$|.|!|\'|,|)]', r'', str(left_over))
            choices = re.sub(r'[?]', r'', str(choices))
            choices = choices.split(';')
            answers = []
            for choice in choices:
                answers.append(choice)

            if '' in answers:
                answers.remove('')

            if len(answers) < 2:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='You need atleast two answers',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return
            elif len(answers) > 21:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='You have more than 20 answers',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                return

            choices = [(to_emoji(e), v) for e, v in enumerate(answers)]

            try:
                await ctx.message.delete()
            except:
                pass
            embed = discord.Embed(title='{} asks:'.format(ctx.message.author.name),
                                  description='**{}**'.format(question),
                                  colour=0xf20006)
            for key, c in choices:
                embed.add_field(name='{} Answer:'.format(':gear:'), value='{} : {}\n'.format(key, c), inline=False)
            a = await self.bot.say(embed=embed)
            for emoji, _ in choices:
                await self.bot.add_reaction(a, emoji)

        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Don\'t forget the question..\nQuestion: did you read the `{}help poll`?'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            await asyncio.sleep(10)


    @commands.command(pass_context=True)
    async def fact(self, ctx, *, search_term: str = None):
        """
        Search for a fact!
        Use this command in combination with a subject you like
        to get a fact for that subject
        """

        if search_term is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You really should reconsider reading the **`{}help fact`**'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        search_term = search_term.lower()

        if search_term == "botzilla":
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Best bot on the market right now! \nNo need for more information!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\U0001f44c')
            return


        try:
            search_number = random.randint(0, 1)
            r = duckduckgo3.query(search_term)
            related_type = r.type
            related_text = r.related[search_number].text
            'Python (programming language), a computer programming language'

            related_related = r.related[search_number].url
            print("Type: %s \nText: %s \nSource: %s" % (related_type, related_text, related_related))
            message2user = "Type: %s \nText: %s \nSource: %s" % (related_type, related_text, related_related)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format(message2user),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            return

        except IndexError:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Nothing found...',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return


    @commands.command(pass_context=True, aliases=["oauth", "invite"])
    async def join(self, ctx):
        """
        Add BotZilla to your server!
        Gives BotZilla OAuth url. Use this to add him to your server!
        When the database restarts botzilla will automatically join voice channels
        with 'music' or 'Music' in the name.
        """

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Use the following url to add BotZilla V2 to your guild!\n**{}**'.format(
                                  discord.utils.oauth_url(self.bot.user.id)),
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """
        Check server response.
        Sends a package to the discord server.
        Calculates response time
        """
        before = time.monotonic()
        await (await self.bot.ws.ping())
        after = time.monotonic()
        ping_result = (after - before) * 1000
        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Pong :ping_pong: **{0:.0f}ms**'.format(ping_result),
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def count(self, ctx):
        """
        Give information about Botzilla.
        Count's the community, servers and more!
        """
        if self.database_file_found:
            self.database.cur.execute("select count(*) from botzilla.users;")
            rows = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            a = str(rows).replace('[(', '')
            self.total_users = a.replace(',)]', '')
            self.total_online_users = 0
            for server in self.bot.servers:
                for member in server.members:
                    if 'online' in str(member.status):
                        self.total_online_users = self.total_online_users + 1
            embed = discord.Embed(title="{}".format("Server Count"),
                                  description="We are in **{}** servers\nWe have **{}** members\nWe had a total of **{}** users\nThere are **{}** users online".format(
                                      str(len(self.bot.servers)), str(len(set(self.bot.get_all_members()))), self.total_users, self.total_online_users),
                                  color=0xf20006)
            a = await self.bot.say(embed=embed)
            self.total_online_users = 0
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        else:
            for server in self.bot.servers:
                for member in server.members:
                    if 'online' in str(member.status):
                        self.total_online_users = self.total_online_users + 1
            embed = discord.Embed(title="{}".format("Server Count"),
                                  description="We are in **{}** servers\nWe have **{}** members\nThere are **{}** users online".format(
                                      str(len(self.bot.servers)), str(len(set(self.bot.get_all_members()))), self.total_online_users),
                                  color=0xf20006)
            a = await self.bot.say(embed=embed)
            self.total_online_users = 0
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def id(self, ctx, *, username=None):
        """Shows your ID or the id of the user."""
        if username is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Your ID is:\n**{}**'.format(str(ctx.message.author.id)),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        else:
            try:
                username = username.replace('<@', '')
                username = username.replace('>', '')
                username = username.replace('!', '')
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='The ID you looking for is:\n**{}**'.format(str(username)),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            except:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Invalid username'.format(str(username)),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])


    @commands.command(pass_context=True, hidden=True)
    async def say(self, ctx, *, message=None):
        """Say something as BotZilla.
        This only works in the direct channel the command is used in.
        Secret egg ;)
        """

        if message is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Maybe you should considering using `{}help say` instead'.format(self.config['prefix']),
                                  colour=0xf20006)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format(str(message)),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def emoji(self, ctx, *, emoji : str =None):
        """
        Shows ASCII information about the emoji.
        Usefull for developers.
        """
        if emoji is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Try `{}help emoji`, That would help..'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        try:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='```asci\n{}\n```'.format(ascii(str(emoji))),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='```Python\n{}\n```'.format(e.args),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


    @commands.command(pass_context=True)
    async def blacklist(self, ctx, username=None, *, reason: str = None):
        """
        Starts a blacklist vote. Ban people from making use of BotZilla.
        5 % of your server has to agree.
        """
        if username is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Read **`{}help blacklist`** that would help..'.format(
                                      self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        elif reason is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You have to give up a reason..\nI recommend reading **`{}help blacklist`**'.format(
                                      self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        else:
            vote_policy = len(ctx.message.server.members) / 100 * 5
            username = username.replace('<@', '')
            username = username.replace('>', '')
            username = username.replace('!', '')

            try:
                name = await self.bot.get_user_info(username)
                if name.id in self.database.blacklist:
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='*`{}` already on the blacklist*'.format(name),
                                          colour=0xf20006)
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, '\U0001f605')
                    return
            except:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Invalid username'.format(str(username)),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return


            embed = discord.Embed(title='Blacklist vote started by {}:'.format(ctx.message.author.name),
                                  description='Total votes are needed: **{}**\n**2** Minutes remaining..\n\nWould you like to blacklist:\n\n**`{}`**\n\nReason:\n\n**`{}`**\n\nPeople who got blacklisted can\'t use BotZilla anymore.\nEven in other servers'.format(
                                      vote_policy, name, str(reason)),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\u2705')
            await self.bot.add_reaction(a, '\U0001f1fd')
            await asyncio.sleep(120)

            message = await self.bot.get_message(ctx.message.channel, a.id)
            total = message.reactions[0].count - 1

            if float(total) >= vote_policy:
                try:
                    reason = str(reason).replace(';', '')
                    self.database.cur.execute("INSERT INTO botzilla.blacklist (ID, server_name, reason, total_votes) VALUES ({}, '{}', '{}', {});".format(name.id, str(name), str(reason), total))
                    self.database.cur.execute("ROLLBACK;")
                    print(f'Vote blacklist approved for {username}')
                    await self.bot.delete_message(message)
                except:
                    await self.bot.delete_message(message)
                    pass
                finally:
                    embed = discord.Embed(title='Blacklist vote approved:',
                                          description='Blacklist vote has been approved for **`{}`**'.format(name),
                                          colour=0xf20006)
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, '\U0001f44b')
            else:
                embed = discord.Embed(title='Blacklist vote started by {}:'.format(ctx.message.author.name),
                                      description='Blacklist vote has been declined for **`{}`**'.format(name),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, '\u2705')

    @commands.command(pass_context=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Commands", description="Use `{}help \'Command\'` for more info over the command", colour=0xf20006)
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Annihilator708/DiscordBot-BotZilla/master/icon.png")
        embed.add_field(name="{}8ball".format(self.config['prefix']), value="8ball! Ask BotZilla Any question.", inline=True)
        embed.add_field(name="{}Joke".format(self.config['prefix']), value="Ever heard a Chuck Norris joke?", inline=True)
        embed.add_field(name="{}rule34".format(self.config['prefix']), value="Shows graphical content NSFW", inline=True)
        embed.add_field(name="{}gif".format(self.config['prefix']), value="Retrieves a random gif from a giphy search", inline=True)
        embed.add_field(name="{}poll".format(self.config['prefix']), value="Make a poll for your server", inline=True)
        embed.add_field(name="{}join".format(self.config['prefix']), value="Add BotZilla to your server!", inline=True)
        embed.add_field(name="{}count".format(self.config['prefix']), value="Count servers, members, etc etc", inline=True)
        embed.add_field(name="{}fact".format(self.config['prefix']), value="Search for a fact!", inline=True)
        embed.add_field(name="{}id".format(self.config['prefix']), value="Shows your ID or the id of the user", inline=True)
        embed.add_field(name="{}emoji".format(self.config['prefix']), value="Shows ASCII information about the emoji", inline=True)
        embed.add_field(name="{}ping".format(self.config['prefix']), value="Check server response", inline=True)
        embed.add_field(name="{}blacklist".format(self.config['prefix']), value="Global blacklist vote", inline=True)
        embed.add_field(name="{}r6s".format(self.config['prefix']), value="Shows your Rainbow Six Siege stats", inline=True)
        embed.add_field(name="{}bitcoin".format(self.config['prefix']), value="Shows current bitcoin value", inline=True)
        embed.add_field(name="{}summon".format(self.config['prefix']), value="Summons the bot to join your voice channel", inline=False)
        embed.add_field(name="{}stop".format(self.config['prefix']), value="Stops playing audio and leaves the voice channel", inline=False)
        embed.add_field(name="{}play".format(self.config['prefix']), value="Plays a song", inline=False)
        embed.add_field(name="{}pause".format(self.config['prefix']), value="Pauses the currently played song", inline=False)
        embed.add_field(name="{}resume".format(self.config['prefix']), value="Resumes the currently played song", inline=False)
        embed.add_field(name="{}np".format(self.config['prefix']), value="Shows info about the currently played song", inline=False)
        embed.add_field(name="{}skip".format(self.config['prefix']), value="Vote to skip a song. The song requester can always skip his own song", inline=False)
        embed.add_field(name="{}volume".format(self.config['prefix']), value="Sets the volume of the currently playing song", inline=False)
        embed.set_footer(text="BotZilla is built / maintained / self hosted by PuffDip\nUserdata may be stored for better experience.")
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
