import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
PREFIX = '/'
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

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