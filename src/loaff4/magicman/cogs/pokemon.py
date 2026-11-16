import discord
from discord.ext import commands

from fetching import Fetching
from data import Data

import random
import math

class Pokemon(commands.Cog):
    API_URL = "https://api.tcgdex.net/v2/en"

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="pgamba")
    async def p_gamba(self, ctx, arg=""):
        await Data.register_user(ctx.message.author.id)
        data = Fetching.get(f"{self.API_URL}/cards?name={arg}")

        if data == None or len(data) == 0:
            await ctx.send("Could not find any cards")
            return

        all_cards = None
       
        all_cards = [card for card in data if "image" in card]

        card_simple = random.choice(all_cards)
        print(card_simple["id"])
        card = Fetching.get(f"{self.API_URL}/cards/{card_simple["id"]}")

        value_eur = self.get_card_value(card)
        value_usd = Fetching.convert_currency(value_eur, "eur", "usd")
        value_rounded = math.floor(round(value_usd, 2)*100)/100
        print(value_rounded)

        user_balance = await Data.get_value("balance", "users", "id", ctx.message.author.id)
        await Data.set_value("balance", "users", "id", ctx.message.author.id, math.floor((user_balance+value_rounded)*100)/100)

        print(card.get("name"))
        embed = discord.Embed(
            title = card.get("name"),
            color = discord.Color.red()
        )
        image_url = f"{card.get("image")}/low.png"
        embed.set_image(url=image_url)

        print(image_url)
        await ctx.send(embed=embed)



    @commands.command(name="pbal")
    async def p_bal(self, ctx):
        user_id = ctx.message.author.id
        balance = await Data.get_value("balance", "users", "id", user_id)
        await ctx.send(balance)


    def get_card_value(self, card_json):
        pricing = card_json.get("pricing") or {}
        cardmarket = pricing.get("cardmarket") or {}
        return cardmarket.get("avg", 0.0)
        
    
    
async def setup(bot):
    await bot.add_cog(Pokemon(bot))