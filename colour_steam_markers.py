# colour_steam_markers.py
# Run from DaVinci Resolve: Workspace > Scripts, or paste into the console.
#
# Finds every marker (on timeline items and the timeline itself) whose name
# starts with MARKER_PREFIX and changes its colour to TARGET_COLOR.
# Marker content (name, note, duration) is preserved.

# ── config ────────────────────────────────────────────────────────────────────

MARKER_PREFIX = "🏆 "

# Valid colours: Blue, Cyan, Green, Yellow, Red, Pink, Purple, Fuchsia,
#                Rose, Lavender, Sky, Mint, Lemon, Sand, Cocoa, Cream
TARGET_COLOR = "Yellow"

# ── helpers ───────────────────────────────────────────────────────────────────

def recolour_markers(obj, label):
    markers = obj.GetMarkers()
    if not markers:
        return 0

    changed = 0
    for frame_id, info in markers.items():
        if not info["name"].startswith(MARKER_PREFIX):
            continue
        if info["color"] == TARGET_COLOR:
            continue

        obj.DeleteMarkerAtFrame(frame_id)
        obj.AddMarker(
            frame_id,
            TARGET_COLOR,
            info["name"],
            info["note"],
            info["duration"],
            info.get("customData", ""),
        )
        print(f"  [{label}] frame {frame_id}: '{info['name']}' → {TARGET_COLOR}")
        changed += 1

    return changed

# ── main ──────────────────────────────────────────────────────────────────────

resolve = bmd.scriptapp("Resolve")  # bmd is a DaVinci built-in when running from Scripts menu
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()

print(f"Timeline: {timeline.GetName()}")
print(f"Prefix:   '{MARKER_PREFIX}'")
print(f"Colour:   {TARGET_COLOR}")
print()

total = 0

# Timeline-level markers (in case any ended up here)
total += recolour_markers(timeline, "timeline")

# Clip-level markers across all tracks
for track_type, prefix in (("video", "V"), ("audio", "A")):
    for track_idx in range(1, timeline.GetTrackCount(track_type) + 1):
        items = timeline.GetItemListInTrack(track_type, track_idx)
        for item in (items or []):
            total += recolour_markers(item, f"{prefix}{track_idx} '{item.GetName()}'")


print()
print(f"Done — {total} marker(s) recoloured.")
