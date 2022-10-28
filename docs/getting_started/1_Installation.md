# Installation

1\. Install dependencies: `poetry install --no-root --no-dev`

2\. Complete `desuko.yaml` with your Discord token:
```yaml
token: YOUR_DISCORD_BOT_TOKEN_HERE
```

3\. _(optional)_ Specify debug guilds to test Desuko faster:
```yaml
debug_guilds:
 - YOUR_GUILD_ID_HERE
```

4\. Run Desuko as a Python module: `python -m desuko`
