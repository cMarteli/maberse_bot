# soundmap.py

def load_user_sounds(file_path="sounds.txt"):
    user_sounds = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(",", 1)
                if len(parts) == 2:
                    user_id_str, sound_file = parts
                    user_id = int(user_id_str.strip())
                    sound_file = sound_file.strip()
                    user_sounds[user_id] = sound_file
    except FileNotFoundError:
        print("[WARN] sounds.txt not found.")
    except Exception as e:
        print(f"[ERROR] Failed to load sounds.txt: {e}")
    return user_sounds
