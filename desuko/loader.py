"""desuko.loader - Post loader of modules."""
import inspect
import logging
from typing import Callable

logger = logging.getLogger(__name__)


class Loader:
    """Post loader of Desuko modules."""

    def __init__(self, create_group_def: Callable, config: dict, modules: dict):
        """Initialize a loader.

        Args:
            create_group_def (Callable): `Bot.create_group` function
            config (dict): Config for modules
            modules (dict): Loaded modules
        """
        self.__create_group_def = create_group_def
        self.__config = config if config else {}
        self.modules = modules if modules else {}

        self.shared_memory = {}
        self.registered_handlers = {}

    def init_modules(self) -> None:
        """Initialize the provided modules."""
        for module_name, module in self.modules.items():
            discord_module_name = ''.join(i for i in module_name if i.isalpha())[:32]
            module_cmd_group = self.__create_group_def(discord_module_name, module['desc'])

            self.modules[module_name] = module['class'](
                self,
                module_cmd_group,
                self.__config[module_name],
            )

    def handler(self, func: Callable, return_async=False) -> Callable:
        """Register a function as a handler.

        If `bool(return_async) == False`, all subscribers will be treated as non-synchronous.

        Args:
            func (Callable): Callable as an Desuko handler
            return_async (bool): Should the function return an asyncronious Callable

        Returns:
            Callable: Registred function
        """
        if func.__name__.startswith('_'):
            func_name = func.__name__[1:]
        else:
            func_name = func.__name__
        key = f'{func.__module__}.{func_name}'

        is_func_async = inspect.iscoroutinefunction(func)

        def handle_subscribers(*args, **kwargs):
            """Call the provided function and its subscribers.

            Args:
                args (Iterable): Arguments
                kwargs (dict): Keyword arguments

            Returns:
                Any: Any result from the provided function (NOT its subscribers)
            """
            result = func(*args, **kwargs)
            for subscriber, is_sub_async in self.registered_handlers[key]:
                if is_sub_async:
                    logger.warning(
                        '%s.%s is an asyncronious function, that was registered as synchronous.',
                        subscriber.__module__,
                        subscriber.__name__,
                    )
                subscriber(*args, **kwargs)
            return result

        async def async_handle_subscribers(*args, **kwargs):
            """Call the provided function and its subscribers.

            Args:
                args (Iterable): Arguments
                kwargs (dict): Keyword arguments

            Returns:
                Any: Any result from the provided function (NOT its subscribers)
            """
            if is_func_async:
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            for subscriber, is_sub_async in self.registered_handlers[key]:
                if is_sub_async:
                    await subscriber(*args, **kwargs)
                else:
                    subscriber(*args, **kwargs)
            return result

        self.registered_handlers[key] = set()
        logger.info('Handler added: %s', key)

        return async_handle_subscribers if return_async else handle_subscribers

    def subscribe(self, handler: str, func: Callable) -> None:
        """Return a function to register a subscriber.

        Args:
            handler (str): Handler import path
            func (Callable): Function to add as a subscriber

        Raises:
            ValueError: Provided invalid handler
        """
        try:
            self.registered_handlers[handler].add((func, inspect.iscoroutinefunction(func)))
        except KeyError as exc:
            raise ValueError(f'{exc.args[0]} is not a valid handler.') from exc
        logger.info('Subscriber added: %s.%s -> %s', func.__module__, func.__name__, handler)
