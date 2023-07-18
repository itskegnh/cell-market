from structs import *

import disnake
from disnake.ext import commands

class MarketCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @commands.slash_command(name='market', description='Inspect the market!')
    async def market(self, command_inter : disnake.ApplicationCommandInteraction):
        tab_group = TabGroup()

        @tab_group.tab(emoji='🔍')
        async def _stocks(inter : disnake.Interaction, tab : Tab):
            embed = Embed(title='Stocks')
            embed.set_thumbnail((self.bot.user.avatar or self.bot.user.default_avatar).url)

            for stock in STOCKS:
                stock.sync()
                BIN, SIN = None, None

                for offer_ref in stock.offers or []:
                    offer = Offer(offer_ref).sync()

                    if (BIN is None) or (BIN > offer.price): BIN = offer.price

                for order_ref in stock.orders or []:
                    order = Order(order_ref).sync()
                    if (SIN is None) or (SIN < order.price): SIN = order.price
                
                BIN = BIN or '-'
                SIN = SIN or '-'

                embed.add_field(name=f'{stock.emoji} `{stock.id}`', value=f'>>> **BIN**: `${millify(BIN)}`\n**SIN**: `${millify(SIN)}`', inline=True)
            
            return TabResponse(embeds=[embed])

        async def _stock(inter : disnake.Interaction, tab : Tab):
            stock = Stock(tab.id).sync()
            embed = Embed(title=f'({stock.id}) {stock.name}')
            embed.set_thumbnail(file=stock.image)

            return TabResponse(embeds=[embed])
    
        for stock in STOCKS:
            stock.sync()
            tab_group.add_tab(Tab(_stock, stock.id, emoji=stock.emoji))

        




        
        await tab_group.start(command_inter)
    
def setup(bot : commands.Bot):
    bot.add_cog(MarketCog(bot))
