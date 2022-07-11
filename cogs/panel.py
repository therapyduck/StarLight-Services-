import discord
from discord.ext import commands
from discord.commands import slash_command

from utilities.functions import acc_guild_ids as ids
from utilities.functions import get_time, main_thumbnail

from datetime import datetime
from replit import db

#db["category_ids"] = {}
# db["tickets"] = {}

questions = {
"Bot Development": ("Would you like to use slash commands?\nIf not, please specify what prefix you wanna have.", "What colour theme / scheme would you like?\nThis would be used for stuff like embeds / emojis.", "What's the name of your bot?\nThis is also for support stuff, like help messages.", "Please write a list of all commands + features you would like.", "Do you want hosting instructions in a `README.md`?"),
"Graphic Effects": ("What type of GFX would you like?", "Would you like a text, if so what?", "What theme and colours would you like?", "Do you have an image you'd like us to use?", "If you want, please choose a font (here)[https://dafont.com].", "Can you give a simple description of how it should look?"),
"Server Creation": ("What type of server would you like? Do you have any special channels?", "What theme is the server?", "Please give us a short description of the server.", "Would you like any specific bots or does it not matter?", "Would you like any self + color roles?", "Do you have a template you would like to use?", "Any additional information?"),
"Visual Effects": ("Currently no questions...",),
"Marketing": ("What do you need help with?",)}

class tickets(discord.ui.View):
	def __init__(self, client):
		super().__init__(timeout = None)
		self.client = client
		
	@discord.ui.select(
		placeholder="Choose a ticket type...",
		min_values = 1,
		max_values = 1,
		custom_id = "tickets",
		options = [
		discord.SelectOption(label = "Bot Development", emoji = "<:bot:991972296229138463>"),
		discord.SelectOption(label = "Graphic Effects", emoji = "<:gfx:991972026472480778>"),
		discord.SelectOption(label = "Server Creation", emoji = "<:server:991972077051584522>"),
		discord.SelectOption(label = "Visual Effects", emoji = "<:vfx:991972046118592542>"),
		discord.SelectOption(label = "Marketing", emoji = "<:marketing:991972097842753567>")])
	async def ticket(self, select: discord.ui.Select, interaction: discord.Interaction):
		member = interaction.user
		channel = interaction.channel
		await create_ticket(self.client, member, channel, select.values[0])

class ticket_closes(discord.ui.View):
	def __init__(self):
		super().__init__(timeout = None)

	@discord.ui.button(emoji = "<:padlock:946364939516379166>", label = "Close", style = discord.ButtonStyle.grey, custom_id = "close")
	async def close_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
		data = db["tickets"][str(interaction.channel.id)]
		del db["tickets"][str(interaction.channel.id)]
		del db["tickets"][str(data[1])]
		opened = round(datetime.strptime(data[4], "%Y-%m-%d %H:%M:%S").timestamp())
		tot = round((datetime.now().timestamp())) - opened
		channel = interaction.channel
		guild = interaction.guild
		if data[2]:
			pers = guild.get_member(data[2])
			if pers: pers = pers.mention
		else: pers = None
			
		with open("ticket_log.txt", "w") as f:
			async for m in channel.history(oldest_first = True):
				f.write(f"\n[{m.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {m.author}\n{m.content}\n")
				for i in m.embeds:
					if i.title:
						f.write(f"{i.title}\n")
					if i.description:
						f.write(f"{i.description}\n")
					for v in i.fields:
						f.write(f"{v.name}\n")
						f.write(f"{v.value}\n\n")
				
			embed = discord.Embed(title = f"{data[0]} - {data[3]}", description = f"**Opened by:** {data[3]} ({data[1]})\n**Opened:** <t:{opened}> (<t:{opened}:R>)\n**Closed:** <t:{round((datetime.now().timestamp()))}> (<t:{round((datetime.now().timestamp()))}:R>)\nOpen for a total of {get_time(tot)}.\n\n**Claimed by:** {pers}.", color = 0xeb4034, timestamp = datetime.now())
		chan = guild.get_channel(db["category_ids"]["Logging"])
		await channel.delete()
		await chan.send(embed = embed)
		with open("ticket_log.txt", "r") as f:
			await chan.send(file = discord.File(f, f"{data[3]}.txt"))
		
