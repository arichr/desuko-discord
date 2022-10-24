"""desuko.bot - Discord bot for Desuko."""
import logging

import discord

from desuko.loader import Loader

logger = logging.getLogger(__name__)


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
        self.bot.event(self.on_ready)

        self.loader = Loader(self.bot.create_group, modules, self.config)
        self.register_slash = self.loader.handler(self._register_slash)

        self.loader.init_modules()

    def _register_slash(self) -> None:
        """Register slash commands."""
        self.bot.slash_command(description='Say hello!')(self.hello)

    async def on_ready(self):
        """Desuko is connected to Discord successfully."""
        logger.warning('We have logged in as %s', self.bot.user)
        await self.bot.sync_commands()
        logger.info('Synced comamnds')

    async def hello(self, ctx):
        """Hello command.

        Args:
            ctx (ApplicationContext): Application context
        """
        embed = discord.Embed(color=discord.Color.blurple())
        embed.add_field(name='Desuko', value='Hello', inline=True)
        await ctx.send_response(embed=embed)

    def run(self) -> None:
        """Run the Discord bot."""
        self.register_slash()
        self.bot.run(self.config['token'])
