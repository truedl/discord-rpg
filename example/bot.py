from discord.ext.commands import BucketType
from asyncio import sleep as aiosleep
from discord.ext import commands
from random import randint, choice
from discord import Embed

bot = commands.Bot(command_prefix='rpg!', description='Example Bot with discord-rpg extension')

bot.load_extension('src.RPG')

crafts = {
    'Wooden Sword': {
        'needed': {'Wood': 5}
    },
    'Mechanic': {
        'needed': {'Wood': 3, 'Defense': 1}
    },
    'Gun': {
        'needed': {'Wood': 2, 'Mechanic': 2, 'Power': 1}
    }
}

@bot.event
async def on_ready():
    bot.rpg.newItem(name='Power', price=100, icon='🔥')
    bot.rpg.newItem(name='Defense', price=100, icon='🛡')
    bot.rpg.newItem(name='PDBox', price=200, icon='📦', lootbox=True, loot=['Power', 'Defense'])
    bot.rpg.newItem(name='Wooden Sword', price=0, icon='⚔🌲', hidden=True)
    bot.rpg.newItem(name='Mechanic', price=0, icon='⚙', hidden=True)
    bot.rpg.newItem(name='Gun', price=0, icon='🔫', hidden=True)
    bot.rpg.newItem(name='Wood', price=25, icon='🌲')
    bot.rpg.newItem(name='Exclusive', icon='👑', hidden=True)

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

@commands.check(bot.rpg.registered)
@bot.command()
async def craft(ctx, *, item):
    if item == 'list':
        await ctx.send(f'{ctx.author.mention}, `{", ".join([x for x in crafts])}`')
    elif item.split(' ', 1)[0] == 'details':
        if item.split(' ', 1)[1] in crafts:
            await ctx.send(f'{ctx.author.mention}, you need `{crafts[item.split(" ", 1)[1]]["needed"]}` to craft {item.split(" ", 1)[1]}')
        else:
            await ctx.send(f'{ctx.author.mention}, item not exists')
    else:
        if item in crafts:
            await ctx.send(f'{ctx.author.mention}, '+await bot.rpg.craftItem(crafts[item]['needed'], item, member=ctx.author))
        else:
            await ctx.send(f'{ctx.author.mention}, you can\'t craft this item!')

@commands.cooldown(1, 75, BucketType.user)
@commands.check(bot.rpg.registered)
@bot.command(aliases=['adv'])
async def adventure(ctx):
    await ctx.send(f'{ctx.author.mention}, you\'ve goes to adventure, you\'ll be back in 60 seconds')
    await aiosleep(60)
    _cash = randint(15, 125)
    _xp = randint(65, 325)
    _items = randint(0, 4)
    _item = choice(list(bot.rpg.items))
    if _items:
        await ctx.send(f'{ctx.author.mention}, welcome back! you\'ve earned `{_xp} XP` and also `{_cash} CASH`. Also you\'ve found `{_item}x{_items}`')
        await bot.rpg.giveItem(_item, member=ctx.author, count=_items)
    else:
        await ctx.send(f'{ctx.author.mention}, welcome back! you\'ve earned `{_xp} XP` and also `{_cash} CASH`')
    await bot.rpg.addMoney(_cash, member=ctx.author)
    await bot.rpg.addXp(_xp, member=ctx.author)

bot.run('token')