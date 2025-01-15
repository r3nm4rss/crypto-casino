import interactions
import json
import cloudscraper
from interactions import listen
from interactions.api.events import Component
from interactions import Button, ButtonStyle, ComponentContext, component_callback
import random
import asyncio
import time
import datetime
requests = cloudscraper.create_scraper()

bot = interactions.Client(
token="ADD BOT TOKEN",
    default_scope=1327238773708427265,
    intents=interactions.Intents.ALL
)
betchannel = 1327256858209288262
coinflipchannel = 1327256811895525478
giveawaychannel = 1326532874186391594
depositchannel = 1327256774524272643
withdrawchannel = 1327257068314427392
coinflipchannellog = 1327239156300120064
jackpotchannel = 1327257158169133132
upgraderchannel  = 1327257208215572481
commandchannel = 
wallet_id = "YOUR APIRONE WALLET ID"
transfer_key = "APIRONE TRANSFER KEY"
ownerid = 1177627178389741568
ad_ping = "@Ads Ping"
tax = 7
withdraw_tax = 0


def dump(filename, jsondata):
    with open(filename, "w") as f:
        json.dump(jsondata, f)
    return 1
def getbalance(id):
    x = json.load(open("users.json", "r"))
    return x[str(id)]['balance']
def register(user_id):
    stats_to_add = {
        f"{user_id}": {"balance": 0}
    }
    users = json.load(open("users.json"))
    users.update(stats_to_add)
    dump("users.json", users)
    return "Done"
def genaddress():
    ad = requests.post(f"https://apirone.com/api/v2/wallets/{wallet_id}/addresses").json()
    address = ad["address"]
    return address
def add(id: str, amount: float):
    x = json.load(open("users.json", "r"))
    oldbal = x[id]['balance']
    newbal = oldbal+amount
    x[id]['balance'] = round(newbal, 2)
    x.update(x)
    dump("users.json", x)
def remove(id: str, amount: float):
    x = json.load(open("users.json", "r"))
    oldbal = x[id]['balance']
    newbal = oldbal-amount
    x[id]['balance'] = round(newbal, 2)
    x.update(x)
    dump("users.json", x)
def ltcwithdraw(amount: float, address: str):
    addresses = requests.get(f"https://apirone.com/api/v2/wallets/{wallet_id}/addresses?limit=99&offset=0&q=empty:true").json()
    addresslist = []
    c = 0
    for x in addresses['addresses']:
        addresslist.append(x['address'])
        c += 1
    add(str(ownerid), float(amount*withdraw_tax/100))    
    def cut(amount, percentage):
        cutted = (amount*percentage/100)
        return round((amount - cutted)* 100000000)
    x = requests.post(f"https://apirone.com/api/v2/wallets/{wallet_id}/transfer", json={
        "transfer-key": transfer_key,

        "destinations": [
            {
                "address": f"{address}",
                "amount": cut(amount, withdraw_tax)
            }
        ],
        "fee": "normal",
        "subtract-fee-from-amount": True
    }).json()

def isregistered(id):
    try:
        x = json.load(open("users.json", "r"))
        x[str(id)]['balance']
        return True
    except:
        return False
def convert_to_unix_time(date: datetime.datetime, days: int, hours: int, minutes: int, seconds: int) -> str:
    # Get the end date
    end_date = date + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    # Get a tuple of the date attributes
    date_tuple = (end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second)

    # Convert to unix time
    return f'<t:{int(time.mktime(datetime.datetime(*date_tuple).timetuple()))}:R>'



@listen()
async def on_ready():
    print('Bot is ready! Connected as ${bot.user.username}')
    await bot.change_presence(status=interactions.Status.ONLINE, activity=interactions.Activity(name=f"Desposit with /deposit",type=interactions.ActivityType.COMPETING))



