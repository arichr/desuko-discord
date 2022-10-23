"""desuko.bot - Discord bot for Desuko."""
import discord

from desuko.loader import Loader


class DesukoBot:
    """Discord bot class."""

    def __init__(self, config: dict, modules: dict):
        """Initialize a bot.

        Args:
            config (dict): Desuko configuration
            modules (dict): Loaded modules
        """
        self.config = config
        self.bot = discord.Bot(
            auto_sync_commands=False,
            debug_guilds=self.config.get('debug_guilds'),
        )

        self.loader = Loader(modules, self.config)
        self.register_slash = self.loader.handler(self._register_slash)

        self.loader.init_modules()

    def _register_slash(self) -> None:
        """Register slash commands."""
        print('Bot register_slash')  # TODO:

    async def hello(self, ctx):
        """Hello command.

        Args:
            ctx (ApplicationContext): Application context
        """
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name='Name', value='Value', inline=True)
        await ctx.send_response(embed=embed)

    def run(self) -> None:
        """Run the Discord bot."""
        self.register_slash()
