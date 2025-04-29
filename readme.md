# Discord Pet Bot

Level up your virtual pet by solving (idk yet), journaling, and committing to GitHub! 🐾

## Commands

- **/login**  
  Do your daily login to earn 10 XP. *(Only once per day)*

- **/journal [text]**  
  Submit a daily journal entry to earn 30 XP. *(Only once per day)*  
  Example:  
  `/journal Today I worked on my Python project and learned about Discord bots.`

- **/link_github [username]**  
  Link your GitHub account to track your coding activity.  
  Example:  
  `/link_github yourusername`

- **/update_commits**  
  Check for new GitHub commits. Earn 3 XP per commit.

- **/solve [solution]**  
  Submit solutions to coding puzzles. Earn 2 XP per solution.  
  Example:  
  `/solve My solution to the problem is...`

- **/pet**  
  View your pet's status, level, and progress.

- **/help_pet**  
  Display help information about all available commands.

## How It Works

- You can **login once per day** to get XP.
- You can **submit one journal entry per day** for extra XP.
- **GitHub commits** are tracked when you run `/update_commits`.
- **Earn XP** to level up and evolve your pet!

## Getting Started

1. Clone this repository.
2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file and add your Discord Bot token:

    ```
    DISCORD_TOKEN=your_token_here
    AI_API_KEY=your_api_key
    ```

4. Run the bot:

    ```bash
    python main.py
    ```

5. Invite the bot to your server and start playing!
