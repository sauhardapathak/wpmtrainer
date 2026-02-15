import json
import os
import base64
from pathlib import Path

# Store in user's AppData folder (hidden on Windows)
if os.name == 'nt':  # Windows
    APPDATA = os.getenv('APPDATA')
    SAVE_DIR = os.path.join(APPDATA, '.wpmtrainer')
else:  # Mac/Linux
    HOME = Path.home()
    SAVE_DIR = os.path.join(HOME, '.wpmtrainer')

# Create directory if it doesn't exist
os.makedirs(SAVE_DIR, exist_ok=True)

HIGHSCORE_FILE = os.path.join(SAVE_DIR, '.data')

def _encode(data):
    """Simple obfuscation (NOT real encryption)"""
    json_str = json.dumps(data)
    encoded = base64.b64encode(json_str.encode()).decode()
    return encoded

def _decode(encoded):
    """Simple deobfuscation"""
    try:
        decoded = base64.b64decode(encoded.encode()).decode()
        return json.loads(decoded)
    except:
        return None

def load_all_highscores():
    """Load all high scores from hidden file.
    Returns dict with keys: 'easy', 'medium', 'hard'
    """
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                encoded = f.read()
                data = _decode(encoded)
                if data:
                    return {
                        'easy': data.get('e', 0),
                        'medium': data.get('m', 0),
                        'hard': data.get('h', 0)
                    }
        except:
            pass
    return {'easy': 0, 'medium': 0, 'hard': 0}

def load_highscore(difficulty='medium'):
    """Load high score for specific difficulty."""
    scores = load_all_highscores()
    return scores.get(difficulty, 0)

def save_highscore(score, difficulty):
    """Save high score for specific difficulty."""
    scores = load_all_highscores()
    
    # Update the specific difficulty
    if difficulty == 'easy':
        scores['easy'] = score
    elif difficulty == 'medium':
        scores['medium'] = score
    elif difficulty == 'hard':
        scores['hard'] = score
    
    # Encode and save
    data = {'e': scores['easy'], 'm': scores['medium'], 'h': scores['hard']}
    encoded = _encode(data)
    with open(HIGHSCORE_FILE, 'w') as f:
        f.write(encoded)

def check_and_update_highscore(new_score, difficulty):
    """Check if new score is higher for this difficulty. Update if it is.
    Returns True if new high score, False otherwise."""
    current_high = load_highscore(difficulty)
    if new_score > current_high:
        save_highscore(new_score, difficulty)
        return True
    return False