@interactions.slash_command(
    name="balance",
    description="Get your balance",
)
async def balance(ctx):
    try:
        if isregistered(ctx.author.id) == False:
            register(str(ctx.author.id))
        getbalance(str(ctx.author.id))
        if ctx.channel_id != commandchannel:
            invalid = interactions.Embed(color=0x26d394, title="Whoopsie! Wrong Channel!", description=f"Please type this command in the <#{commandchannel}> Channel!")
            await ctx.send(embeds=invalid, ephemeral=True)
        else:        
            balance = interactions.Embed(color=0x26d394, title="Your balance")
            balance.add_field(name=f"{ctx.author.username}'s Balance", value=f"```${getbalance(ctx.author.id)}```\nUse __/deposit__ to get more balance", inline=False)
            await ctx.send(embeds=balance, ephemeral=True)

    except:
        error = interactions.Embed(color=0x26d394, title="Unexpected Error.")
        await ctx.send(embeds=error, ephemeral=True)

@interactions.slash_command(
    name="deposit",
    description="Deposit LTC",
)
async def deposit(ctx):
    try:
        if isregistered(ctx.author.id) == False:
            register(ctx.author.id)
        getbalance(str(ctx.author.id))
        if ctx.channel_id != depositchannel:
            stock = interactions.Embed(color=0x26d394, title="Whoopsie! Wrong Channel!", description=f"Please type this command in the <#{depositchannel}> Channel!")
            await ctx.send(embeds=stock, ephemeral=True)
        else:    

            address = genaddress() 
            invoice = interactions.Embed(color=0x26d394, title="Deposit")
            invoice.add_field(name='Litecoin (LTC) Address', value=f"```{address}  ```", inline=False)
            invoice.add_field(name = "Information", value="You will receive confirmation in dms.", inline=False)
            await ctx.send(embeds=invoice, ephemeral=True)
            def addrbalance(address):
                try:
                    x = requests.get(f"https://apirone.com/api/v2/wallets/{wallet_id}/addresses/{address}/balance").json()["total"] 
                    return float(x)/100000000
                except:
                    return False
            prev_balance = addrbalance(address=address)
            while True:
                balance = addrbalance(address=address)
                if str(balance) != 'False':

                    if float(balance) == prev_balance:
                        await asyncio.sleep(5)
                        continue
                    else:
                        break
                else: 
                    await asyncio.sleep(5)
                    continue


            wallet = requests.get(f"https://apirone.com/api/v2/wallets/{wallet_id}/addresses/{address}/balance").json()
            price_of_ltc = requests.get("https://api.coinbase.com/v2/prices/LTC-USD/buy").json()["data"]["amount"]
            usd = (float(wallet['total']/100000000)*float(price_of_ltc))
            confirmationembed = interactions.Embed(color=0x26d394, title="Deposit")
            confirmationembed.add_field(name='STATUS', value=f"Awaiting confirmations. ${usd}", inline=False)

            await ctx.author.send(embeds=confirmationembed)
            while True:
                try:
                    tx_hash = requests.get(f"https://apirone.com/api/v2/wallets/{wallet_id}/addresses/{address}/history?limit=10&offset=0").json()['txs'][0]['txid']

                    break
                except:
                    await asyncio.sleep(5)
                    continue
            txh = interactions.Embed(color=0x26d394, title="Click to view transaction", url=f"https://blockchair.com/en/litecoin/transaction/{tx_hash}")
            await ctx.author.send(embeds=txh)
            while True:
                try:

                    if requests.get(f"https://apirone.com/api/v2/wallets/{wallet_id}/history?addresses={address}&limit=10&offset=0").json()['items'][0]['is_confirmed'] == True:

                        break
                except:

                    pass
                await asyncio.sleep(5)

            confirmed = interactions.Embed(color=0x26d394, title="New Deposit!")
            confirmed.add_field(name = "Information",value=f"A deposit of ${round(usd,2)} has been processed.", inline=False)
            channel = bot.get_channel(depositchannel)
            await channel.send(embeds=confirmed, content=f'${round(usd,2)} deposited by <@{ctx.author.id}>')
            await ctx.author.send(embeds=confirmed) 

            add(str(ctx.author.id), round(usd,2))

    except:
        error = interactions.Embed(color=0x26d394, title="Unexpected Error.")
        await ctx.send(embeds=error, ephemeral=True)


