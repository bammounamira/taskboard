# Checkpoint 0 — answer

**Why must `.gitignore` exist before the first `git add .`?**

`git add .` stages every file that is not ignored. If `.gitignore` does not exist yet, files such as `.env`, private keys, `.venv/` or `__pycache__/` get staged and then committed. Once committed, a secret stays in the Git history even if the file is deleted in a later commit: anyone who clones the repository can recover it with `git log -p`. Removing it requires rewriting history (and the secret must be considered leaked and rotated anyway). Adding `.gitignore` afterwards does not help either, because it only affects untracked files — already-tracked files keep being tracked.
