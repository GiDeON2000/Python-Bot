import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect("server.db")
cursor = db.cursor()

class Rep(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases = ['+реп', '+rep'])
	async def __plus_reputation(self, ctx, member: discord.Member=None):
		if not member:
			await ctx.message.delete()
			await ctx.send(f'{ctx.author.mention} Укажите кому желаете выдать репутацию!', delete_after = 2)

		else:
			cursor.execute(f"UPDATE users SET rep = rep + {1} WHERE id = {member.id}")
			db.commit()
			emb = discord.Embed(color=0xFF00A8,
				description=f'{ctx.author.mention} Выдал репутацию {member.mention}, теперь у {member.mention} **{cursor.execute(f"SELECT rep FROM users WHERE id = {member.id}").fetchone()[0]}** репутации')
			await ctx.send(embed=emb)

	@commands.command(aliases = ['rep-liaders', 'реп-лидеры'])
	async def __reputation_leaderboard(self, ctx):
		emb = discord.Embed(title = 'Топ 10 сервера по репутации!', color = 0x7EFF00)
		counter = 0
		for row in cursor.execute(f"SELECT name, rep FROM users WHERE server_id = {ctx.guild.id} ORDER BY rep DESC LIMIT 10"):
			counter += 1
			emb.add_field(
				name = f'`№ {counter}` - **{row[0]}**',
				value = f'Репутации: **{row[1]}**\n--------------',
				inline = False
			)

		await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Rep(bot))