@interactions.slash_command(
    name="withdraw",
    description="withdraw LTC",
    options=[
        interactions.SlashCommandOption(
            name="amount",
            description="USD Balance",
            type=3,  # 3 represents string type
            required=True
        ),
        interactions.SlashCommandOption(
            name="address",
            description="Your LTC address",
            type=3,  # 3 represents string type
            required=True
        ),

    ]
)
async def withdraw(ctx, amount: float, address: str):
    try:
        if isregistered(ctx.author.id) == False:
            register(ctx.author.id)
        amount = float(amount)
        getbalance(str(ctx.author.id))
        if ctx.channel_id != commandchannel:
            stock = interactions.Embed(color=0x26d394, title="Whoopsie! Wrong Channel!", description=f"Please type this command in the <#{commandchannel}> Channel!")
            await ctx.send(embeds=stock, ephemeral=True)
        else:          

            wallet = requests.get(f"https://apirone.com/api/v2/wallets/{wallet_id}/balance").json()
            price_of_ltc = requests.get("https://api.coinbase.com/v2/prices/LTC-USD/buy").json()["data"]["amount"]
            amount_in_ltc = (amount/float(price_of_ltc))

            if amount < 0.10:
                withdrawembed = interactions.Embed(color=0x26d394, title="Withdraw atleast $0.10")
                await ctx.send(embeds=withdrawembed, ephemeral=True)
            elif amount_in_ltc > float(getbalance(str(ctx.author.id))):
                withdrawembed = interactions.Embed(color=0x26d394, title="Not enough balance")
                await ctx.send(embeds=withdrawembed, ephemeral=True)
            elif float(wallet['available']/100000000) < float(amount_in_ltc):
                withdrawembed = interactions.Embed(color=0x26d394, title="Not enough bankroll")
                await ctx.send(embeds=withdrawembed, ephemeral=True)
            elif getbalance(str(ctx.author.id)) > amount:

                remove(str(ctx.author.id), amount)
                ltcwithdraw(amount_in_ltc, address)
                withdrawembed = interactions.Embed(color=0x26d394, title="Withdraw sent")
                withdrawembed.add_field(name='STATUS', value=f"```sent withdrawal of ${round(amount, 2)}```", inline=False)
                channel = bot.get_channel(withdrawchannel)
                await channel.send(embeds=withdrawembed, content=f'withdrew by <@{ctx.author.id}>')
                await ctx.send(embeds=withdrawembed, ephemeral=True)

    except:
        error = interactions.Embed(color=0x26d394, title="Unexpected Error.")
        await ctx.send(embeds=error, ephemeral=True)


