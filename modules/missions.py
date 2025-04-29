import datetime
from database import get_user_profile, add_experience, update_login, add_journal_entry, increment_puzzles_solved
from config import XP_SETTINGS

def process_login(user_id):
    """Process daily login mission"""
    profile = get_user_profile(user_id)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if profile["last_login"] == today:
        return False, "You've already logged in today!", False
    
    update_login(user_id, today)
    
    leveled_up = add_experience(user_id, XP_SETTINGS['login'])
    return True, f"Daily login successful! +{XP_SETTINGS['login']} XP.", leveled_up

def process_journal(user_id, entry):
    """Process journal submission"""
    profile = get_user_profile(user_id)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if not entry:
        return False, "Please include your journal entry.", False
        
    if today in profile.get("journal_days", {}):
        return False, "You've already submitted a journal today!", False
    
    success = add_journal_entry(user_id, entry, today)
    
    if not success:
        return False, "You've already submitted a journal today!", False
    
    leveled_up = add_experience(user_id, XP_SETTINGS['journal'])
    return True, f"Journal entry recorded! +{XP_SETTINGS['journal']} XP.", leveled_up

def process_puzzle(user_id, solution):
    """Process puzzle solving"""
    if not solution:
        return False, "Please include your solution.", False
    
    # In a real implementation, verify solution
    increment_puzzles_solved(user_id)
    
    leveled_up = add_experience(user_id, XP_SETTINGS['puzzle'])
    return True, f"Puzzle solution submitted! +{XP_SETTINGS['puzzle']} XP.", leveled_up