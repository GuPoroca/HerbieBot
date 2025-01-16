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
    '356605986854928387': 'audios/pedronepiece.mp3',  # Pedrinho
    '211269261346340864': 'audios/dinhomusic.mp3',  # Dinho
}

# Set up the bot
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='h!', intents=intents)

# ID of the specific text channel where commands are allowed
COMMAND_CHANNEL_ID = 1329533472112377958  # Replace with your text channel ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command(name='join')
async def join(ctx):
    if ctx.channel.id != COMMAND_CHANNEL_ID:
        await ctx.send("I can only accept commands in the designated channel.")
        return

    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        vc = get(bot.voice_clients, guild=ctx.guild)

        if not vc or not vc.is_connected():
            await voice_channel.connect()
            await ctx.send(f"Joined {voice_channel}!")
        else:
            await ctx.send("I'm already in a voice channel!")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command(name='leave')
async def leave(ctx):
    if ctx.channel.id != COMMAND_CHANNEL_ID:
        await ctx.send("I can only accept commands in the designated channel.")
        return

    vc = get(bot.voice_clients, guild=ctx.guild)

    if vc and vc.is_connected():
        await vc.disconnect()
        await ctx.send("I have left the voice channel.")
    else:
        await ctx.send("I'm not connected to any voice channel.")

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:  # User joined a voice channel
        user_id = str(member.id)

        if user_id in user_audio_map:
            audio_path = user_audio_map[user_id]
            vc = get(bot.voice_clients, guild=member.guild)

            # Check if the bot is connected to a voice channel
            if vc:
                if vc.channel == after.channel:
                    # Bot is already in the same channel
                    await play_intro(vc, audio_path)
            else:
                # Bot is not connected, join the user's channel
                voice_channel = after.channel
                vc = await voice_channel.connect()
                await play_intro(vc, audio_path)

async def play_intro(vc, audio_path):
    """
    Plays the given audio file in the provided voice client.
    """
    if os.path.exists(audio_path):
        if not vc.is_playing():
            vc.play(FFmpegPCMAudio(audio_path), after=lambda e: print(f'Finished playing: {e}'))
        else:
            print("Audio is already playing, skipping intro.")
    else:
        print(f"Audio file not found: {audio_path}")

# Run the bot
bot.run(TOKEN)