@interactions.slash_command(
    name="coinflip",
    description="create a coinflip",
    options=[
        interactions.SlashCommandOption(
            name="bet",
            description="Ur bet in usd",
            type=3,  # 3 represents string type
            required=True
        )
    ]
)
async def coinflip(ctx, bet: float):
    try:
        if isregistered(ctx.author.id) == False:
            register(ctx.author.id)

        bet = float(bet)
        if bet < 0.30:
            stock = interactions.Embed(color=0xFF0000, title="Whoopsie!", description=f"Minimum bet $0.30")
            await ctx.send(embeds=stock, ephemeral=True)
            return
        def cut(amount, percentage):
            cutted = (amount*percentage/100)
            return float(amount - cutted)

        getbalance(str(ctx.author.id))
        if ctx.channel_id != betchannel:
            stock = interactions.Embed(color=0xFF0000, title="Whoopsie! Wrong Channel!", description=f"Please type this command in the <#{coinflipchannel}> Channel!")
            await ctx.send(embeds=stock, ephemeral=True)
        elif float(getbalance(str(ctx.author.id))) < bet:
            notenough = interactions.Embed(color=0xFF0000, title="Not enough balance")
            await ctx.send(embeds=notenough, ephemeral=True)
        else:
            remove(str(ctx.author.id), bet)
            rounded = round(bet,2)
            randomcustomid1 = str(random.randint(1,1000000))
            randomcustomid2 = str(random.randint(1,1000000))
            randomcustomid3 = str(random.randint(1,1000000))
            join = interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label=f"Join ${rounded}",
                custom_id=randomcustomid1,
            )
            cancel = interactions.Button(
                style=interactions.ButtonStyle.DANGER,
                label="Cancel",
                custom_id=randomcustomid2,
            )
            callbot = interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label=f"call bot",
                custom_id=randomcustomid3,
            )
            pot = bet*2
            joiner = None
            coinflip = interactions.Embed(color=0x345d9d, title="Coinflip Created")
            await ctx.send(embeds=coinflip, ephemeral=True)
            channel = bot.get_channel(coinflipchannel)


            coinflip = interactions.Embed(color=0x345d9d, title="Coinflip")
            coinflip.add_field(name=f"{ctx.user.username} Started a coinflip worth ${rounded}", value=f"**pot**\n```${rounded}```\n**Joiner**\n```{joiner}```")
            coinflipembed = await channel.send(embeds=coinflip, components=[join, cancel, callbot])
            oldid = ctx.author.id
            oldname = ctx.author.username
            async def check(component: Component) -> bool:
                if component.ctx.custom_id == randomcustomid1:

                    if oldid != component.ctx.author.id:
                        if getbalance(component.ctx.author.id) < bet:
                            notenough = interactions.Embed(color=0xFF0000, title="your balance is too small")
                            await component.ctx.send(embeds=notenough, ephemeral=True)
                        else:
                            joiner = component.ctx.author.username
                            remove(str(component.ctx.author.id), amount=bet)
                            coinflip = interactions.Embed(color=0xFFA500, title="Coinflip is rolling...")
                            coinflip.add_field(name=f"{oldname} Started a coinflip worth ${rounded}", value=f"**pot**\n```${rounded*2}```\n**Joiner**\n```{joiner}```")
                            await coinflipembed.edit(embeds=coinflip, components=[])
                            rng = random.randint(1, 100000)/100000
                            time.sleep(5)
                            await coinflipembed.edit(embeds=coinflip)
                            if rng > 0.5:
                                coinflip = interactions.Embed(color=0x008000, title="Coinflip")
                                coinflip.add_field(name=f"{oldname} Started a coinflip worth ${rounded}", value=f"**pot**\n```${rounded*2}```\n**Joiner**\n```{joiner}```\n**Winner**\n```{joiner}```")
                                coinflip.add_field(name=f"game id: ", value=f"{rng}")
                                await coinflipembed.edit(embeds=coinflip)
                                channel = bot.get_channel(coinflipchannellog)
                                await channel.send(embeds=coinflip)
                                add(str(1327238773708427265), cut(pot, tax))
                            else:
                                coinflip = interactions.Embed(color=0x008000, title="Coinflip")
                                coinflip.add_field(name=f"{oldname} Started a coinflip worth ${rounded}", value=f"**pot**\n```${rounded*2}```\n**Joiner**\n```{component.ctx.author.username}```\n**Winner**\n```{oldname}```")
                                coinflip.add_field(name=f"game id: ", value=f"{rng}")
                                channel = bot.get_channel(coinflipchannellog)
                                await channel.send(embeds=coinflip)
                                await coinflipembed.edit(embeds=coinflip)
                                add(str(oldid), cut(pot, tax))
                            cutted = (bet*tax/100)
                            add(str(ownerid), (float(cutted) * 2))
                            time.sleep(10)
                            await coinflipembed.delete()

                    else:
                        notenough = interactions.Embed(color=0xFF0000, title="Cant join your own coinflip!")
                        await component.ctx.send(embeds=notenough, ephemeral=True)
                elif component.ctx.custom_id == randomcustomid2:
                    if oldid != component.ctx.author.id:
                        notenough = interactions.Embed(color=0xFF0000, title="Not your game")
                        await component.ctx.send(embeds=notenough, ephemeral=True)
                    else:
                        await coinflipembed.delete()
                        add(str(oldid), bet)
                        canceled = interactions.Embed(color=0xFF0000, title="Canceled Game")
                        msg = await component.ctx.send(embeds=canceled, ephemeral=True)
                elif component.ctx.custom_id == randomcustomid3:
                    if oldid != component.ctx.author.id:
                        yours = interactions.Embed(color=0xFF0000, title="Not your game")
                        await component.ctx.send(embeds=yours, ephemeral=True) 
                    else:
                        joiner = "bot"
                        coinflip = interactions.Embed(color=0xFFA500, title="Coinflip is rolling...")
                        coinflip.add_field(name=f"{oldname} Started a coinflip worth ${rounded}", value=f"**pot**\n```${rounded*2}```\n**Joiner**\n```{joiner}```")
                        await coinflipembed.edit(embeds=coinflip, components=[])
                        rng = random.randint(1, 100000)/100000
                        time.sleep(5)
                        await coinflipembed.edit(embeds=coinflip)
                        if rng > 0.7:
                            coinflip = interactions.Embed(color=0x008000, title="Coinflip")
                            coinflip.add_field(name=f"{oldname} Started a coinflip worth ${rounded}", value=f"**pot**\n```${rounded*2}```\n**Joiner**\n```{joiner}```\n**Winner**\n```{joiner}```")
                            coinflip.add_field(name=f"game id", value=f"{rng}")
                            await coinflipembed.edit(embeds=coinflip)
                            channel = bot.get_channel(coinflipchannellog)
                            await channel.send(embeds=coinflip)
                            add(str(1327238773708427265), cut(pot, tax))
                        else:
                            coinflip = interactions.Embed(color=0x008000, title="Coinflip")
                            coinflip.add_field(name=f"{oldname} Started a coinflip worth ${rounded}", value=f"**pot**\n```${rounded*2}```\n**Joiner**\n```{joiner}```\n**Winner**\n```{oldname}```")
                            coinflip.add_field(name=f"game id ", value=f"it rolled {rng}")
                            channel = bot.get_channel(coinflipchannellog)
                            await channel.send(embeds=coinflip)
                            await coinflipembed.edit(embeds=coinflip)
                            add(str(oldid), cut(pot, tax))
                        cutted = (bet*tax/100)
                        add(str(ownerid), (float(cutted) * 2))
                        time.sleep(10)
                        await coinflipembed.delete()

            while True:        
                try:
                    used_component: Component = await bot.wait_for_component(components=[randomcustomid2, randomcustomid1, randomcustomid3], check=check, timeout=60)
                except TimeoutError:
                    pass


    except:
        error = interactions.Embed(color=0x345d9d, title="Unexpected Error.")
        await ctx.send(embeds=error, ephemeral=True)



