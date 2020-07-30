import discord
from discord.ext import commands
from bot_info import info
import sqlite3
import random

bot = commands.Bot(command_prefix='!')
token = info["TOKEN"]

db = sqlite3.connect("server.db")
cursor = db.cursor()

@bot.event
async def on_ready():
	cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        id INT,
        coins BIGINT,
        mini_coins INT,
        rep INT,
        lvl INT,
		xp INT,
        warn INT,
        server_id TEXT
    )""")



	for guild in bot.guilds:
		for member in guild.members:
			if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, 0, {guild.id})")
			else:
				pass

	db.commit()

	print('ok')

@bot.event
async def on_guild_join(guild):
	channel = random.choice(guild.TextChannel)
	await guild.send('Привет!!!!!!!!!!!!!')



@bot.event
async def on_member_join(member):
	if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
		cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, 0, {guild.id})")
		db.commit()
	else:
		pass

@bot.command()
async def ping(ctx):
	await ctx.send(f'{ctx.author.mention} Pong!')

h = ['прив', 'здаров']
bad_words = ['хай', 'ку']


@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	for word in h:
		if word in message.content.lower():
			await message.channel.send(f'{message.author.mention} Давно не виделись;)')

	for bad_word in bad_words:
		if bad_word in message.content.lower():
			await message.delete()
			await message.channel.send(f'{message.author.mention} Ты упомянул плохое слово!')
	await bot.process_commands(message)



@bot.command()
async def load(ctx, extensions):
    Bot.load_extension(f'cogs.{extensions}')
    await ctx.send('loaded')

@bot.command()
async def reload(ctx, extensions):
    Bot.load_extension(f'cogs.{extensions}')
    Bot.unload_extensions(f'cogs.{extensions}')
    await ctx.send('reloaded')

@bot.command()
async def unload(ctx, extensions):
    Bot.unload_extension(f'cogs.{extensions}')
    await ctx.send('unloaded')


bot.load_extension('cogs.rep')
bot.load_extension('cogs.coins')
bot.load_extension('cogs.ranked')


bot.run(token)