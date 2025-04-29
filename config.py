import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
PREFIX = '/'
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    print("ERROR: Discord token not found in environment variables!")

if DISCORD_TOKEN is None:
    raise ValueError("DISCORD_TOKEN is not set in the environment variables.")
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

AI_API_KEY = os.getenv("AI_API_KEY")
AI_API_URL = os.getenv("AI_API_URL", "https://api.openai.com/v1/chat/completions")

# Experience settings
XP_SETTINGS = {
    'login': 10,
    'journal': 30,
    'commit': 3,
    'puzzle': 2
}

# Level requirements
def calculate_level_requirement(level):
    if level == 1:
        return 20
    elif level == 2:
        return 45
    elif level == 3:
        return 80
    else:
        return calculate_level_requirement(level-1) + (level * 10)