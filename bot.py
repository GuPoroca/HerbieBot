import discord
from discord.ext import commands
from discord.utils import get
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from discord import FFmpegPCMAudio

# Load environment variables

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# Track user-specific MP3s
user_audio_map = {
    '170604831059345408': 'audios/Escalon.mp3',  # Poroca
    '242353862030131201': 'audios/all-of-the-lights.mp3',  # Gabi
    '247115447865049088': 'audios/Betolaintro.mp3',  # Betola
    '337759969497579521': 'audios/Bankai.mp3',  # Nanda
    '292424522576166913': 'audios/mais-polvora.mp3',  # Bred
    '275661911058677760': 'audios/taylor.mp3',  # Marcel
}

# Set up the bot
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joined a voice channel
    if before.channel is None and after.channel is not None:
        user_id = str(member.id)

        # Check if the user has an assigned MP3
        if user_id in user_audio_map:
            audio_path = user_audio_map[user_id]
            voice_channel = after.channel

            # Connect to the voice channel
            vc = await voice_channel.connect()

            # Play the MP3 file
            if os.path.exists(audio_path):
                vc.play(FFmpegPCMAudio(audio_path), after=lambda e: print(f'Finished playing: {e}'))

                # Wait for the audio to finish, then disconnect
                while vc.is_playing():
                    await discord.utils.sleep_until(datetime.now() + timedelta(seconds=1))

                await vc.disconnect()
            else:
                print(f"Audio file not found: {audio_path}")

# Run the bot
bot.run(TOKEN)
