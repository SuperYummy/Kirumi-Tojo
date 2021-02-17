# https://discord.com/oauth2/authorize?client_id=782990263391092776&scope=bot&permissions=8
import discord
from discord.ext import commands, tasks
import logging
import random
import os
from itertools import cycle


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


with open("prefix", "r", encoding="utf-8") as f:
    prefix = f.read()

client = commands.Bot(command_prefix =prefix)
client.remove_command('help')
status = cycle([f"with {len(client.guilds)} servers", "Danganronpa V2: Bloodlust"])


@client.event
async def on_ready():
    change_status.start()
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Inavlid command used.")

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='Help')
    embed.add_field(name='.ping', value='Returns Pong!', inline=False)

    await ctx.send(author, embed=embed)

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await channel.send(f'{user.name} has added {reaction.emoji} to the message: {reaction.message.content}')

@client.event
async def on_raw_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await channel.send(f'{user.name} has removed {reaction.emoji} from the message: {reaction.message.content}')




@tasks.loop(seconds=6)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



@client.command()
async def meow(ctx):
    await ctx.send("Meow!")


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['Yes', 'No', 'I don\'t know']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    await ctx.send('Please specify an amount of messages to delete.')

# Embed
@client.command()
async def displayembed(ctx):
    embed = discord.Embed(
        title = "Title",
        description = "This is a description.",
        colour = discord.Colour.blue()
    )

    embed.set_footer(text="This is a footer.")
    embed.set_image(url="https://cdn.discordapp.com/avatars/782990263391092776/eca2a90eac2952806367728a0fed41c1.png?size=128")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/782990263391092776/eca2a90eac2952806367728a0fed41c1.png?size=128")
    embed.set_author(name="Author name", 
    icon_url="https://cdn.discordapp.com/avatars/782990263391092776/eca2a90eac2952806367728a0fed41c1.png?size=128")
    embed.add_field(name="Field Name", value="Field Value", inline=False)
    embed.add_field(name="Field Name", value="Field Value", inline=True)
    embed.add_field(name="Field Name", value="Field Value", inline=True)

    await ctx.send(embed=embed)


def is_it_me(ctx):
    return ctx.author.id == 523350271313575946

@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f"Hi, I am {ctx.author}.")

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discrimator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

with open("token", "r", encoding="utf-8") as f:
    token = f.read()

client.run(token)

