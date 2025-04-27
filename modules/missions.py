import datetime
from modules.experience import add_experience, get_user_profile, load_data, save_data
from config import XP_SETTINGS

def process_login(user_id):
    """Process daily login mission"""
    data = load_data()
    profile = get_user_profile(user_id, data)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if profile["last_login"] == today:
        return False, "You've already logged in today!", 0
    
    profile["last_login"] = today
    save_data(data)
    
    leveled_up = add_experience(user_id, XP_SETTINGS['login'])
    return True, f"Daily login successful! +{XP_SETTINGS['login']} XP.", leveled_up

def process_journal(user_id, entry):
    """Process journal submission"""
    data = load_data()
    profile = get_user_profile(user_id, data)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if not entry:
        return False, "Please include your journal entry.", 0
        
    if today in profile.get("journal_days", {}):
        return False, "You've already submitted a journal today!", 0
    
    if "journal_days" not in profile:
        profile["journal_days"] = {}
        
    profile["journal_days"][today] = entry
    save_data(data)
    
    leveled_up = add_experience(user_id, XP_SETTINGS['journal'])
    return True, f"Journal entry recorded! +{XP_SETTINGS['journal']} XP.", leveled_up

def process_puzzle(user_id, solution):
    """Process puzzle solving"""
    data = load_data()
    profile = get_user_profile(user_id, data)
    
    if not solution:
        return False, "Please include your solution.", 0
    
    # In a real implementation, verify solution
    
    profile["puzzles_solved"] = profile.get("puzzles_solved", 0) + 1
    save_data(data)
    
    leveled_up = add_experience(user_id, XP_SETTINGS['puzzle'])
    return True, f"Puzzle solution submitted! +{XP_SETTINGS['puzzle']} XP.", leveled_up