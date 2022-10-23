"""Desuko - Discord bot.

How is it structured?
    Desuko aims to be modular. It has a base package implemented here and modules
    to extend its functionality.

    To make changes into Desuko code, please, make sure that your edits will NOT
    break any existing modules.
"""
import logging
import sys
from importlib import import_module
from pathlib import Path

from yaml import safe_load

from desuko.bot import DesukoBot

BASE_DIR = Path(__file__).parent.parent

logging.basicConfig(
    format='%(asctime)23s | %(levelname)8s | %(message)s',
    level=logging.INFO,
)

try:
    with open(BASE_DIR / 'desuko.yaml', 'rb') as yaml_f:
        CONFIG = safe_load(yaml_f)

    if CONFIG.get('config_file'):
        logging.info('Found configuration re-direct.')
        with open(BASE_DIR / CONFIG['config_file'], 'rb') as yaml_f:
            CONFIG = safe_load(yaml_f)
except IOError:
    logging.critical('Failed to load Desuko configuration. Abort.')
    sys.exit(1)


def load_module(name: str) -> dict:
    """Load an Desuko Python module.

    Args:
        name (str): Name of a submodule (e.g. `desuko.modules.foo_bar`)

    Returns:
        dict: Information about the module

    Raises:
        AttributeError: One of Desuko modules miss required functions
        ModuleNotFoundError: Configuration requires non-existing modules
    """
    try:
        module = import_module(f'desuko.modules.{name}')
        return {
            'desc': module.__DESC__,
            'version': module.__VERSION__,
            'class': module.Module,
        }
    except (AttributeError, ModuleNotFoundError) as exc:
        if CONFIG.get('silence_import_exceptions'):
            return {}

        raise exc


modules = {}

for module_name in CONFIG['modules'].keys():
    modules[module_name] = load_module(module_name)
    if not modules[module_name]:
        logging.critical('Unable to import %s. Abort.', module_name)
        sys.exit(1)

logging.warning('Loaded %d modules.', len(modules))

DesukoBot(CONFIG, modules).run()
