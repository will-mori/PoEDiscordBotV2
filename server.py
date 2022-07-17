# William Mori

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
import asyncio
import random
from datetime import date, datetime, timezone
from itertools import groupby, chain
from global_vars import CURRENCY_DICT, URL

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CURRENCY = ["Chaos Orb", "Exalted Orb", "Divine Orb", "Awakener's Orb","Elevated Sextant","Ancient Orb",
            "Orb of Annulment", "Stacked Deck", "Awakened Sextant", "Mirror of Kalandra"]

CURRENCY_STR = ", ".join(CURRENCY_DICT.keys())

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discorcd')


@bot.command(name="woah", help="woah bro")
async def woah(ctx, mg=None):
    if ctx.author == bot.user:
        return
    print(ctx)
    print(mg)
    response = "Woah"
    await ctx.channel.send(response)


@bot.command(name="trade")
async def trade(ctx):
    query = {
        "sell": "Exalted Orb",
        "buy": "Chaos Orb",
        "limit": 5
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=query) as resp:
            print(resp)
            output = await resp.json(content_type="application/json")
            for i in output["offers"]:
                del i["item_id"]
                del i["stash_id"]
                del i["seller_account"]
                print(i)

            await ctx.channel.send("look at terminal")


def limit_handler(arg: str) -> tuple[bool, int]:
    """
    Helper function to handle converting argument
    :param arg: String to be cast to an int and used as the query limit
    :return: Tuple with first element representing if the arg is valid, the second representing the valid argument
                if the first element is false, ignore the second element
    """
    try:
        limit = int(arg)
        if limit < 1:
            return False, limit
        if limit > 200:
            limit = 200
        return True, limit
    except ValueError:
        return False, 0


def currency_handler(arg: str) -> tuple[bool, str]:
    """
    Helper function to convert currency as passed by the user to a currency as used by the endpoint
    :param arg: String to be looked up in CURRENCY_DICT
    :return: Tuple with the first element representing if the arg is a valid currency, the secong element representing
                the currency to obe used in the query, if the first element is false, ignore the second element
    """
    try:
        return True, CURRENCY_DICT[arg]
    except KeyError:
        return False, arg


def readable_listings(listings: list[dict]) -> list[str]:
    listings.sort(key=lambda x:x["conversion_rate"])
    f = lambda x: x["conversion_rate"]
    output = []
    for key, group in groupby(listings, f):
        stack = list(group)
        total_stock = 0
        max_stock = 0
        min_stock = 0
        oldest_list = ""
        newest_list = ""
        sell = stack[0]["sell"]
        buy = stack[0]["buy"]
        for listing in stack:
            total_stock += listing["stock"]
            if min_stock == 0:
                min_stock = listing["stock"]
            if listing["stock"] < min_stock:
                min_stock = listing["stock"]
            if listing["stock"] > max_stock:
                max_stock = listing["stock"]

            if oldest_list == "":
                oldest_list = listing["created_at"]
                newest_list = listing["created_at"]
            if listing["created_at"] < oldest_list:
                oldest_list = listing["created_at"]
            if listing["created_at"] > newest_list:
                newest_list = listing["created_at"]

        full_string = f"Exchange rate: 1 {sell} : {key} {buy}, or approx. {1 / key :.2f} {sell} : 1 {buy}\n" \
                      f"Total stock: {total_stock}, min listing: {min_stock}, max listing: {max_stock}\n" \
                      f"Oldest listing: {oldest_list}, Newest listing {newest_list}, Num listings {len(stack)}"
        half_string = f"Exchange rate: 1 {sell} : {key} {buy}, or approx. {1 / key :.2f} {sell} : 1 {buy}\n" \
                      f"Total stock: {total_stock}, max listing: {max_stock}, num sellers {len(stack)}" \

        output.append((key,half_string))
        # print(f"Conversion rate: 1 {sell} : {key} {buy}, or approx. {1/key :.1f} {sell} : 1 {buy}")
        # print(f"Total stock: {total_stock}, min listing: {min_stock}, max listing: {max_stock}")
        # print(f"Oldest listing: {oldest_list}, Newest listing {newest_list}")

    return [x[1] for x in sorted(output)]


async def write_to_file(filename:str, content:str) -> None:
    writer = open(f"{filename}.txt", "w")
    writer.write(content)
    writer.close()


