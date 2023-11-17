import asyncio
import logging

import discord
from discord.ext import commands
from speech_recognition import RequestError, UnknownValueError
from user_files.config import *
from speech.sr_sink import SRSink

logger = logging.getLogger("speech.speech_cog")


class SpeechCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connections = {}  # Cache of voice connections

    @discord.slash_command()
    async def start(self, ctx: discord.ApplicationContext):
        """Start transcription."""
        guild = self.bot.get_guild(ctx.guild_id)
        voice = ctx.author.voice
        if not voice:
            return await ctx.respond("You're not in a vc right now")

        vc = guild.voice_client
        self.connections.update({ctx.guild.id: vc})

        # The recording takes place in the sink object.
        # SRSink will discard the audio once is transcribed.
        vc.start_recording(SRSink(self.speech_callback_bridge, ctx), self.stop_callback)

        await ctx.respond("The transcription has started!")

    @discord.slash_command()
    async def stop(self, ctx: discord.ApplicationContext):
        """Stop transcription."""
        if ctx.guild.id in self.connections:
            vc = self.connections[ctx.guild.id]
            vc.stop_recording()
            del self.connections[ctx.guild.id]
            await ctx.delete()
        else:
            await ctx.respond("Not recording in this guild.")

    async def stop_callback(self, sink):
        await sink.vc.disconnect()

    def speech_callback_bridge(self, recognizer, audio, ctx, user):
        asyncio.run_coroutine_threadsafe(
            self.speech_callback(recognizer, audio, ctx, user), self.bot.loop
        )

    async def speech_callback(self, recognizer, audio, ctx, user):
        from utils.ai_api import CAI, tts_get
        from utils.funcs import vals_load
        try:
            text = recognizer.recognize_google(audio, language='vi-VN')
        except UnknownValueError:
            logger.debug("Google Speech Recognition could not understand audio")
        except RequestError as e:
            logger.exception(
                "Could not request results from Google Speech Recognition service",
                exc_info=e,
            )
        else:
            chat_log = vals_load('user_files/vals.json', 'chat_log')
            answ, ain = await CAI(text)
            url = await tts_get(answ, speaker, pitch, intonation_scale, speed)
            if chat_log:
                print(text)
                print(f"{ain}: {answ}")
                print()
            await ctx.send(f"<@{user}> said: {text}")


def setup(bot):
    bot.add_cog(SpeechCog(bot))
