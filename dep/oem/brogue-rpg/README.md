# brogue-rpg

## Build and run
```
python scripts/rebuild_pkpy.py

pocketpy/main.exe main.py
```
Supports Windows, Linux, and MacOS. For mobile platforms, use the `driver.py` script.

## File structure
+ `backend/` - Game logic and data flow
+ `frontend/` - Terminal rendering and user input handling
+ `pocketpy/` - Portable python interpreter
+ `dungeon3/` - Dungeon generation algorithm
+ `scripts/` - Build and utility scripts
+ `driver.py` - Game driver for terminal rendering for both desktop and mobile
+ `main.py` - Game entry point for desktop platforms
+ `pyrightconfig.json` - Python auto-completion configuration for VSCode

## Notes
If you are using VSCode's integrated terminal, you should add this line to the `settings.json` file:

```
"terminal.integrated.minimumContrastRatio": 1,
```

VSCode does not support emojis.