@interactions.slash_command(
    name="airdrop",
    description="Create a airdrop (rain)",
    options=[
        interactions.SlashCommandOption(
            name="amount",
            description="amount in usd",
            type=3,  # 3 represents string type
            required=True
        )
    ]
)
async def airdrop(ctx, amount: float):
    try:
        if not isregistered(ctx.author.id):
            register(ctx.author.id)

        amount = float(amount)

        if amount < 5.0:
            min_amount_embed = interactions.Embed(
                color=0x26d394,
                title="Minimum Amount Required",
                description="The minimum amount for an airdrop is $5.00."
            )
            await ctx.send(embeds=[min_amount_embed], ephemeral=True)
            return
        if float(getbalance(ctx.author.id)) >= float(amount):
            coinflip = interactions.Embed(color=0x26d394, title="airdrop Created")
            await ctx.send(embeds=coinflip, ephemeral=True)
            remove(str(ctx.author.id), amount)
            airdropid = f"airdrop{random.randint(1,1000000)}"
            join = interactions.Button(
                style=interactions.ButtonStyle.BLURPLE,
                label=f"Join airdrop",
                    custom_id=airdropid,
            )
            expiration = (f"{datetime.datetime.now().minute + 1}{datetime.datetime.now().second}")
            users = []
            author = ctx.author.id
            time = convert_to_unix_time(date=datetime.datetime.now(), days=0, hours=0, minutes=1, seconds=0)
            embed = interactions.Embed(title="Airdrop")
            embed.add_field(name="Pot", value=f"```${amount}```")
            embed.add_field(name="Users", value=f"```1```")
            embed.add_field(name="Payout", value=f"```${amount} per person```")
            embed.add_field(name="Ending", value=f"{time}")
            channel = bot.get_channel(giveawaychannel)
            msg = await channel.send(embeds=embed, components=[join], content=ad_ping)
            users.append(int(ctx.author.id))
            async def joinairdrop(ctx: Component):
                if isregistered(ctx.ctx.author.id) == False:
                    register(ctx.ctx.author.id)
                if int(ctx.ctx.author.id) in users:
                    await ctx.ctx.send(f"already joined airdrop", ephemeral=True)
                    return True

                else:

                    users.append(int(ctx.ctx.author.id))
                    await ctx.ctx.send(f"Joined airdrop", ephemeral=True)
                    embed = interactions.Embed(title="Airdrop")
                    embed.add_field(name="Pot", value=f"```${amount}```")
                    embed.add_field(name="Users", value=f"```{len(users)}```")
                    embed.add_field(name="Payout", value=f"```${(amount/len(users))} per person```")
                    embed.add_field(name="Ending", value=f"{time}")
                    await msg.edit(embeds=embed, components=[join])
                    return True


            while True:
                try:
                    await bot.wait_for_component(components=join, check=joinairdrop, timeout=60)
                except TimeoutError:

                    now = (f"{datetime.datetime.now().minute}{datetime.datetime.now().second}")
                    if int(now) >= int(expiration):
                        join.disabled = True
                        embed = interactions.Embed(title="Airdrop Ended")
                        embed.add_field(name="Pot", value=f"```${amount}```")
                        embed.add_field(name="Users", value=f"```{len(users)}```")
                        embed.add_field(name="Payed out", value=f"```${(amount/len(users))} per person```")
                        await msg.edit(embeds=embed, components=[join])
                        for i in users:
                            user = bot.get_user(i)
                            await user.send(f"You got ${amount/len(users)} from <@{author}>'s airdrop")
                            add(str(i), float(amount/len(users)))
                        break
        else:
            await ctx.send(f"Not enough balance", ephemeral=True)
            return True

    except Exception as e:
        print(e)
        error = interactions.Embed(color=0x26d394, title="Unexpected Error.")
        await ctx.send(embeds=error, ephemeral=True)
