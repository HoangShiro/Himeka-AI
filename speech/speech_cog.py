import asyncio
import logging

import discord
from discord.ext import commands
from speech_recognition import RequestError, UnknownValueError
from discord import FFmpegPCMAudio
from user_files.config import *
from speech.sr_sink import SRSink

logger = logging.getLogger("speech.speech_cog")

class SpeechCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vwait = False
        self.connections = {}  # Cache of voice connections

    @discord.slash_command()
    async def vchat(self, ctx: discord.ApplicationContext):
        """Voice chat with Himeka."""
        voice = ctx.author.voice
        if not voice:
            return await ctx.respond("You're not in a vc right now")

        if ctx.guild.id in self.connections:
        # Nếu bot đã trong voice chat, thoát khỏi voice chat
            await self.connections[ctx.guild.id].disconnect()
            del self.connections[ctx.guild.id]

        vc = await voice.channel.connect()
        self.connections.update({ctx.guild.id: vc})

        # The recording takes place in the sink object.
        # SRSink will discard the audio once is transcribed.
        vc.start_recording(SRSink(self.speech_callback_bridge, ctx), self.stop_callback)

        await ctx.respond("Himeka's tablet: Himeka can hear voice now.", )

    @discord.slash_command()
    async def vstop(self, ctx: discord.ApplicationContext):
        """Stop voice chat with Himeka."""
        if ctx.guild.id in self.connections:
            vc = self.connections[ctx.guild.id]
            vc.stop_recording()
            del self.connections[ctx.guild.id]
            await ctx.delete()
        else:
            await ctx.respond("Not recording in this guild.")

    async def stop_callback(self, sink):
        pass
        #await sink.vc.disconnect()

    def speech_callback_bridge(self, recognizer, audio, ctx, user):
        asyncio.run_coroutine_threadsafe(
            self.speech_callback(recognizer, audio, ctx, user), self.bot.loop
        )

    async def speech_callback(self, recognizer, audio, ctx, user):
        from utils.ai_api import CAI, tts_get
        from utils.bot import ai_status
        if not self.vwait:
            self.vwait = True
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
                async with ctx.typing():
                    chat_log = ai_status.chat_log
                    answ, ain, busy = await CAI(text)
                    await ctx.send(answ)
                    voice_channel = ctx.author.voice.channel
                    if voice_channel:
                        url = await tts_get(answ, speaker, pitch, intonation_scale, speed)
                        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
                        await asyncio.sleep(0.5)
                        voice_client.play(FFmpegPCMAudio(url), after=lambda e: print('done', e))
                    if chat_log:
                        print(text)
                        print(f"{ain}: {answ}")
                        print()
                self.vwait = False
        else:
            print("pong~")


def setup(bot):
    bot.add_cog(SpeechCog(bot))
