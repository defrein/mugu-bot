import json
import os
from config import calculate_level_requirement

DATA_PATH = 'data/pet_data.json'

def ensure_data_dir():
    os.makedirs('data', exist_ok=True)

def load_data():
    ensure_data_dir()
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    ensure_data_dir()
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def get_user_profile(user_id, data=None):
    if data is None:
        data = load_data()
    
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {
            "level": 1,
            "experience": 0,
            "last_login": None,
            "github_commits": {},
            "journal_days": {},
            "puzzles_solved": 0
        }
        save_data(data)
    return data[user_id]

def add_experience(user_id, amount):
    """Add experience and check for level up"""
    data = load_data()
    profile = get_user_profile(user_id, data)
    profile["experience"] += amount
    save_data(data)
    
    return check_level_up(user_id, data)

def check_level_up(user_id, data=None):
    """Check if user can level up, returns true if leveled up"""
    if data is None:
        data = load_data()
        
    profile = get_user_profile(user_id, data)
    level_req = calculate_level_requirement(profile["level"])
    
    if profile["experience"] >= level_req:
        profile["level"] += 1
        save_data(data)
        return True
    return False