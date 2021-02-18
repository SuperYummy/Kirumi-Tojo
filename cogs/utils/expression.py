import discord

def happy(self, ctx, description):
    print('hi')
    embed = discord.Embed(
        title = "Title",
        description = "This is a description.",
        colour = discord.Colour.blue()
    )

    sprite = ['happy_1', 'happy_2']
    
    file = discord.File(f"./attachment/sprites/kirumi-tojo/{sprite}.png", filename="happy_1.png")
    embed.set_footer(text="This is a footer.")
    embed.set_image(url=f"attachment://{sprite}.png")

    await ctx.send(file=file, embed=embed)