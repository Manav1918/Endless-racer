import json
import os

def get_save_path(filename="save.json"):
    """Return a writable app-private path on Android, or a local path on desktop."""
    base_dir = os.environ.get("ANDROID_PRIVATE") or os.getcwd()
    try:
        os.makedirs(base_dir, exist_ok=True)
    except Exception:
        base_dir = os.getcwd()
    return os.path.join(base_dir, filename)

SAVE_FILE = get_save_path()

DEFAULTS = {
    "best_score": 0,
    "previous_score": 0,
    "music_vol": 50,
    "sfx_on": True,
}

def load_data():
    if not os.path.exists(SAVE_FILE):
        return dict(DEFAULTS)
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Fill any missing keys with defaults (handles old save files)
        for k, v in DEFAULTS.items():
            data.setdefault(k, v)
        return data
    except Exception:
        return dict(DEFAULTS)

def save_data(best_score, previous_score, music_vol=None, sfx_on=None):
    # Load existing first so we don't wipe other keys
    current = load_data()
    current["best_score"]     = best_score
    current["previous_score"] = previous_score
    if music_vol is not None:
        current["music_vol"] = music_vol
    if sfx_on is not None:
        current["sfx_on"] = sfx_on
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(current, f, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")

def save_settings(music_vol, sfx_on):
    """Save only settings without touching scores."""
    current = load_data()
    current["music_vol"] = music_vol
    current["sfx_on"]    = sfx_on
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(current, f, indent=2)
    except Exception as e:
        print(f"Error saving settings: {e}")