@interactions.slash_command(
    name="tip",
    description="Tip a user",
    options=[
        interactions.SlashCommandOption(
            name="amount",
            description="amount in usd",
            type=3,  # 3 represents string type
            required=True
        ),
        interactions.SlashCommandOption(
            name="user",
            description="discord user",
            type=6,  # 3 represents string type
            required=True
        )
    ]
)
async def tip(ctx, amount: float, user):
    amount = float(amount)
    try:
        if amount >= 0.1:
            if isregistered(ctx.author.id) == False:
                register(ctx.author.id)
            if float(getbalance(ctx.author.id)) > float(amount):
                if isregistered(str(user.id)) == True:
                    remove(str(ctx.author.id), float(amount))
                    add(str(user.id), float(amount))
                    tip = interactions.Embed(color=0x26d394, title="Sucess!", description=f"Tipped {user.mention} ${amount}")
                    await ctx.send(embeds=tip, ephemeral=True)
                else:
                    register(str(user.id))
                    remove(str(ctx.author.id), float(amount))
                    add(str(user.id), float(amount))
                    tip = interactions.Embed(color=0x26d394, title="Sucess!", description=f"Tipped {user.mention} ${amount}")

        else:
            error = interactions.Embed(color=0x26d394, title="Tip atleast 0.1!")
            await ctx.send(embeds=error, ephemeral=True)
    except:
        error = interactions.Embed(color=0x26d394, title="Unexpected Error.")
        await ctx.send(embeds=error, ephemeral=True)           
