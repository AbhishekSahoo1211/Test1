import git
import requests

# Configuration
GITHUB_TOKEN = 'your_github_token_here'
REPO_URL = 'https://github.com/yourusername/your-repo.git'
EXISTING_BRANCH = 'main'  # Branch to clone
NEW_BRANCH = 'new-feature-branch'
OWNER = 'yourusername'
REPO_NAME = 'your-repo'

# Clone the repository
repo = git.Repo.clone_from(REPO_URL, 'temp_repo')

# Checkout the existing branch
repo.git.checkout(EXISTING_BRANCH)

# Create a new branch from the existing one
repo.git.checkout('-b', NEW_BRANCH)

# Push the new branch to the remote repository
repo.git.push('--set-upstream', 'origin', NEW_BRANCH)

# Fetch existing branch protection rules
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}
branch_protection_url = f'https://api.github.com/repos/{OWNER}/{REPO_NAME}/branches/{EXISTING_BRANCH}/protection'
response = requests.get(branch_protection_url, headers=headers)

if response.status_code == 200:
    protection_rules = response.json()
else:
    print(f"Failed to fetch protection rules: {response.status_code} {response.text}")
    protection_rules = None

# Set the same protection rules on the new branch
if protection_rules:
    new_branch_protection_url = f'https://api.github.com/repos/{OWNER}/{REPO_NAME}/branches/{NEW_BRANCH}/protection'
    response = requests.put(new_branch_protection_url, headers=headers, json=protection_rules)
    
    if response.status_code == 200:
        print(f"Branch protection rules applied to {NEW_BRANCH}.")
    else:
        print(f"Failed to apply branch protection rules: {response.status_code} {response.text}")

# Clean up the temporary repository
repo.close()
