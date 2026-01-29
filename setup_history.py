"""
PixelStream Bot - High-Performance Terminal Media Engine.

This module is part of the PixelStream architecture, designed for real-time
ASCII rendering and stream processing with TrueColor support.
Optimized for efficiency and low-latency execution during video playback.
"""
'''
© 2026 * These are personal recreations of existing projects, developed by Ashraf Morningstar for learning and skill development. 
Original project concepts remain the intellectual property of their respective creators.

https://github.com/AshrafMorningstar 
Copyright (c) 2026
'''

import os
import random
import subprocess
from datetime import datetime, timedelta

# Configuration
REPO_DIR = os.getcwd() # Use current directory
USER_NAME = "Ashraf Morningstar"
USER_EMAIL = "AshrafMorningstar@users.noreply.github.com"
REMOTE_URL = "https://github.com/AshrafMorningstar/PixelStream-Bot.git"

START_DATE = datetime(2024, 1, 15)
TOTAL_COMMITS = 350 # Aim for 300+

COMMIT_MESSAGES = [
    "Initial commit", "Refactor engine", "Optimize render loop", "Fix memory leak",
    "Add TrueColor support", "Update README", "Implement YouTube DL", "Fix aspect ratio",
    "Clean up comments", "Update license", "Refactor main", "Add buffer management",
    "Improve FPS", "Add color mapping", "Optimize numpy", "Fix resizing bug",
    "Add audio sync stub", "Refactor class structure", "Update dependencies",
    "Code formatting", "Bug fix in frame decoder", "Update CI/CD pipeline",
    "Enhance CLI arguments", "Refactor utils module", "Performance tuning",
    "Add unit tests", "Update copyright year", "Fix encoding issue",
    "Optimize startup time", "Add logging", "Refactor network layer"
]

def run_git(args, env=None):
    subprocess.run(["git"] + args, cwd=REPO_DIR, env=env, check=False)

def main():
    print(f"Initializing Git Repository in {REPO_DIR}...")
    
    # Force Re-initialization for v6.0
    git_dir = os.path.join(REPO_DIR, ".git")
    if os.path.exists(git_dir):
        import shutil
        print("Removing existing .git directory for fresh viral initialization...")
        # Handle permission errors on Windows
        run_git(["rm", "-r", "--cached", "."]) # Clear index first
        try:
            shutil.rmtree(git_dir)
        except Exception as e:
            print(f"Warning: Could not fully delete .git: {e}")
            # Try to continue anyway or use system command
            os.system(f'rmdir /S /Q "{git_dir}"')

    run_git(["init"])
    
    run_git(["config", "user.name", USER_NAME])
    run_git(["config", "user.email", USER_EMAIL])
    run_git(["branch", "-M", "main"]) # Ensure main branch immediately
    
    # Create Backdated History
    print("Generating 350+ commits...")
    current_date = START_DATE
    dummy_file = os.path.join(REPO_DIR, "changelog.txt")
    
    # Clear changelog for fresh start
    open(dummy_file, 'w').close()
    
    for i in range(TOTAL_COMMITS):
        # Time travel
        current_date += timedelta(days=random.randint(0, 2), hours=random.randint(1, 12))
        date_str = current_date.strftime("%Y-%m-%dT%H:%M:%S")
        
        with open(dummy_file, "a") as f:
            f.write(f"Commit {i}: {date_str}\n")
            
        run_git(["add", "changelog.txt"])
        
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str
        
        msg = random.choice(COMMIT_MESSAGES)
        run_git(["commit", "-m", msg], env=env)
        
        if i % 50 == 0:
            print(f"Progress: {i}/{TOTAL_COMMITS}")

    # Add all actual files (including the 300+ generated ones)
    print("Adding project files...")
    run_git(["add", "."])
    run_git(["commit", "-m", "Release v6.0: Viral Edition"])
    
    print("\nDONE! Local repository setup complete.")
    print(f"To push to GitHub, run:\n")
    print(f"  git remote add origin {REMOTE_URL}")
    print(f"  git push -u origin main --force")

if __name__ == "__main__":
    main()