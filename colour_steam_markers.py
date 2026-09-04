# colour_steam_markers.py
# Workspace > Scripts > Utility > ColorSteamMarkers

COLORS = [
    "Blue", "Cyan", "Green", "Yellow", "Red", "Pink", "Purple",
    "Fuchsia", "Rose", "Lavender", "Sky", "Mint", "Lemon", "Sand", "Cocoa", "Cream",
]

DEFAULT_PREFIX = "🏆 "
DEFAULT_COLOR  = "Yellow"

# ── resolve / ui bootstrap ────────────────────────────────────────────────────

resolve  = bmd.scriptapp("Resolve")
project  = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()
fusion   = resolve.Fusion()
ui       = fusion.UIManager
disp     = bmd.UIDispatcher(ui)

# ── ui ────────────────────────────────────────────────────────────────────────

win = disp.AddWindow({
    "ID":          "CSMWin",
    "WindowTitle": "Colour Steam Markers",
    "Geometry":    [200, 200, 380, 220],
}, [
    ui.VGroup({"Spacing": 8}, [
        ui.HGroup({"Weight": 0}, [
            ui.Label({"Text": "Marker prefix:", "Weight": 0.4}),
            ui.LineEdit({"ID": "Prefix", "Text": DEFAULT_PREFIX, "Weight": 0.6}),
        ]),
        ui.HGroup({"Weight": 0}, [
            ui.Label({"Text": "Change colour to:", "Weight": 0.4}),
            ui.ComboBox({"ID": "Color", "Weight": 0.6}),
        ]),
        ui.CheckBox({
            "ID":      "RemoveAudio",
            "Text":    "Remove all markers from audio tracks",
            "Checked": False,
            "Weight":  0,
        }),
        ui.VGap(4),
        ui.HGroup({"Weight": 0}, [
            ui.Button({"ID": "BtnRun",    "Text": "Run",    "Weight": 1}),
            ui.Button({"ID": "BtnCancel", "Text": "Cancel", "Weight": 1}),
        ]),
        ui.Label({"ID": "Status", "Text": "", "Weight": 1, "WordWrap": True}),
    ]),
])

itm = win.GetItems()
for c in COLORS:
    itm["Color"].AddItem(c)
itm["Color"].CurrentIndex = COLORS.index(DEFAULT_COLOR)

# ── logic ─────────────────────────────────────────────────────────────────────

def recolour_markers(obj, prefix, color):
    markers = obj.GetMarkers()
    if not markers:
        return 0
    changed = 0
    for frame_id, info in markers.items():
        if not info["name"].startswith(prefix):
            continue
        if info["color"] == color:
            continue
        obj.DeleteMarkerAtFrame(frame_id)
        obj.AddMarker(frame_id, color, info["name"], info["note"],
                      info["duration"], info.get("customData", ""))
        changed += 1
    return changed


def remove_audio_markers(tl):
    removed = 0
    for track_idx in range(1, tl.GetTrackCount("audio") + 1):
        for item in (tl.GetItemListInTrack("audio", track_idx) or []):
            markers = item.GetMarkers()
            for frame_id in list(markers.keys()):
                item.DeleteMarkerAtFrame(frame_id)
                removed += 1
    return removed


def run(prefix, color, strip_audio):
    total   = 0
    removed = 0

    total += recolour_markers(timeline, prefix, color)

    for track_type in ("video", "audio"):
        for track_idx in range(1, timeline.GetTrackCount(track_type) + 1):
            for item in (timeline.GetItemListInTrack(track_type, track_idx) or []):
                total += recolour_markers(item, prefix, color)

    if strip_audio:
        removed = remove_audio_markers(timeline)

    parts = [f"{total} marker(s) recoloured."]
    if strip_audio:
        parts.append(f"{removed} audio marker(s) removed.")
    return "  ".join(parts)

# ── events ────────────────────────────────────────────────────────────────────

def on_run(ev):
    prefix      = itm["Prefix"].Text
    color       = COLORS[itm["Color"].CurrentIndex]
    strip_audio = itm["RemoveAudio"].Checked
    try:
        msg = run(prefix, color, strip_audio)
        itm["Status"].Text = msg
    except Exception as e:
        itm["Status"].Text = f"Error: {e}"

def on_cancel(ev):
    disp.ExitLoop()

win.On.CSMWin.Close    = lambda ev: disp.ExitLoop()
win.On.BtnRun.Clicked  = on_run
win.On.BtnCancel.Clicked = on_cancel

win.Show()
disp.RunLoop()
win.Hide()
