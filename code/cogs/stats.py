from discord.ext import commands
import discord
import asyncio


class ServerInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.server())

    async def server(self):
        await self.bot.wait_until_ready()

        while True:
            try:
                mrs = self.bot.get_guild(737310156907610160).members
                channel = self.bot.get_channel(737753312648101888)
                message = await channel.fetch_message(689509163818287156)
                online = len(list(filter(lambda x: x.status == discord.Status.online, mrs)))
                offline = len(list(filter(lambda x: x.status == discord.Status.offline, mrs)))
                idle = len(list(filter(lambda x: x.status == discord.Status.idle, mrs)))
                dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, mrs)))
                emb = discord.Embed(description="Статус сервера:")
                emb.add_field(name='Участники:', value=f":online:Online: {online}\n"
                                                       f":offline:Offline: {offline}\n"
                                                       f":not_active:Idle: {idle}\n"
                                                       f":not_disturb:Dnd: {dnd}")
                await asyncio.sleep(30)
                await message.edit(embed=emb)
            except Exception:
                break


def setup(bot):
    bot.add_cog(ServerInfoCog(bot))