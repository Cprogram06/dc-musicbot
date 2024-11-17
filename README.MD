# Ghost DJ - Discord Music Bot 🎵

Welcome to **Ghost DJ**, your personal music bot for Discord! With Ghost DJ, you can play your favorite tunes, manage playlists, and create the perfect atmosphere for your server. Below, you'll find a detailed guide to using Ghost DJ.

---

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
2. [Technologies Used](#technologies-used)
3. [Bot Commands](#bot-commands)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)
6. [Contributing](#contributing)
7. [License](#license)

---

## Features

- **Queue Management:** Add, view, shuffle, and clear songs from your music queue.
- **Playlist Support:** Import playlists from YouTube or Spotify.
- **YouTube Integration:** Play individual tracks or search for music directly.
- **Easy Setup:** Quickly connect and disconnect from voice channels.
- **Skip Tracks:** Move seamlessly to the next track in the queue.

---

## Installation
1. Clone the Ghost DJ repository:
```
git clone https://github.com/Cprogram06/dc-musicbot.git
```
2. Navigate to the project directory:
```
cd dc-musicbot
```
3. Set up a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate # For Linux/Mac
venv\Scripts\activate    # For Windows
```
4. Install the required dependencies:
```
pip install -r requirements.txt
```
5. Create a .env file in the project directory and configure your environment variables:
```
DISCORD_TOKEN=your-discord-bot-token
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_SECRET=your-spotify-client-secret
```
6. Start the bot:
```
python bot.py
```
The bot should now be running and ready for use in your Discord server.

---

## Technologies Used

Ghost DJ is built using the following technologies and libraries:

- **[Nextcord](https://docs.nextcord.dev/):** A modern Python wrapper for Discord's API, used for bot commands and event handling.
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp):** For downloading and streaming audio from YouTube.
- **[Spotipy](https://spotipy.readthedocs.io/):** For interacting with the Spotify API to retrieve playlist and track data.
- **[Google API Client](https://developers.google.com/api-client-library/python/):** For accessing YouTube playlists via the YouTube Data API.
- **[Python asyncio](https://docs.python.org/3/library/asyncio.html):** For asynchronous programming to manage concurrent tasks.
- **[dotenv](https://pypi.org/project/python-dotenv/):** For loading environment variables securely from a `.env` file.
- **[Random](https://docs.python.org/3/library/random.html):** Used for shuffling the queue.
- **Custom Scripts:**
  - `get_playlist_data.py` for processing YouTube playlist items.

---

## Bot Commands

Here’s the complete list of commands you can use with Ghost DJ:

| **Command**                 | **Alias**     | **Description**                                      |
|-----------------------------|---------------|------------------------------------------------------|
| `!check_queue`              | `!q`          | View the list of songs currently in the queue.      |
| `!clear_queue`              | `!clear`      | Clear all songs from the queue.                     |
| `!leave`                    |               | Disconnect the bot from the voice channel.          |
| `!play <YouTube URL/Text>`  | `!p`          | Play music using a YouTube link or search text.     |
| `!playlist <URL>`           | `!pl`, `!l`   | Add music from a YouTube or Spotify playlist.  |
| `!shuffle`                  |               | Shuffle the songs in the queue.                     |
| `!skip`                     |               | Skip the current song in the queue.                 |

**Note:** Prefix for the commands is customizable. The default prefix is `!`.

---

## Configuration

To customize Ghost DJ, modify the following settings in the `.env` file:

| **Variable**        | **Description**                                 |
|---------------------|-------------------------------------------------|
| `DISCORD_TOKEN`     | Your Discord bot token.                         |
| `PREFIX`            | Command prefix for the bot (default is `!`).    |

---

## Troubleshooting

Here are some common issues and how to resolve them:

1. **Bot not responding to commands:**
   - Ensure the bot has the correct permissions in the channel.
   - Check if the bot is online and running.

2. **Music not playing:**
   - Ensure FFmpeg is installed and accessible in your system path.
   - Verify the provided YouTube or playlist link is valid.

3. **Queue issues:**
   - Use the `!clear_queue` command to reset the queue if it gets stuck.

If you encounter any other issues, feel free to open a ticket on the [GitHub Issues](https://github.com/Cprogram06/dc-musicbot/issues) page.

---

## Contributing

We welcome contributions! Please fork the repository, make your changes, and submit a pull request. For major changes, open an issue first to discuss your idea.

---

## License

Ghost DJ is licensed under the [LICENSE](LICENSE). Feel free to use, modify, and distribute this bot with proper attribution.

---

🎧 **Enjoy your music with Ghost DJ!** If you have any questions or feedback, don't hesitate to reach out.
