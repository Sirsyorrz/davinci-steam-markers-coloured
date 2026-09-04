# davinci-steam-markers-coloured

DaVinci Resolve script that recolours timeline markers by name prefix. Pairs with [obs-steam-achievement](https://github.com/sirs/obs-steam-achievement) which writes chapter markers to recordings when Steam achievements unlock.

## Setup

Copy `colour_steam_markers.py` to:
```
/DaVinciResolve/Fusion/Scripts/
```

## Usage

1. Edit the two config values at the top of the script:
   - `MARKER_PREFIX` — prefix to match (default: `🏆 `)
   - `TARGET_COLOR` — colour to apply (default: `Yellow`)
2. Open your recording in DaVinci Resolve
3. Run via **Workspace → Scripts → colour_steam_markers**

Valid colours: `Blue`, `Cyan`, `Green`, `Yellow`, `Red`, `Pink`, `Purple`, `Fuchsia`, `Rose`, `Lavender`, `Sky`, `Mint`, `Lemon`, `Sand`, `Cocoa`, `Cream`
