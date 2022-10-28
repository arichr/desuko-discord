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
        self.loader = Loader(self.bot.create_group, self.config['modules'], modules)

        self.register_slash = self.loader.handler(self._register_slash)
        self.on_ready = self.loader.handler(
            self._on_ready, return_async=True, spoof_name='on_ready',
        )

        self.loader.init_modules()
        self.bot.event(self.on_ready)

    def _register_slash(self) -> None:
        """Register slash commands."""
        self.bot.slash_command(description='Say hello!')(self.hello)

    async def _on_ready(self):
        """Desuko is connected to Discord successfully."""
        await self.bot.sync_commands()
        logger.warning('Ready to go! We have logged in as %s.', self.bot.user)

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
