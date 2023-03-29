import csv
import discord
import io
from discord.ext import commands

with open("token", "r") as f:
    TOKEN = f.read()
intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="collect")
async def export_messages(ctx):
    server = ctx.guild

    # Iterate through channels and collect messages
    with open("server_messages.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["Message", "Time", "Author", "Channel"])
        writer.writeheader()
        for channel in server.channels:
            print(f"Collecting messages from {channel.name}")
            if isinstance(channel, discord.TextChannel):
                async for message in channel.history(limit=None):
                    writer.writerow(
                        {
                            "Message": message.content,
                            "Time": message.created_at,
                            "Author": message.author.name,
                            "Channel": message.channel,
                        }
                    )

        print("Done collecting messages")
        # Send the collected messages in a CSV file
        await ctx.send(
            "Here's the CSV file of all messages:",
            file=discord.File(f),
        )


# Run the bot
bot.run(TOKEN)
