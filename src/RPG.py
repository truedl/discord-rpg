from random import randint, choice
from discord import Embed
import aiosqlite

class Database:
    """ Database Class """

    def __init__(self, file):
        self.file = file
    
    async def query(self, sql):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(sql)
            await db.commit()
    
    async def fetch(self, sql):
        async with aiosqlite.connect(self.file) as db:
            cursor = await db.execute(sql)
            rows = await cursor.fetchall()
            await cursor.close()
            return rows

class Item:
    """ Item Class """

    def __init__(self, price, icon, rarity, hidden, lootbox, loot):
        self.price = price # item price
        self.icon = icon # item icon (emoji/other)
        self.rarity = rarity # rarity level from 1 to 10
        self.hidden = hidden # item hidden
        self.lootbox = lootbox # if item is lootbox
        self.loot = loot # array of items the lootbox can give

class Member:
    """ Member Class """

    def __init__(self, balance, xp, level, inventory):
        self.balance = balance # player balance
        self.xp = xp # player xp
        self.level = level # player level
        self.inv = inventory # player inventory

class RPG:
    def __init__(self, bot):
        self.ItemClass = Item
        self.MemberClass = Member
        self.EmbedFunction = self.createEmbed
        self.db = Database(r'src\db\main.db')
        self.me = bot
        self.embedColor = 0xffc500
        self.regMember = self.registerMember
        self.getInv = self.getInventory
        self.getInvEmbed = self.getInventoryEmbed
        bot.loop.create_task(self.setup())
    
    async def setup(self):
        """ Load RPG Members on Startup & Setup Stuff """

        await self.me.wait_until_ready()

        self.me.rpg.currency = '$'
        self.me.rpg.items = {}
        self.me.rpg.members = {}

        result = await self.db.fetch(f'SELECT * FROM members')
        for id, bal, xp, lvl, inv in result:
            self.me.rpg.members[id] = self.MemberClass(bal, xp, lvl, self.parseInv(inv))

        print('RPG Members Loaded')
    
    def newItem(self, name, price=None, icon='', rarity=1, hidden=False, lootbox=False, loot=None):
        """ Apply new item to RPG System """
        
        self.me.rpg.items[name] = self.ItemClass(price, icon, rarity, hidden, lootbox, loot)
    
    async def giveItem(self, item, id=None, member=None, count=1):
        """ Give Item """

        if not id and not member:
            print('[RPG] Can\'t give item! I\'m not find id / member arguments')
        elif not id:
            try:
                self.me.rpg.members[member.id].inv[item] += count
            except:
                self.me.rpg.members[member.id].inv[item] = count
            await self.db.query(f'UPDATE members SET inv="{self.reParseInv(self.me.rpg.members[member.id].inv)}" WHERE id="{member.id}"')
        else:
            try:
                self.me.rpg.members[id].inv[item] += count
            except:
                self.me.rpg.members[id].inv[item] = count
            await self.db.query(f'UPDATE members SET inv="{self.reParseInv(self.me.rpg.members[id].inv)}" WHERE id="{id}"')        
    
    def parseInv(self, inv, _dict={}):
        """ Parse Inventory String to Dict """

        for x in [x.split(':') for x in inv.split(';')]:
            if x[0]:
                _dict[x[0]] = int(x[1])
        return _dict
    
    def hasItem(self, item, id=None, member=None):
        """ Check if member has item by ID/Member """
        
        if not id and not member:
            print('[RPG] Can\'t getInventory! I\'m not find id / member arguments')
        elif not id:
            if item in self.me.rpg.members[member.id].inv:
                if self.me.rpg.members[member.id].inv[item] > 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            if item in self.me.rpg.members[id].inv:
                if self.me.rpg.members[id].inv[item] > 0:
                    return True
                else:
                    return False
            else:
                return False
    
    async def buyItem(self, item, id=None, member=None, count=1):
        if item in self.me.rpg.items:
            if not id and not member:
                print('[RPG] Can\'t memberBuyItem! I\'m not find id / member arguments')
                return 'Error Occured'
            elif not id:
                if self.me.rpg.members[member.id].balance >= self.me.rpg.items[item].price*count:
                    await self.addMoney(-self.me.rpg.items[item].price*count, member=member)
                    await self.giveItem(item, member=member, count=count)
                    return f'You bought `{item}` for `{self.me.rpg.items[item].price*count}{self.me.rpg.currency}`'
                else:
                    return f'You need `{self.me.rpg.items[item].price*count}{self.me.rpg.currency}` to buy `{item}`'
            else:
                if self.me.rpg.members[id].balance >= self.me.rpg.items[item].price*count:
                    self.addMoney(-self.me.rpg.items[item].price*count, member=member)
                    self.giveItem(item, member=member, count=count)
                    return f'You bought `{item}` for `{self.me.rpg.items[item].price*count}{self.me.rpg.currency}`'
                else:
                    return f'You need `{self.me.rpg.items[item].price*count}{self.me.rpg.currency}` to buy `{item}`'
        else:
            return f'"{item}" item not found'

    def getInventory(self, id=None, member=None):
        """ Get member's Inventory Dict """

        if not id and not member:
            print('[RPG] Can\'t getInventory! I\'m not find id / member arguments')
        elif not id:
            return self.me.rpg.members[member.id].inv
        else:
            return self.me.rpg.members[id].inv
    
    def getShop(self):
        """ Get Shop Dict """

        shop_dict = {}
        for x in self.me.rpg.items:
            if self.me.rpg.items[x].hidden != True:
                shop_dict[x] = self.me.rpg.items[x].price
        return shop_dict
    
    def createEmbed(self, author, member, title, color):
        """ Basic Embed builder for RPG System """

        if not color:
            emb = Embed(color=self.embedColor)
        else:
            emb = Embed(color=color)

        emb.set_author(name=f'{member.name}\'s {title}', icon_url=member.avatar_url)
        emb.set_footer(text=f'Requested by {author}', icon_url=author.avatar_url)
        return emb
    
    def getShopEmbed(self, color=None):
        """ Get Shop in Embed """

        if not color:
            emb = Embed(title='Shop', color=self.embedColor)
        else:
            emb = Embed(title='Shop', color=color)
        for x in self.me.rpg.items:
            if self.me.rpg.items[x].hidden != True:
                emb.add_field(name=f'{self.me.rpg.items[x].icon}{x}', value=f'**Price: `{self.me.rpg.items[x].price}{self.me.rpg.currency}`**')
        return emb

    def getProfileEmbed(self, id=None, member=None, color=None):
        """ Get member's Profile in Embed """

        if not id and not member:
            print('[RPG] Can\'t getProfileEmbed! I\'m not find id / member arguments')
        elif not id:
            emb = self.EmbedFunction(member, member, 'Profile', color)
            emb.add_field(name='Level', value=self.me.rpg.members[member.id].level)
            emb.add_field(name='XP', value=self.xpString(member=member))
            emb.add_field(name='Balance', value=self.me.rpg.members[member.id].balance)
            return emb
        else:
            emb = self.EmbedFunction(self.me.get_user(id), self.me.get_user(id), 'Profile', color)
            emb.add_field(name='Level', value=self.me.rpg.members[id].level)
            emb.add_field(name='XP', value=self.xpString(id=id))
            emb.add_field(name='Balance', value=self.me.rpg.members[id].balance)
            return emb

    def getInventoryEmbed(self, id=None, member=None, color=None):
        """ Get member's Inventory in Embed """

        if not id and not member:
            print('[RPG] Can\'t getInventoryEmbed! I\'m not find id / member arguments')
        elif not id:
            emb = self.EmbedFunction(member, member, 'Inventory', color)
            for x in self.me.rpg.members[member.id].inv:
                emb.add_field(name=f'{x}', value=f'{self.me.rpg.items[x].icon}{self.me.rpg.members[member.id].inv[x]}')
            return emb
        else:
            emb = self.EmbedFunction(self.me.get_user(id), self.me.get_user(id), 'Inventory', color)
            for x in self.me.rpg.members[id].inv:
                emb.add_field(name=f'{x}', value=f'{self.me.rpg.items[x].icon}{self.me.rpg.members[id].inv[x]}')
            return emb
    
    def reParseInv(self, inv_dict, _str=''):
        """ Parse Inventory Dict to String """
        for x in inv_dict:
            _str += f'{x}:{inv_dict[x]};'
        return _str
    
    def getMember(self, id=None, member=None):
        """ Get Member Class By ID/Member """

        if not id and not member:
            print('[RPG] Can\'t process getMember! I\'m not find id / member arguments')
        elif not id:
            return self.me.rpg.members[member.id]
        else:
            return self.me.rpg.members[id]
    
    def xpString(self, id=None, member=None):
        """ Return XP String by ID/Member """

        if not id and not member:
            print('[RPG] Can\'t process xpString! I\'m not find id / member arguments')
        elif not id:
            return f'{self.me.rpg.members[member.id].xp}/{100+self.me.rpg.members[member.id].level*20}'
        else:
            return f'{self.me.rpg.members[id].xp}/{100+self.me.rpg.members[id].level*20}'

    def xpReachNextLvl(self, id=None, member=None):
        """ Check how many xp member need to get next level by ID/Member """

        if not id and not member:
            print('[RPG] Can\'t process xpReachNextLvl! I\'m not find id / member arguments')
        elif not id:
            return 100+self.me.rpg.members[member.id].level*20
        else:
            return 100+self.me.rpg.members[id].level*20
    
    async def addXp(self, xp, id=None, member=None):
        """ Add XP to member by ID/Member """

        if not id and not member:
            print('[RPG] Can\'t process addXp! I\'m not find id / member arguments')
        elif not id:
            self.me.rpg.members[member.id].xp += xp
            if self.me.rpg.members[member.id].xp >= self.xpReachNextLvl(id=member.id):
                self.me.rpg.members[member.id].xp = 0
                self.me.rpg.members[member.id].level += 1
                await self.db.query(f'UPDATE members SET xp="{self.me.rpg.members[member.id].xp}", level="{self.me.rpg.members[member.id].level}" WHERE id="{member.id}"')
            else:
                await self.db.query(f'UPDATE members SET xp="{self.me.rpg.members[member.id].xp}" WHERE id="{member.id}"')
        else:
            self.me.rpg.members[id].xp += xp
            if self.me.rpg.members[id].xp >= self.xpReachNextLvl(id=id):
                self.me.rpg.members[id] = 0
                self.me.rpg.members[id].level += 1
                await self.db.query(f'UPDATE members SET xp="{self.me.rpg.members[id].xp}", level="{self.me.rpg.members[id].level}" WHERE id="{id}"')
            else:
                await self.db.query(f'UPDATE members SET xp="{self.me.rpg.members[id].xp}" WHERE id="{id}"')

    async def addMoney(self, amount, id=None, member=None):
        """ Add Money to member by ID/Member """

        if not id and not member:
            print('[RPG] Can\'t process addMoney! I\'m not find id / member arguments')
        elif not id:
            self.me.rpg.members[member.id].balance += amount
            await self.db.query(f'UPDATE members SET balance="{self.me.rpg.members[member.id].balance}" WHERE id="{member.id}"')
        else:
            self.me.rpg.members[id].balance += amount
            await self.db.query(f'UPDATE members SET balance="{self.me.rpg.members[id].balance}" WHERE id="{id}"')
    
    async def openLootBox(self, lootbox_item_name, key_required=False, key_item_name=None, id=None, member=None):
        """ Open Loot Box Function - return == response """

        if lootbox_item_name in self.me.rpg.items:
            if self.me.rpg.items[lootbox_item_name].lootbox:
                if not id and not member:
                    print('[RPG] Can\'t process openLootBox! I\'m not find id / member arguments')
                elif not id:
                    if self.hasItem(lootbox_item_name, member=member):
                        await self.giveItem(lootbox_item_name, member=member, count=-1)
                        gi = choice(self.me.rpg.items[lootbox_item_name].loot)
                        gc = randint(1, 4)
                        await self.giveItem(gi, member=member, count=gc)
                        return f'You opened `{lootbox_item_name}` lootbox and received `{gi} x{gc}`!'
                    else:
                        return 'You don\'t have lootbox in your inventory!'
                else:
                    if self.hasItem(lootbox_item_name, id=id):
                        await self.giveItem(lootbox_item_name, id=id, count=-1)
                        gi = choice(self.me.rpg.items[lootbox_item_name].loot)
                        gc = randint(1, 4)
                        await self.giveItem(gi, id=id, count=gc)
                        return f'You opened `{lootbox_item_name}` lootbox and received `{gi} x{gc}`!'
                    else:
                        return 'You don\'t have lootbox in your inventory!'
            else:
                return f'"{lootbox_item_name}" item is not a lootbox!'
        else:
            return f'"{lootbox_item_name}" item is not found'

    async def registerMember(self, id=None, member=None):
        """ Register a member to RPG System """

        if not id and not member:
            print('[RPG] Can\'t register new member! I\'m not find id / member arguments')
        elif not id:
            self.me.rpg.members[member.id] = self.MemberClass(0, 0, 0, self.parseInv(';'))
            await self.db.query(f'INSERT INTO members (id, balance, xp, level, inv) VALUES ("{member.id}", "0", "0", "0", ";")')
        else:
            self.me.rpg.members[id] = self.MemberClass()
            await self.db.query(f'INSERT INTO members (id, balance, xp, level, inv) VALUES ("{id}", "0", "0", "0", ";")')
    
    def registered(self, ctx):
        """ (Check Function) Check if user is registered to RPG System """

        return ctx.author.id in self.me.rpg.members
    
    def not_registered(self, ctx):
        """ (Check Function) Check if user is not registered to RPG System """

        return not ctx.author.id in self.me.rpg.members

def setup(bot):
    bot.rpg = RPG(bot)