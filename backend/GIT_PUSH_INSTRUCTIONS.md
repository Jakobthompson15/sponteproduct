# Git Push Instructions

The backend code is ready and committed locally. Now you need to push it to GitHub.

## Commands to Run

Open your terminal and run these commands:

```bash
cd /Users/jakobthompson/Desktop/personal/rankingme/backend

# Verify git status
git status

# Check that origin is set
git remote -v

# Push to GitHub (you'll be prompted for your GitHub credentials)
git push -u origin main
```

## If You Get Authentication Errors

### Option 1: Use GitHub Personal Access Token (Recommended)

1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` permissions
3. Copy the token (save it somewhere safe)
4. When prompted for password, paste the token instead

### Option 2: Use SSH

```bash
# Change remote URL to SSH
git remote set-url origin git@github.com:Jakobthompson15/spontebackend.git

# Push
git push -u origin main
```

### Option 3: Use GitHub CLI

```bash
# Install GitHub CLI if you haven't: brew install gh
gh auth login

# Then push
git push -u origin main
```

## Verify Push Was Successful

After pushing, visit:
https://github.com/Jakobthompson15/spontebackend

You should see all your backend files there!

## Next Steps After Pushing

Once the code is on GitHub, we can:
1. Connect Railway to the GitHub repo
2. Deploy to production
3. Test the live API
4. Update the frontend to connect to it
