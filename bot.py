import csv
import discord
import io
from discord.ext import commands

with open("token", "r") as f:
    TOKEN = f.read()
intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='export_messages')
async def export_messages(ctx):
    server = ctx.guild
    output_file = io.StringIO()
    csv_writer = csv.writer(output_file)

    # Write CSV header
    csv_writer.writerow(['channel', 'message_id', 'author', 'timestamp', 'content'])

    # Iterate through channels and collect messages
    for channel in server.channels:
        if isinstance(channel, discord.TextChannel):
            async for message in channel.history(limit=None):
                csv_writer.writerow([channel.name, message.id, message.author, message.created_at, message.content])

    # Reset the output_file cursor to the start
    output_file.seek(0)

    # Send the collected messages in a CSV file
    await ctx.send("Here's the CSV file of all messages:", file=discord.File(output_file, 'server_messages.csv'))

# Run the bot
bot.run(TOKEN)

