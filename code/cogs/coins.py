import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect("server.db")
cursor = db.cursor()

class Coins(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		cursor.execute(f"UPDATE users SET mini_coins = mini_coins + {10} WHERE id = {message.author.id}")
		db.commit()
		if cursor.execute(f"SELECT mini_coins FROM users WHERE id = {message.author.id}").fetchone()[0] >= 100:
			cursor.execute(f"UPDATE users SET mini_coins = {0} WHERE id = {message.author.id}")

	

	@commands.command()
	async def coins(self, ctx, member: discord.Member=None):
		emb = discord.Embed(color=0x3EF74B,
			description=f'Ваш счёт составляет **{cursor.execute(f"SELECT coins FROM users WHERE id = {member.id}").fetchone()[0]}** монет.')
		await ctx.send(embed=emb)




def setup(bot):
    bot.add_cog(Coins(bot))