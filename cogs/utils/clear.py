import discord 
from discord.ext import commands
from expression import happy

class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def lol(self, ctx):
        await ctx.send('nice')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify an amount of messages to delete.')

def setup(client):
    client.add_cog(Test(client))