# Configuration

Desuko can operate on its own, once the `token` value is valid and saved correctly. However, to specify more options `desuko.yaml` should be used. For now, those can be handled by Desuko out-of-the-box:

* **token** (`str`): Token of your Discord bot
* **debug_guilds** (`Iterable[int]`): Discord debug guilds, represented as an interable of integers.
* **silence_import_exceptions** (`bool`): Should we fail silently on import exceptions? Defaults to `True`.
* **modules** (`dict[str, Any]`): A dictionary of enabled modules, whose keys are valid package names and values can be anything.

!!! note
    If you want to place Desuko configuration elsewhere, use **config_file** (`str`).
    In that case, all other options in `desuko.yaml` **will be ignored**.
