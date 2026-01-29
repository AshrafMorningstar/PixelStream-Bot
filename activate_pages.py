'''
© 2026 * These are personal recreations of existing projects, developed by Ashraf Morningstar for learning and skill development. 
Original project concepts remain the intellectual property of their respective creators.

https://github.com/AshrafMorningstar 
Copyright (c) 2026
'''

import urllib.request
import json
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") # Securely load from environment
USER_NAME = "AshrafMorningstar"
REPO_NAME = "PixelStream-Bot"

def activate_pages():
    url = f"https://api.github.com/repos/{USER_NAME}/{REPO_NAME}/pages"
    
    data = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"✅ GitHub Pages ACTIVATED for {REPO_NAME}!")
            print(f"🌐 Live URL: https://{USER_NAME}.github.io/{REPO_NAME}/")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 409:
            print(f"⚠️ GitHub Pages already enabled.")
            print(f"🌐 Live URL: https://{USER_NAME}.github.io/{REPO_NAME}/")
            return True
        else:
            print(f"❌ Failed to activate Pages: {e}")
            print(e.read().decode())
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    activate_pages()
