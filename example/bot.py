from discord.ext import commands
from discord import Embed

bot = commands.Bot(command_prefix='rpg!', description='Example Bot with discord-rpg extension')

bot.load_extension('src.RPG')

@bot.event
async def on_ready():
    bot.rpg.newItem(name='king sword', price=1000, icon='KS ', rarity=10, hidden=False)
    bot.rpg.newItem(name='Basic Loot', price=100, icon='BL ', rarity=1, hidden=False, lootbox=True, loot=['king sword', 'Basic Loot'])

@commands.check(bot.rpg.not_registered)
@bot.command()
async def reg(ctx):
    await bot.rpg.regMember(id=ctx.author.id)
    await ctx.send(f'{ctx.author.mention} **registered**')

@commands.check(bot.rpg.registered)
@bot.command()
async def me(ctx):
    await ctx.send(embed=bot.rpg.getProfileEmbed(member=ctx.author))

@commands.check(bot.rpg.registered)
@bot.command()
async def inv(ctx):
    await ctx.send(embed=bot.rpg.getInvEmbed(member=ctx.author))

@commands.check(bot.rpg.registered)
@bot.command()
async def shop(ctx):
    await ctx.send(embed=bot.rpg.getShopEmbed())

@commands.check(bot.rpg.registered)
@bot.command()
async def buy(ctx, *, item):
    await ctx.send(await bot.rpg.buyItem(item, member=ctx.author))

@commands.check(bot.rpg.registered)
@bot.command()
async def openlootbox(ctx, *, boxName):
    await ctx.send(await bot.rpg.openLootBox(boxName, member=ctx.author))

bot.run(token)