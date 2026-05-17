import discord
from discord.ext import commands
from dotenv import load_dotenv

import asyncio
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix='!pomo ',
    intents=intents,
    help_command=None
)

active_sessions = {}
paused_sessions = {}


@bot.event
async def on_ready():

    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="students focus 📚"
    )

    await bot.change_presence(
        status=discord.Status.idle,
        activity=activity
    )

    print(f'{bot.user} is online!')


@bot.command()
async def pomo(ctx, arg1=None, arg2=None, arg3=None):
    await ctx.message.delete()

    # HELP MENU
    if arg1 == "help" or arg1 is None:

        embed = discord.Embed(
            title="🍅 Pomu by rusty.fae",
            description="Simple Pomodoro bot for some discord server",
            color=0x5865F2
        )

        embed.add_field(
            name="📚 Commands",
            value="""
`!pomo 25 5`
Start 25 minute focus + 5 minute break

`!pomo 25 5 4`
Start looping pomodoro

`!pomo pause`
Pause timer

`!pomo resume`
Resume timer

`!pomo stop`
Stop current session

`!pomo status`
Check current timer
            """,
            inline=False
        )

        embed.set_footer(text="Stay focused ✨")

        await ctx.send(embed=embed, delete_after=10)
        return

    # VC CHECK
    if not ctx.author.voice:
        await ctx.send("Join a VC first!", delete_after=5)
        return

    # START TIMER
    try:
        study_time = int(arg1)
        break_time = int(arg2)

        cycles = 1

        if arg3:
            cycles = int(arg3)

    except:
        await ctx.send("Usage: `!pomo 25 5 4`", delete_after=5)
        return

    active_sessions[ctx.author.id] = {
        "study": study_time,
        "break": break_time,
        "remaining": study_time * 60,
        "running": True,
        "paused": False,
        "phase": "study",
        "cycles": cycles
    }

    session = active_sessions[ctx.author.id]

    # MAIN LOOP
    for cycle in range(cycles):

        session["phase"] = "study"
        session["remaining"] = study_time * 60

        embed = discord.Embed(
            title="📚 Focus Session Started",
            description=(
                f"⏳ {study_time} minute study / "
                f"{break_time} minute break"
            ),
            color=0x5865F2
        )

        embed.add_field(
            name="👤 Started By",
            value=ctx.author.mention,
            inline=False
        )

        embed.set_footer(text="Stay focused ✨")

        timer_message = await ctx.send(embed=embed)

        session["message"] = timer_message

        await ctx.send(
            f"📚 Cycle {cycle + 1}/{cycles} started!",
            delete_after=5
        )

        # STUDY TIMER
        while session["remaining"] > 0:

            if ctx.author.id not in active_sessions:
                return

            # AUTO STOP IF USER LEAVES VC
            if not ctx.author.voice:

                await ctx.send(
                    f"🛑 {ctx.author.mention} left VC.\n"
                    f"Pomodoro stopped.",
                    delete_after=5
                )

                del active_sessions[ctx.author.id]
                return

            if session["paused"]:
                await asyncio.sleep(1)
                continue

            await asyncio.sleep(1)

            session["remaining"] -= 1

            minutes = session["remaining"] // 60
            seconds = session["remaining"] % 60

            live_embed = discord.Embed(
                title="📚 Focus Session",
                description=(
                    f"⏳ {minutes:02}:{seconds:02} remaining\n"
                    f"▶️ Running"
                ),
                color=0x5865F2
            )

            live_embed.add_field(
                name="👤 Started By",
                value=ctx.author.mention,
                inline=False
            )

            live_embed.add_field(
                name="📚 Cycle",
                value=f"{cycle + 1}/{cycles}",
                inline=False
            )

            live_embed.set_footer(text="Stay focused ✨")

            if session["remaining"] % 5 == 0:
                await session["message"].edit(embed=live_embed)

        await ctx.send(
            f'☕ {ctx.author.mention} Focus session ended!\n'
            f'Take a {break_time} minute break!',
            delete_after=10
        )

        # BREAK TIMER
        session["phase"] = "break"
        session["remaining"] = break_time * 60

        while session["remaining"] > 0:

            if ctx.author.id not in active_sessions:
                return

            if not ctx.author.voice:

                await ctx.send(
                    f"🛑 {ctx.author.mention} left VC.\n"
                    f"Pomodoro stopped.",
                    delete_after=5
                )

                del active_sessions[ctx.author.id]
                return

            if session["paused"]:
                await asyncio.sleep(1)
                continue

            await asyncio.sleep(1)

            session["remaining"] -= 1

            minutes = session["remaining"] // 60
            seconds = session["remaining"] % 60

            live_embed = discord.Embed(
                title="☕ Break Session",
                description=(
                    f"⏳ {minutes:02}:{seconds:02} remaining\n"
                    f"▶️ Running"
                ),
                color=0x5865F2
            )

            live_embed.add_field(
                name="👤 Started By",
                value=ctx.author.mention,
                inline=False
            )

            live_embed.add_field(
                name="📚 Cycle",
                value=f"{cycle + 1}/{cycles}",
                inline=False
            )

            live_embed.set_footer(text="Relax a little ☕")

            if session["remaining"] % 5 == 0:
                await session["message"].edit(embed=live_embed)

        await ctx.send(
            f'📚 {ctx.author.mention} Break over!\n'
            f'Back to studying!',
            delete_after=10
        )

    await ctx.send(
        f"🎉 {ctx.author.mention} completed all pomodoro cycles!",
        delete_after=10
    )

    del active_sessions[ctx.author.id]


@bot.command()
async def pause(ctx):
    await ctx.message.delete()

    session = active_sessions.get(ctx.author.id)

    if not session:
        await ctx.send("❌ No active pomodoro.", delete_after=5)
        return

    if session["paused"]:
        await ctx.send("⏸️ Pomodoro already paused.", delete_after=5)
        return

    session["paused"] = True

    await ctx.send(
        f'⏸️ {ctx.author.mention} Pomodoro paused.',
        delete_after=5
    )


@bot.command()
async def resume(ctx):
    await ctx.message.delete()

    session = active_sessions.get(ctx.author.id)

    if not session:
        await ctx.send("❌ No active pomodoro.", delete_after=5)
        return

    if not session["paused"]:
        await ctx.send("▶️ Pomodoro is already running.", delete_after=5)
        return

    session["paused"] = False

    await ctx.send(
        f'▶️ {ctx.author.mention} Pomodoro resumed.',
        delete_after=5
    )


@bot.command()
async def status(ctx):
    await ctx.message.delete()

    session = active_sessions.get(ctx.author.id)

    if not session:
        await ctx.send("❌ No active pomodoro.", delete_after=5)
        return

    minutes = session["remaining"] // 60
    seconds = session["remaining"] % 60

    phase = (
        "📚 Focus Session"
        if session["phase"] == "study"
        else "☕ Break Session"
    )

    state = (
        "⏸️ Paused"
        if session["paused"]
        else "▶️ Running"
    )

    await ctx.send(
        f"{phase}\n"
        f"⏳ {minutes:02}:{seconds:02} remaining\n"
        f"{state}",
        delete_after=15
    )


@bot.command()
async def stop(ctx):
    await ctx.message.delete()

    if ctx.author.id not in active_sessions:
        await ctx.send("❌ No active pomodoro.", delete_after=5)
        return

    del active_sessions[ctx.author.id]

    await ctx.send("🛑 Pomodoro stopped.", delete_after=5)


bot.run(TOKEN)
