# davinci-steam-markers-coloured

DaVinci Resolve script that finds markers by name prefix and recolours them. Designed to work with [obs-steam-achievement](https://github.com/Sirsyorrz/obs-steam-achievement-marker) which writes chapter markers to recordings on Steam achievement unlocks.

## Install

Copy `colour_steam_markers.py` to:

**Linux**
```
~/.local/share/DaVinciResolve/Fusion/Scripts/Utility/
```

**Windows**
```
%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\
```

**macOS**
```
~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/
```

## Usage

Run via **Workspace → Scripts → Utility → colour_steam_markers**.

A dialog will open where you can set the marker prefix, pick a colour, and optionally strip all markers off audio tracks before hitting Run.
