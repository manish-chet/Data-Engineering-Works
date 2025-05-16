# Learn Git – The Full Course

This document is based on the Boot.dev YouTube video "[Learn Git - The Full Course](https://www.youtube.com/watch?v=rH3zE7VlIMs)". It breaks down the video into digestible concepts with explanations and command examples.

---

## 1. Introduction to Git

Git is a distributed version control system that lets multiple developers collaborate while maintaining a complete history of changes.

**Key Concepts:**
- Version control
- Snapshots (not differences)
- Local vs. remote

---

## 2. Setting Up Git

Configure your identity so Git can associate commits with your name and email.

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```


Check your config:

```bash
git config --list
```

---

## 3. Repositories

A repo is essentially just a directory that contains a project (other directories and files). The only difference is that it also contains a hidden .git directory. That hidden directory is where Git stores all of its internal tracking and versioning information for the project.
### Initialize a repository

```bash
git init
```

### Clone a repository

```bash
git clone https://github.com/user/repo.git
```

---

## 4. Git Internals

Git uses:
- **Commits**: snapshots of your code
- **Branches**: movable pointers to commits
- **HEAD**: pointer to your current branch

A file can be in one of several states in a Git repository. Here are a few important ones:
- untracked: Not being tracked by Git
- staged: Marked for inclusion in the next commit
- committed: Saved to the repository's history
The git status command shows you the current state of your repo. It will tell you which files are untracked, staged, and committed


Check HEAD:

```bash
cat .git/HEAD
```

---

## 5. Configuration

Set editor:

```bash
git config --global core.editor "code --wait"
```

Set default branch name:

```bash
git config --global init.defaultBranch main
```

---

## 6. Branching

Create a new branch:

```bash
git branch feature-xyz
```

Switch to it:

```bash
git checkout feature-xyz
```

Or both at once:

```bash
git checkout -b feature-xyz
```

List branches:

```bash
git branch
```

---

## 7. Merging

Merge a branch into your current one:

```bash
git merge feature-xyz
```

If conflicts arise, Git will mark them in the file and you must resolve them manually.

---

## 8. Rebasing

Rebase your branch onto main:

```bash
git checkout feature-xyz
git rebase main
```

Interactive rebase to clean up commits:

```bash
git rebase -i HEAD~3
```

---

## 9. Resetting

Soft reset:

```bash
git reset --soft HEAD~1
```

Mixed reset (default):

```bash
git reset --mixed HEAD~1
```

Hard reset (dangerous):

```bash
git reset --hard HEAD~1
```

---

## 10. Remote Repositories

Add a remote:

```bash
git remote add origin https://github.com/user/repo.git
```

Push to remote:

```bash
git push origin main
```

Pull from remote:

```bash
git pull origin main
```

---

## 11. GitHub Integration

GitHub is a platform that hosts Git repositories.

Typical flow:
- Push feature branch
- Create Pull Request (PR)
- Review & merge PR

---

## 12. .gitignore File

The `.gitignore` file tells Git what to ignore.

Example:

```
# Node modules
node_modules/

# Logs
*.log

# Environment variables
.env
```

---

## Conclusion

This guide walks through the essential Git concepts and commands demonstrated in Boot.dev’s Git course. Mastering Git will improve your productivity, collaboration, and confidence as a developer.

📺 Watch the video: [Learn Git - The Full Course](https://www.youtube.com/watch?v=rH3zE7VlIMs)
