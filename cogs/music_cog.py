import nextcord
from nextcord.ext import commands
import yt_dlp as youtube_dl
import re
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from scripts.get_playlist_data import get_playlist_items
import os
from dotenv import load_dotenv
import random 

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

# Set up Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, 
    client_secret=SPOTIPY_CLIENT_SECRET
))

# Set up YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# FFmpeg and yt-dlp options
FFMPEG_OPTIONS = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}


class MusicBot(commands.Cog):
    """
    A Discord bot Cog for managing music playback using YouTube and Spotify links.
    """

    def __init__(self, client: commands.Bot):
        """
        Initialize the music bot.

        Args:
            client (commands.Bot): The Discord bot instance.
        """
        self.client = client
        self.queue = []  # Queue to manage songs

    @commands.command(name="play", aliases=['p'], help="Play music using a YouTube link or search text")
    async def play(self, ctx: commands.Context, *, search: str):
        """
        Play a song or add it to the queue based on a YouTube search or link.

        Args:
            ctx (commands.Context): The context of the command.
            search (str): The search text or YouTube link.
        """
        if not ctx.author.voice:
            return await ctx.send("You need to be in a voice channel to play music.")

        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await voice_channel.connect()

        async with ctx.typing():
            try:
                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(f"ytsearch:{search}", download=False)
                    if 'entries' in info and len(info['entries']) > 0:
                        info = info['entries'][0]
                        url = info['url']
                        title = info['title']
                        self.queue.append((url, title))
                        await ctx.send(f'Added **{title}** to the queue.')
                        if not ctx.voice_client.is_playing():
                            await self.play_next(ctx)
                    else:
                        await ctx.send("No results found for your search.")
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")

    @commands.command(name="playlist", aliases=['pl', 'l'], help="Add all videos from a YouTube or Spotify playlist to the queue")
    async def playlist(self, ctx: commands.Context, url: str):
        """
        Add songs from a YouTube or Spotify playlist to the queue.

        Args:
            ctx (commands.Context): The context of the command.
            url (str): The playlist URL.
        """
        if not ctx.author.voice:
            return await ctx.send("You need to be in a voice channel to add music.")

        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await voice_channel.connect()

        await ctx.send(f'Moki is searching for the discs, please wait. It may lag if the list is too long.')
        async with ctx.typing():
            try:
                if "youtube.com/" in url:
                    await self.add_youtube_playlist(ctx, url)
                elif "spotify.com/playlist" in url:
                    await self.add_spotify_playlist(ctx, url)
                if not ctx.voice_client.is_playing():
                    await self.play_next(ctx)
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")

    async def add_youtube_playlist(self, ctx: commands.Context, url: str):
        """
        Add all videos from a YouTube playlist to the queue.

        Args:
            ctx (commands.Context): The context of the command.
            url (str): The YouTube playlist URL.
        """
        try:
            match = re.search(r"&list=([^&]*)", url)
            if match:
                list_id = match.group(1)
                titles = get_playlist_items(API_KEY, list_id)

                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    for title in titles:
                        info = ydl.extract_info(f"ytsearch:{title}", download=False)
                        if 'entries' in info and len(info['entries']) > 0:
                            info = info['entries'][0]
                            url = info['url']
                            title = info['title']
                            self.queue.append((url, title))
                            await ctx.send(f'Added **{title}** to the queue.')
                            if not ctx.voice_client.is_playing():
                                await self.play_next(ctx)
                        else:
                            await ctx.send("Could not find a YouTube video for the track.")
        except Exception as e:
            await ctx.send(f"An error occurred while processing the YouTube playlist: {str(e)}")

    async def add_spotify_playlist(self, ctx: commands.Context, url: str):
        """
        Add all tracks from a Spotify playlist to the queue.

        Args:
            ctx (commands.Context): The context of the command.
            url (str): The Spotify playlist URL.
        """
        try:
            playlist_id = re.search(r"playlist/([a-zA-Z0-9]+)", url).group(1)
            results = sp.playlist_tracks(playlist_id)
            tracks = results['items']

            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                for track in tracks:
                    track_name = track['track']['name']
                    search_query = f"{track_name}"
                    info = ydl.extract_info(f"ytsearch:{search_query}", download=False)
                    if 'entries' in info and len(info['entries']) > 0:
                        info = info['entries'][0]
                        url = info['url']
                        title = info['title']
                        self.queue.append((url, title))
                        await ctx.send(f'Added **{title}** to the queue.')
                        if not ctx.voice_client.is_playing():
                            await self.play_next(ctx)
                    else:
                        await ctx.send(f"Could not find a YouTube video for the track: **{track_name}**.")
        except Exception as e:
            await ctx.send(f"An error occurred while processing the Spotify playlist: {str(e)}")

    @commands.command(name="skip", aliases=['next'], help="Skip the current music in the queue")
    async def skip(self, ctx: commands.Context):
        """
        Skip the current song and play the next one in the queue.

        Args:
            ctx (commands.Context): The context of the command.
        """
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped the current song.")
        else:
            await ctx.send("No song is currently playing.")

    @commands.command(name="check_queue", aliases=['queue', 'q'], help="Check the list of songs in the queue")
    async def check_queue(self, ctx: commands.Context):
        """
        Display the current music queue.

        Args:
            ctx (commands.Context): The context of the command.
        """
        if not self.queue:
            await ctx.send("The queue is currently empty.")
            return

        items_per_page = 10
        total_items = len(self.queue)
        total_pages = (total_items + items_per_page - 1) // items_per_page

        def get_embed_page(page_number: int) -> nextcord.Embed:
            """
            Create an embed for the specified queue page.

            Args:
                page_number (int): The page number to display.

            Returns:
                nextcord.Embed: An embed object showing the queue.
            """
            start = page_number * items_per_page
            end = min(start + items_per_page, total_items)
            page_items = self.queue[start:end]

            embed = nextcord.Embed(
                title="Current Queue",
                description=f"Page {page_number + 1}/{total_pages}",
                color=nextcord.Color.blue()
            )
            for i, (url, title) in enumerate(page_items, start=1):
                embed.add_field(name=f"#{start + i}", value=title, inline=False)

            return embed

        current_page = 0
        embed = get_embed_page(current_page)
        message = await ctx.send(embed=embed)

        if total_pages > 1:
            await message.add_reaction("◀️")
            await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and reaction.emoji in ["◀️", "▶️"]

        while total_pages > 1:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                break

            if reaction.emoji == "◀️" and current_page > 0:
                current_page -= 1
            elif reaction.emoji == "▶️" and current_page < total_pages - 1:
                current_page += 1

            embed = get_embed_page(current_page)
            await message.edit(embed=embed)
            await message.remove_reaction(reaction.emoji, user)

    @commands.command(name="clear_queue", aliases=['cq', 'clear'], help="Clear the songs in the queue")
    async def clear_queue(self, ctx: commands.Context):
        """
        Clear all songs from the queue.

        Args:
            ctx (commands.Context): The context of the command.
        """
        self.queue = []
        await ctx.send("The queue has been cleared.")

    @commands.command(name="leave", aliases=['stop', 'tamana'], help="Disconnect the bot from the voice channel")
    async def leave(self, ctx: commands.Context):
        """
        Disconnect the bot from the voice channel.

        Args:
            ctx (commands.Context): The context of the command.
        """
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Left the voice channel.")
        else:
            await ctx.send("I'm not connected to a voice channel.")

    @commands.command(name="shuffle", help="Shuffle the songs in the queue")
    async def shuffle(self, ctx: commands.Context):
        """
        Shuffle the current music queue.

        Args:
            ctx (commands.Context): The context of the command.
        """
        if not self.queue:
            await ctx.send("The queue is currently empty.")
            return

        random.shuffle(self.queue)
        await ctx.send("The queue has been shuffled.")

        # Optional: Automatically start playing the first song after shuffling
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    @commands.command(name='wokihelp', help="Show the help message with bot commands")
    async def wokihelp(self, ctx: commands.Context):
        """
        Display a help message with all available bot commands.

        Args:
            ctx (commands.Context): The context of the command.
        """
        embed = nextcord.Embed(
            title="Woki DJ Commands:",
            description="Here are the commands you can use with Woki DJ:",
            color=nextcord.Color.blue()
        )
        embed.add_field(name="🔍 check_queue, q", value="View the list of songs in the queue.", inline=False)
        embed.add_field(name="🗑️ clear_queue, clear", value="Clear all songs from the queue.", inline=False)
        embed.add_field(name="🚪 leave", value="Disconnect the bot from the voice channel.", inline=False)
        embed.add_field(name="▶️ play, p", value="Play music using a YouTube link or search text.", inline=False)
        embed.add_field(name="🎵 playlist, pl, l", value="Add all videos from a YouTube or Spotify playlist to the queue.", inline=False)
        embed.add_field(name="🔀 shuffle", value="Shuffle the songs in the queue.", inline=False)
        embed.add_field(name="⏩ skip", value="Skip the current song in the queue.", inline=False)
        embed.add_field(name="❓ wokihelp", value="Show this help message.", inline=False)
        embed.set_footer(text="For more information on a command, type `!wokihelp`.")

        await ctx.send(embed=embed)

    async def play_next(self, ctx: commands.Context):
        """
        Play the next song in the queue.

        Args:
            ctx (commands.Context): The context of the command.
        """
        if self.queue:
            url, title = self.queue.pop(0)
            source = nextcord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda _: self.client.loop.create_task(self.play_next(ctx)))
            await ctx.send(f'Now playing **{title}**')
        elif not ctx.voice_client.is_playing():
            await ctx.send("No more songs in the queue.")
