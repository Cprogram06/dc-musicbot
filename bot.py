import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
from cogs.music_cog import MusicBot

# Load environment variables
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Set up bot with intents and prefix
intents = nextcord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="/.", intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    print("Connected to the following servers:")
    for guild in client.guilds:
        print(f" - {guild.name}")
    print(f"Command prefix: {client.command_prefix}")

    # Set the bot's status
    await client.change_presence(
        activity=nextcord.Game(name="Type '/.help' to see the list of commands 😊"),  # Change activity type and name here
        status=nextcord.Status.online  # Can be nextcord.Status.online, nextcord.Status.idle, nextcord.Status.dnd, nextcord.Status.invisible
    )

# Add the MusicBot Cog to the bot
client.add_cog(MusicBot(client))

# Run the bot
client.run(DISCORD_BOT_TOKEN)