@bot.command(name="query", help="Query a currency exchange rate.  Command can be used in the following forms:\n1."
                                "'!query {currency}' to see generic listings of the currency using the default "
                                "listing limit\n"
                                "2. '!query {currency} {currency}' to see listings of the first currency using"
                                " the second currency using the default listing limit\n"
                                "3. '!query {currency} {limit}' to see generic listings with the number of listings "
                                "limited by limit\n"
                                "4. '!query {currency} {currency} {limit}' to see listings of the first currency"
                                "to be purchased with the second currency with the number of listings limited by limit")
async def query(ctx, *args):
    start = datetime.now()
    if len(args) == 0:
        await ctx.channel.send("Must specify a currency to query from " + str(list(CURRENCY_DICT.keys())))
        return

    valid, sell = currency_handler(args[0])
    if valid is False:
        await ctx.channel.send(f"Invalid first argument {args[0]}, enter a valid currency for the first argument."
                               f"  Use !currency to see the full currency list")
        return

    http_query = {"sell": sell}

    if len(args) == 2:
        valid_buy, buy = currency_handler(args[1])
        if valid_buy is False:
            valid_limit, limit = limit_handler(args[1])
            if valid_limit is False:
                await ctx.channel.send(f"Invalid second argument {args[1]}, enter a currency, or enter an integer from"
                                       f" 1 to 200, integers over 200 will be truncated to 200.  Use !currency to see"
                                       f" the full currency list.")
                return
            else:
                http_query["limit"] = limit
        else:
            http_query["buy"] = buy

    elif len(args) == 3:
        valid_buy, buy = currency_handler(args[1])
        if valid_buy is False:
            await ctx.channel.send(f"Invalid second argument {args[1]}, enter !currency to see the full currency list")
            return
        valid_limit, limit = limit_handler(args[2])
        if valid_limit is False:
            await ctx.channel.send(f"Invalid limit {args[2]}, enter an integer from 1 to 200, integers over 200 will"
                                   f"be truncated to 200")
        http_query["buy"] = buy
        http_query["limit"] = limit

    elif len(args) > 3:
        await ctx.channel.send(f"Too many arguments, args has len {len(args)}")
        return

    print(http_query)
    listings = []
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=http_query) as resp:
            print(resp)
            output = await resp.json(content_type="application/json")
            for i in output["offers"]:
                del i["item_id"]
                del i["stash_id"]
                del i["seller_account"]
                listings.append(i)
                #print(i)

            filename = ctx.channel.last_message_id
            content = "\n".join(readable_listings(listings))
            await write_to_file(filename, content )
            await ctx.channel.send(content=f"Time taken to complete: {datetime.now() - start}",
                                   file=discord.File(f"{filename}.txt"))
            os.remove(f"{filename}.txt")


@bot.command(name="currency", help="Prints out a list of searchable currencies")
async def currency_print(ctx):
    await ctx.channel.send(CURRENCY_STR)


@bot.command(name="log-currency", help="Logs prices of ex, mirrors, woke, and ancient orbs")
async def log_currency(ctx):
    start = datetime.now()
    queries = [
        {
            "sell": "Exalted Orb",
            "buy": "Chaos Orb",
            "limit": 200
        },
        {
            "sell": "Mirror of Kalandra",
            "buy": "Exalted Orb",
            "limit": 200
        },
        {
            "sell": "Awakener's Orb",
            "buy": "Exalted Orb",
            "limit": 200
        },
        {
            "sell": "Ancient Orb",
            "buy": "Exalted Orb",
            "limit": 200
        }
    ]

    log = []
    async with aiohttp.ClientSession() as session:
        for i in queries:
            async with session.post(URL, json=i) as resp:
                output = await resp.json(content_type="application/json")
                for listing in output["offers"]:
                    del listing["item_id"]
                    del listing["stash_id"]
                    del listing["seller_account"]
                    log.append(listing)


    # TODO Add MYSQL connection



    file_name = str(date.today())
    file_time = str(datetime.now().isoformat())
    file = open(file_name, "w")
    file.write(file_time)
    for i in log:
        file.write(str(i)+",\n")
    file.close()
    await ctx.channel.send("Finished in "+str(datetime.now()-start))


@bot.command(name="down")
async def down(ctx):
    await ctx.channel.send("Function being built")
    return
    
    async with aiohttp.ClientSession() as session:
        async with session.get("http://trade.maximumsotck.net/healthcheck") as resp:
            print(resp)
            if resp.status == 200:
                await ctx.channel.send("Endpoint is up")
            else:
                await ctx.channel.send("Endpoint is unavailable")

@bot.event
async def on_error(event, *args, **kwargs):
    with open("err.log",'a') as file:
        if event == "on_message":
            file.write(f"Unhandled message: {args[0]}")
        else:
            raise


bot.run(TOKEN)


