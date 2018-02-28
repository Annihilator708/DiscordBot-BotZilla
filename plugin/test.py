import discord
from discord.ext import commands
import json
import datetime
import asyncio
import random
import aiohttp
import ast
import os
import sys
import re
try:
    from plugin.database import Database
except Exception as e:
    pass

tmp_config = json.loads(str(open('./options/config.js').read()))
config = tmp_config['config']
owner_list = config['owner-id']


class TestScripts:
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
        except Exception as e:
            print('Test: Database files not found - {}'.format(e.args))
            pass


    @commands.command(pass_context=True)
    async def crimeprofile(self, ctx, player : discord.Member = None):

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        def check_profile(self, ID):
            self.database.cur.execute(f"select * from botzilla.c_user where ID = {ID};")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if profile is None:
                return True
            else:
                return False

        if player:
            has_profile = await check_profile(self, player.id)
            print(has_profile)
        else:
            has_profile = await check_profile(self, ctx.message.author.id)
            print(has_profile)

def setup(bot):
    bot.add_cog(TestScripts(bot))
