import discord
from discord.ext import commands
import datetime
from modules.pet import Pet
from modules.missions import process_login, process_journal, process_puzzle
from modules.github import link_github_account, update_github_commits
from modules.experience import get_user_profile, load_data
from config import PREFIX, DISCORD_TOKEN, calculate_level_requirement

# Bot setup with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')
    
@bot.command(name="login")
async def login(ctx):
    success, message, leveled_up = process_login(ctx.author.id)
    await ctx.send(message)
    
    if leveled_up:
        profile = get_user_profile(ctx.author.id)
        await ctx.send(f"🎉 Congratulations! Your pet reached level {profile['level']}!")

@bot.command(name="journal")
async def journal(ctx, *, entry=None):
    success, message, leveled_up = process_journal(ctx.author.id, entry)
    await ctx.send(message)
    
    if leveled_up:
        profile = get_user_profile(ctx.author.id)
        await ctx.send(f"🎉 Congratulations! Your pet reached level {profile['level']}!")

@bot.command(name="solve")
async def solve_puzzle(ctx, *, solution=None):
    success, message, leveled_up = process_puzzle(ctx.author.id, solution)
    await ctx.send(message)
    
    if leveled_up:
        profile = get_user_profile(ctx.author.id)
        await ctx.send(f"🎉 Congratulations! Your pet reached level {profile['level']}!")

@bot.command(name="link_github")
async def link_github(ctx, username=None):
    success, message = link_github_account(ctx.author.id, username)
    await ctx.send(message)

@bot.command(name="update_commits")
async def update_commits(ctx):
    success, message, leveled_up = update_github_commits(ctx.author.id)
    await ctx.send(message)
    
    if leveled_up:
        profile = get_user_profile(ctx.author.id)
        await ctx.send(f"🎉 Congratulations! Your pet reached level {profile['level']}!")

@bot.command(name="pet")
async def show_pet(ctx):
    profile = get_user_profile(ctx.author.id)
    level = profile["level"]
    xp = profile["experience"]
    
    pet = Pet(level)
    next_level_req = calculate_level_requirement(level)
    
    embed = discord.Embed(title=f"{ctx.author.name}'s {pet.get_name()}", color=0x00ff00)
    embed.add_field(name="Level", value=str(level), inline=True)
    embed.add_field(name="XP", value=f"{xp}/{next_level_req}", inline=True)
    embed.add_field(name="Progress", value=f"{min(100, int(xp/next_level_req*100))}%", inline=True)
    
    # Add mission stats
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    embed.add_field(name="Today's Missions", value=
        f"✅ Login: {'Completed' if profile.get('last_login') == today else 'Not done'}\n"
        f"📝 Journal: {'Completed' if today in profile.get('journal_days', {}) else 'Not done'}\n"
        f"💻 GitHub: {profile.get('github_commits', {}).get(today, 0)} commits\n"
        f"🧩 Puzzles: {profile.get('puzzles_solved', 0)} solved", inline=False)
    
    # Add pet ASCII art
    embed.description = f"```\n{pet.get_ascii()}\n```"
    
    await ctx.send(embed=embed)

@bot.command(name="help_pet")
async def help_command(ctx):
    help_text = """
__**Virtual Pet Bot Commands**__

**/login** - Daily login (+10 XP)
**/journal [text]** - Submit daily journal (+30 XP)
**/link_github [username]** - Link your GitHub account
**/update_commits** - Check for new GitHub commits (+3 XP per commit)
**/solve [solution]** - Submit solution to current puzzle (+2 XP)
**/pet** - View your pet's status and progress

**Level Requirements:**
Level 1 → 2: 20 XP
Level 2 → 3: 25 more XP (45 total)
Level 3 → 4: 35 more XP (80 total)
And so on...
"""
    embed = discord.Embed(title="Pet Bot Help", description=help_text, color=0x00ff00)
    await ctx.send(embed=embed)

# Run the bot
try:
    bot.run(DISCORD_TOKEN)
except Exception as e:
    print(f"Error: {e}")