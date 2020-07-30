import discord
from discord.ext import commands
import sqlite3
import math

db = sqlite3.connect("server.db")
cursor = db.cursor()

class Ranked(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild:
			if message.author == self.bot.user:
				return
			user = message.author
			lvl, xp = cursor.execute(f"SELECT lvl, xp FROM users WHERE id = {user.id}").fetchone()
			cursor.execute(f"UPDATE users SET xp = {xp+25} WHERE id = {user.id}")
			db.commit()
			if xp >= 500 + 100 * lvl:
				xp, lvl = 0, lvl + 1
				cursor.execute(f"UPDATE users SET xp = 0, lvl = {lvl} WHERE id = {user.id}")
				db.commit()
				await user.send(f'{message.author.mention}, Ваш уровень теперь **{lvl}**')
		else:
			pass

	@commands.command(aliases = ['lvl-leaders', 'lvl-top', 'левел-топ'])
	async def __leader_board_level(self, ctx, top: int = None):
		if top is None:
			top = 10
		elif top > len(ctx.guild.members):
			await ctx.send(f'Воу полегче! У вас нету **{top}** человек!')

		elif type(top) != int:
			await ctx.send('Аргументом может быть только **целое** число')


		emb = discord.Embed(title = f'Топ {top} сервера {ctx.guild.name} по уровню!')
		counter = 0

		for row in cursor.execute(f"SELECT name, lvl, xp FROM users WHERE server_id = {ctx.guild.id} ORDER BY rep DESC LIMIT {top}"):
			counter += 1
			emb.add_field(
				name = f'`№ {counter}` - **{row[0]}**',
				value = f'Уровень: **{row[1]}** До след. уровня: **{100 - xp}**\n--------------',
				inline = False
			)

		await ctx.send(embed=emb)




	@commands.command()
	async def my(self, ctx):
		if ctx.message.guild:
			await ctx.message.delete()
		embed= discord.Embed(title="Ваша статистика", color=0x222ECC)
		lvl, xp = cursor.execute(f"SELECT lvl, xp FROM users WHERE id={ctx.author.id}").fetchone()
		need_xp = 500 + 100 * lvl
		procentXp = round(xp / need_xp * 100)
		procent_bar = round(xp / need_xp * 20)
		progressbar = "█" * procent_bar + "░" * (20 - procent_bar)
		embed.add_field(name="xp", value=f"{procentXp}%\\100%", inline=False)
		embed.add_field(name="progressbar", value=f"{progressbar}")
		embed.add_field(name="lvl", value=f"{lvl}", inline=False)
		await ctx.author.send(embed=embed)

def setup(bot):
    bot.add_cog(Ranked(bot))