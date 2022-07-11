import discord, os
from discord.ext import commands
from utilities.host import keep_alive as runit

from cogs.panel import tickets, ticket_closes
client = commands.Bot(intents = discord.Intents().all())

@client.event
async def on_ready():
    client.add_view(tickets(client))
    client.add_view(ticket_closes())
    print(f"\n\n-------------------------------\nYou are logged in as {client.user}!")

ie = []
for i in os.listdir("./cogs"):
	if i.endswith(".py"):
		ie.append("cogs." + i[:-3])
if __name__ == '__main__':
	for ex in ie:
		client.load_extension(ex)

runit()
client.run(os.environ["token"])