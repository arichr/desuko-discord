"""desuko.loader - Post loader of modules."""
import logging
from typing import Callable

logger = logging.getLogger(__name__)


class Loader:
    """Post loader of Desuko modules."""

    def __init__(self, modules: dict = None, config: dict = None):
        r"""Initialize a loader.

        Args:
            modules (dict): Loaded modules
            config (dict): Config for modules. Defaults to \{\}
        """
        self.modules = modules if modules else {}
        self.config = config if config else {}

        self.shared_memory = {'foo': 'bar'}
        self.registered_handlers = {}

    def init_modules(self) -> None:
        """Initialize the provided modules."""
        for module_name, module in self.modules.items():
            self.modules[module_name] = module['class'](self)

    def handler(self, func: Callable) -> Callable:
        """Register a function as a handler.

        Args:
            func (Callable): Callable as an Desuko handler

        Returns:
            Callable: Registred function
        """
        if func.__name__.startswith('_'):
            func_name = func.__name__[1:]
        else:
            func_name = func.__name__
        key = f'{func.__module__}.{func_name}'

        def handle_subscribers(*args, **kwargs):
            """Call the provided function and its subscribers.

            Args:
                args (Iterable): Arguments
                kwargs (dict): Keyword arguments

            Returns:
                Any: Any result from the provided function (NOT its subscribers)
            """
            result = func(*args, **kwargs)
            for subscriber in self.registered_handlers[key]:
                subscriber(*args, **kwargs)
            return result

        self.registered_handlers[key] = set()
        logger.info('Handler added: %s', key)
        return handle_subscribers

    def subscribe(self, handler: str, func: Callable) -> None:
        """Return a function to register a subscriber.

        Args:
            handler (str): Handler import path
            func (Callable): Function to add as a subscriber
        """
        self.registered_handlers[handler].add(func)
        logger.info('Subscriber added: %s.%s -> %s', func.__module__, func.__name__, handler)
