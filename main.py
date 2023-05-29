from discord import Intents
from discord.ext import commands
from discord import Game
from discord import Status
from discord import Object
from discord import TextChannel

class main(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='',
            intents=Intents.all(),
            sync_all_commands=True,
            application_id=
        )
        self.initial_extension = [
            "Cogs.Commands"
        ]

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)
        await bot.tree.sync()

    async def on_ready(self):
        print("login")
        print(self.user.name)
        print(self.user.id)
        print("===============")
        game = Game("작동")
        await self.change_presence(status=Status.online, activity=game)
    
bot = main()
bot.run('')
