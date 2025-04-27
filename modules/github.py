import datetime
from github import Github
from modules.experience import add_experience, get_user_profile, load_data, save_data
from config import GITHUB_TOKEN, XP_SETTINGS

def link_github_account(user_id, github_username):
    """Link a GitHub account to user profile"""
    data = load_data()
    profile = get_user_profile(user_id, data)
    
    if not github_username:
        return False, "Please provide your GitHub username."
    
    profile["github_username"] = github_username
    save_data(data)
    
    return True, f"GitHub account {github_username} linked successfully!"

def update_github_commits(user_id):
    """Update GitHub commit count and award XP"""
    data = load_data()
    profile = get_user_profile(user_id, data)
    
    if "github_username" not in profile:
        return False, "You need to link your GitHub account first with `/link_github username`", 0
    
    # Use token if available, otherwise use public access
    g = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()
    
    try:
        user = g.get_user(profile["github_username"])
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        commit_count = 0
        
        # Count today's commits
        for repo in user.get_repos():
            try:
                commits = repo.get_commits(since=datetime.datetime.strptime(today, "%Y-%m-%d"))
                for commit in commits:
                    if commit.commit.author.name == user.name or commit.commit.author.email == user.email:
                        commit_count += 1
            except:
                continue
        
        # Initialize if needed
        if "github_commits" not in profile:
            profile["github_commits"] = {}
            
        # Calculate new commits
        previous_commits = profile["github_commits"].get(today, 0)
        new_commits = max(0, commit_count - previous_commits)
        
        if new_commits > 0:
            profile["github_commits"][today] = commit_count
            save_data(data)
            
            leveled_up = add_experience(user_id, new_commits * XP_SETTINGS['commit'])
            return True, f"Found {new_commits} new commits! +{new_commits * XP_SETTINGS['commit']} XP.", leveled_up
        else:
            return False, "No new commits found since last check.", 0
            
    except Exception as e:
        return False, f"Error fetching GitHub data: {str(e)}", 0