@interactions.slash_command(
    name="upgrader",
    description="Play Upgrader (tokens)",
    options=[
        interactions.SlashCommandOption(
            name="bet",
            description="Your bet in USD",
            type=3,  # 3 représente un type de chaîne
            required=True,
        ),
    ],
)
async def jackpot(ctx, bet: str):
    bet = float(bet.replace(",", "."))
    try:
        if not isregistered(ctx.author.id):
            register(str(ctx.author.id))

        getbalance(str(ctx.author.id))

        if ctx.channel_id != jackpotchannel:
            stock = interactions.Embed(
                color=0x26d394,
                title="Whoopsie! Wrong Channel!",
                description=f"Please type this command in the <#{jackpotchannel}> Channel!",
            )
            await ctx.send(embeds=stock, ephemeral=True)

        elif float(getbalance(str(ctx.author.id))) < bet:
            notenough = interactions.Embed(
                color=0x26d394, title="Not enough balance"
            )
            await ctx.send(embeds=notenough, ephemeral=True)

        elif bet < 0.10:  # Pari minimum de 10 cents
            min_bet = interactions.Embed(
                color=0x26d394,
                title="Minimum Bet",
                description="The minimum bet is $0.10. Please try again.",
            )
            await ctx.send(embeds=min_bet, ephemeral=True)

        else:
            remove(str(ctx.author.id), bet)
            rounded = round(bet, 2)
            jackpot_result = random.randint(1, 1000)  # Ajuster la probabilité ici
            win_chance = 0.0005  # Chance de 5% de gagner (ajuster si nécessaire)

            if jackpot_result <= win_chance * 1000:
                # Jackpot gagné!
                win_amount = bet * 0.50  # Ajuster le multiplicateur pour le jackpot
                add(str(ctx.author.id), win_amount)
                jackpot = interactions.Embed(
                    color=0x26d394, title="JACKPOT!"
                )
                jackpot.add_field(
                    name=f"You won {win_amount} tokens!",
                    value=f"Congratulations, you won this upgrade! Your new balance is {getbalance(str(ctx.author.id))} tokens.",
                    inline=False,
                )
                await ctx.send(embeds=jackpot, ephemeral=True)

                # Envoyer le log dans le canal d'upgrade
                channel = ctx.client.get_channel(upgraderchannel)
                log_embed = interactions.Embed(
                    color=0x26d394,
                    title=f"Upgrade Log for {ctx.author.username}",
                    description=f"Bet: {bet} tokens\nWon: {win_amount} tokens\nNew Balance: {getbalance(str(ctx.author.id))}"
                )
                await channel.send(embeds=log_embed)

            else:
                # Perdu
                jackpot = interactions.Embed(
                    color=0x26d394, title="You didn't win this time!"
                )
                jackpot.add_field(
                    name=f"You lost your {bet} tokens.",
                    value=f"Better luck next time! Your new balance is {getbalance(str(ctx.author.id))} tokens.",
                    inline=False,
                )
                await ctx.send(embeds=jackpot, ephemeral=True)

                # Envoyer le log dans le canal d'upgrade
                channel = ctx.client.get_channel(upgraderchannel)
                log_embed = interactions.Embed(
                    color=0xFF0000,
                    title=f"Upgrade Log for {ctx.author.username}",
                    description=f"Bet: {bet} tokens\nLost: {bet} tokens\nNew Balance: {getbalance(str(ctx.author.id))}"
                )
                await channel.send(embeds=log_embed)

    except Exception as e:
        print(f"Error: {e}")
        error_embed = interactions.Embed(
            color=0x26d394,
            title="An error occurred",
            description="Something went wrong. Please try again later."
        )
        await ctx.send(embeds=error_embed, ephemeral=True)

    except Exception as e:
        print(f"Error: {e}")
        error_embed = interactions.Embed(
            color=0x26d394,
            title="An error occurred",
            description="Something went wrong. Please try again later."
        )
        await ctx.send(embeds=error_embed, ephemeral=True)
    except Exception as e:
        withdrawembed = interactions.Embed(
            color=0x26d394,
            title="Not registered",
            description="Please use another command first!",
        )
        await ctx.send(embeds=withdrawembed, ephemeral=True)
bot.start()