async def create_ticket(client, member, channel, ttype):
	if str(member.id) not in db["tickets"]:
		if member.can_send():
			data = {}
			for i in questions[ttype]:
				embed = discord.Embed(description = i, colour = 0xeb4034, timestamp = datetime.now())
				embed.set_thumbnail(url = main_thumbnail)
				msg = await member.send(embed = embed)
				data[i] = (await client.wait_for('message', check=lambda message: message.author == member and not message.guild)).content
				await msg.delete()
			guild = member.guild
			category = guild.get_channel(db["category_ids"][ttype])
			chan = await guild.create_text_channel(f"🟢-{str(member)}", category = category)
			overwrites = chan.overwrites
			overwrites[member] = discord.PermissionOverwrite(view_channel = True)
			await chan.edit(overwrites = overwrites)
		
			db["tickets"][str(chan.id)] = [ttype, member.id, None, str(member), datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
			db["tickets"][str(member.id)] = "I'm here"

			embed = discord.Embed(description = "thanks for opening a ticket lol", colour = 0xeb4034)
			embed.set_thumbnail(url = member.display_avatar.url)
			view = ticket_closes()
			await chan.send(member.mention, embed = embed)
			embed = discord.Embed(title = f"{ttype} Request", color = 0xeb4034, timestamp = datetime.now())
			for i in data:
				embed.add_field(name = i, value = data[i])
			await chan.send(embed = embed, view = view)
		else:
			await channel.send(f"Error! Your dms are closed, please turn them on. - {member.mention}", delete_after = 5)
	else:
		await channel.send(f"You already have an open ticket! {member.mention}", delete_after = 5)
		
class SetupBot(commands.Cog):
	def __init__(self, client):
		self.client = client

	@slash_command(guild_ids = ids, name = "action")
	async def ticket_action(self, ctx, action: discord.Option(
		str, "Enter an action you want to make in this channel.", choices = [
			discord.OptionChoice(name = "claim"),
			discord.OptionChoice(name = "unclaim"),
		]
	)):
		role_ids = [i.id for i in ctx.author.roles[1:]]
		if action == "claim":
			prev = db["tickets"][str(ctx.channel.id)][2]
			db["tickets"][str(ctx.channel.id)][2] = ctx.author.id
			embed = discord.Embed(title = "Channel Claimed!", description = f"**Previously claimed by:** <@{prev}> (`{prev}`)\n**Now claimed by:** {ctx.author.mention} (`{ctx.author.id}`)", color = 0xeb4034, timestamp = datetime.now())
			embed.set_thumbnail(url = main_thumbnail)
			msg = await ctx.respond(embed = embed)
			await ctx.channel.edit(name = f"🟡-{ctx.author}", topic = f"The channel is claimed by {ctx.author}.")
			
		elif action == "unclaim":
			if ctx.author.id == db["tickets"][str(ctx.channel.id)][2]:
				db["tickets"][str(ctx.channel.id)][2] = None
				await ctx.channel.edit(name = f"🟢-{ctx.author}", topic = "")
				embed = discord.Embed(title = "Channel Unclaimed!", description = "The channel has been unclaimed.", color = 0xeb4034, timestamp = datetime.now())
				embed.set_thumbnail(url = main_thumbnail)
				msg = await ctx.respond(embed = embed)
				
			else:
				embed = discord.Embed(title = "You haven't claimed this channel!", color = 0xeb4034, timestamp = datetime.now())
				embed.set_thumbnail(url = main_thumbnail)
				await ctx.respond(embed = embed)
			
	@slash_command(guild_ids = ids)
	async def setup_bot(self, ctx, ticket_panel: discord.Option(discord.TextChannel, "The text channel to have the ticket panel in.")):
		"""The command to setup the entire bot."""
		await ctx.defer()
		
		if len(db["category_ids"]) != 6:
			await ctx.respond("You must set up all category channels first! `/setup_categories`")
			return
		ticket = discord.Embed(title = "Our services", description = "Please read the description about the service you wanna order.", color = 0xeb4034, timestamp = datetime.now())
		ticket.add_field(name = "<:bot:991972296229138463> ・ Bot Development", value = "The bot department can create bots, review bots, fix bots, and all for free!\n・**Time:** Up to 4 weeks.", inline = False)
		ticket.add_field(name = "<:gfx:991972026472480778> ・ Graphic Effects", value = "The graphic effects department can create banners, logos, images and GIFs. Exactly how you would like it.\n・ **Time:** Up to a week.", inline = False)
		ticket.add_field(name = "<:server:991972077051584522> ・ Server Creation", value = "The server creation department can create a server, review one, or even fix something you don't know how to!\n・ **Time:** Up to a week.", inline = False)
		ticket.add_field(name = "<:vfx:991972046118592542> ・ Visual Effects", value = "The visual effects department can edit, create and manage videos.\n・ **Time:** Up to two weeks.", inline = False)
		ticket.add_field(name = "<:marketing:991972097842753567> ・ Marketing", value = "The marketing department can create or review your ads. They can give you suggestions on how to grow your server.\n・ **Time:** Up to three days.", inline = False)
		ticket.set_thumbnail(url = main_thumbnail)
		view = tickets(self.client)
		await ticket_panel.send(embed = ticket, view = view)

	@slash_command(guild_ids = ids)
	async def setup_categories(self, ctx, bot_channel: discord.CategoryChannel = None, server_channel: discord.CategoryChannel = None, gfx_channel: discord.CategoryChannel = None, vfx_channel: discord.CategoryChannel = None, market_channel: discord.CategoryChannel = None, ticket_logging: discord.TextChannel = None):
		"""Set the categories for tickets."""
		if bot_channel: db["category_ids"]["Bot Development"] = bot_channel.id
		if server_channel: db["category_ids"]["Server Creation"] = server_channel.id
		if gfx_channel: db["category_ids"]["Graphic Effects"] = gfx_channel.id
		if vfx_channel: db["category_ids"]["Visual Effects"] = vfx_channel.id
		if market_channel: db["category_ids"]["Marketing"] = market_channel.id
		if ticket_logging: db["category_ids"]["Logging"] = ticket_logging.id
		await ctx.respond("Categories has been updated.")

def setup(client):
    client.add_cog(SetupBot(client))