# Configuration

Desuko has pre-defined values to work with. However, it also provides an opportunity to use `desuko.yaml` for more precise control over things.

For now, Desuko handles these options:

* **token** (`str`; **Required**): Token of your Discord bot
* **debug_guilds** (`Iterable[int]`; Optional): Debug guilds (updates slash commands only for specified guilds). Defaults to `[]`.
* **silence_import_exceptions** (`bool`; Optional): Should import failures be handled automatically or leave them as-is? Defaults to `True`.
* **modules** (`dict[str, Any]`; Optional): Modules to extend an Desuko functionality. Defaults to `{}`.

## Modules

Modules can differ one from another. So their configuration styles. To see possible options, refer to their own documentation pages.
