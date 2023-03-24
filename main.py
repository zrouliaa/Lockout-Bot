import discord
import os
import datetime

from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, BadArgument, MemberNotFound

from utils import tasks
from constants import AUTO_UPDATE_TIME
from cogs import handles

from dotenv import load_dotenv
load_dotenv()

#intents = discord.Intents.all()
#intents = discord.Intents.default()
#intents.members = True
#client = Bot(case_insensitive=True, description="Lockout Bot", command_prefix=when_mentioned_or("."), intents=intents)

logging_channel = None

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = commands.when_mentioned_or("."),
            intents = discord.Intents.all(),
            help_command = commands.DefaultHelpCommand(dm_help=True)
        )
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="lool ⚔️"))

    async def setup_hook(self): #overwriting a handler
        print(f"\033[31mLogged in as {client.user}\033[39m")
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/cogs"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await client.tree.sync()
        print("Loaded cogs")

client = Client()
client.run(os.environ.get('LOCKOUT_BOT_TOKEN'))
