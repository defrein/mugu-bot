import datetime
from github import Github
from database import get_user_profile, add_experience, update_github_username, record_github_commits
from config import GITHUB_TOKEN, XP_SETTINGS

def link_github_account(user_id, github_username):
    """Link a GitHub account to user profile"""
    if not github_username:
        return False, "Please provide your GitHub username."
    
    update_github_username(user_id, github_username)
    
    return True, f"GitHub account {github_username} linked successfully!"

def update_github_commits(user_id):
    """Update GitHub commit count and award XP"""
    profile = get_user_profile(user_id)
    
    if "github_username" not in profile or not profile["github_username"]:
        return False, "You need to link your GitHub account first with `/link_github username`", False
    
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
            
        # Calculate new commits
        previous_commits = profile["github_commits"].get(today, 0)
        new_commits = max(0, commit_count - previous_commits)
        
        if new_commits > 0:
            record_github_commits(user_id, today, commit_count)
            
            leveled_up = add_experience(user_id, new_commits * XP_SETTINGS['commit'])
            return True, f"Found {new_commits} new commits! +{new_commits * XP_SETTINGS['commit']} XP.", leveled_up
        else:
            return False, "No new commits found since last check.", False
            
    except Exception as e:
        return False, f"Error fetching GitHub data: {str(e)}", False