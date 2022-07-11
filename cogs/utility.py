import discord
from discord.ext import commands
from discord.commands import slash_command

from utilities.functions import acc_guild_ids as ids
from utilities.functions import get_time, main_thumbnail
from datetime import datetime

class UtilityCog(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.launch_time = datetime.now()

	@slash_command(guild_ids = ids)
	async def uptime(self, ctx):
		"""Check the bots uptime."""
		await ctx.defer()
		msg = await ctx.respond("Loading...")
		seconds = round((datetime.now() - self.launch_time).seconds)
		embed = discord.Embed(title = "The bot has been online for:", description = f"```{get_time(seconds)}```", colour = 0xF5EF92, timestamp = self.launch_time)
		embed.set_thumbnail(url = main_thumbnail)
		embed.set_footer(icon_url = main_thumbnail, text = "Started")
		await msg.edit(embed = embed, content = "")
		
def setup(client):
	client.add_cog(UtilityCog(client))