# discord-rpg
discord-rpg This is an extension for discord.py with which you can create an RPG bot easily and quickly!

# Installasion & Setup
1) Download the project and unpack src in your bot folder
2) Put it in your main bot file:
```
bot.load_extension('src.RPG')
```
3) Here you go!

# About discord-rpg
# Init
 - Database Asynced system based on aiosqlite
 - Members system with balance, xp, level & inventory
 - Items system
 - Lootbox System
 - Shop System

# Functions
First thing you need to know is discord-rpg called by "bot.rpg"
Than we call functions like that:
```
bot.rpg.function(arg1, arg2, ...)
```

# Members Functions

Register new Member to system by ID/Member
```
bot.rpg.registerMember(id=None, member=None)
# id == discord member id || member == discord.Member class ( Choose one )

# alias(es) -> regMember
```

Give amount of money to member by ID/Member
```
bot.rpg.addMoney(amount, id=None, member=None)
# id == discord member id || member == discord.Member class ( Choose one )
# amount == amount of money you want to add
```

Give amount of XP to member by ID/Member
```
bot.rpg.addXp(xp, id=None, member=None)
# id == discord member id || member == discord.Member class ( Choose one )
# xp == amount of xp you want to add
```

Get the rpg member class by ID/Member
```
bot.rpg.getMember(id=None, member=None)
# id == discord member id || member == discord.Member class ( Choose one )

# Returned: member class
```

Get member's profile in embed
```
bot.rpg.getProfileEmbed(id=None, member=None, color=None)
# id == discord member id || member == discord.Member class ( Choose one )
# color == embed color (Optional)

# Returned: Member's profile embed
```

# Item Functions

Create new item
```
bot.rpg.newItem(name, price=None, icon='', rarity=1, hidden=False, lootbox=False, loot=None)
# name == item name (String)
# price == item price in the shop (Int)
# icon == item icon (Optional | String)
# rarity == item rarity level (coming soon)
# hidden == item is visible in the shop? (True/False)
# lootbox == item is a lootbox? (True/Flase)
# loot == if item is a lootbox than what user can receieve while opening? (array)
```

Give item to member by ID/Member
```
bot.rpg.giveItem(item, id=None, member=None, count=1)
# id == discord member id || member == discord.Member class ( Choose one )
# item == item name (String)
# count == how many items give? (Int)
```

Check if member has item (item_count > 0)
```
bot.rpg.hasItem(item, id=None, member=None)
# id == discord member id || member == discord.Member class ( Choose one )
# item == item name (String)

# Returned value: True/False
```

Get Member's inventory dict
```
bot.rpg.getInventory(id=None, member=None)
# id == discord member id || member == discord.Member class ( Choose one )

# alias(es) -> getInv
# Returned: Member's Inventory (Dict)
```

Get Member's inventory in embed
```
bot.rpg.getInventoryEmbed(id=None, member=None, color=None)
# id == discord member id || member == discord.Member class ( Choose one )
# color == embed color (Optional)

# alias(es) -> getInvEembed
# Returned: Member's Inventory Embed
```

# Shop Functions

Get Shop Dict
```
bot.rpg.getShop()

# Returned: Shop Dict
```

Get Shop Embed
```
bot.rpg.getShopEmbed(color=None)
# color == embed color (Optional)

# Returned: Shop Embed
```

When member buy item
```
bot.rpg.buyItem(color=None)
# item == item name (String)
# id == discord member id || member == discord.Member class ( Choose one )
# count == how many items the member buy? (Optional | Int)

# Returned: Response
```

# Lootbox Functions

Open Lootbox
```
bot.rpg.openLootBox(lootbox_item_name, id=None, member=None)
# id == discord member id || member == discord.Member class ( Choose one )
# lootbox_item_name == lootbox item name (String)

# Returned: Response
```

# Check Functions

Check if member is registered to system
```
@commands.check(bot.rpg.registered)
```

Check if member is not registered to system
```
@commands.check(bot.rpg.not_registered)
```

# Classes

# Member Class
Member class contain:
 .balance
 .xp
 .level
 .inv

# Item Class
Item class contain:
 .price
 .icon
 .rarity
 .hidden
 .lootbox
 .loot


# Changable Variables
bot.rpg.currency (As default "$")
bot.rpg.embedColor (As default 0xffc500)

# Coming Soon
 - Keys for lootboxes
