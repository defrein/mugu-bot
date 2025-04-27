import discord
from discord.ext import commands
import json
import os
import datetime
from github import Github  # You'll need PyGithub installed

# Bot setup with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Load or create user data file
def load_data():
    if os.path.exists('pet_data.json'):
        with open('pet_data.json', 'r') as f:
            return json.load(f)
    return {}

# Save data to file
def save_data(data):
    with open('pet_data.json', 'w') as f:
        json.dump(data, f, indent=4)

# User data structure
user_data = load_data()