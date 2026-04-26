import json
import os

def get_save_path():
    """Return a writable path for the save file, especially for Android."""
    # Check if we are running on Android
    if 'ANDROID_ARGUMENT' in os.environ or 'ANDROID_PRIVATE' in os.environ:
        # Use the internal app storage directory
        return os.path.join(os.environ.get('PYTHON_SERVICE_ARGUMENT', '.'), "save.json")
    # Default to local folder for PC
    return os.path.join(os.path.dirname(__file__), "save.json")

SAVE_FILE = get_save_path()

DEFAULTS = {
    "best_score": 0,
    "previous_score": 0,
    "music_vol": 50,   # 0–100
    "sfx_on": True,
}

def load_data():
    if not os.path.exists(SAVE_FILE):
        return dict(DEFAULTS)
    try:
        data = json.load(open(SAVE_FILE, "r"))
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
