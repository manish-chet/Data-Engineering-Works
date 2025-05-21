**Git Fundamentals and Setup**

*   **What Git is:** Git is a Version Control System ``. Specifically, it's a **distributed** Version Control System ``. It was written by Linus Torvalds (creator of Linux) in 2005 in just 5 days ``. Today, it is the **de facto standard for all developers** ``. Git allows you to **track code changes over time by author** with a set of commands to search, manipulate, and revert history ``.
*   **Git vs. Hosting Services:** When the term "Git" is used in the course, it does not refer to companies like GitHub, GitLab, or Stash ``. These companies **use Git** but are not Git itself ``. GitHub is described as a product by Microsoft that hosts Git repositories and is a way for them to make money and collect data ``. Forking and Pull Requests are features offered by these hosting services, not core Git operations ``.
*   **Git Usage:** 93% of developers use Git, which the speaker feels is low because 100% of developers they've worked with use it ``. Git has a very strong hold on the Version Control industry ``.
*   **Git Documentation:** One of the best parts of Git is that all the documentation is fantastic ``. You can access it using the `man` command, like `man git` or `man git tag` ``.
*   **Git Configuration (`git config`):**
    *   You need to configure Git with your information (name and email) whenever you code ``.
    *   Git configuration is stored in a file, either in **global space** (your home directory) or within your `.git` folder ``.
    *   You can set configuration values using `git config --global <key> <value>` ``.
    *   You can list configuration values using `git config list` or `git config list --local` or `git config list --global` ``.
    *   You can set the **default branch** using `git config --global init.defaultBranch <branch-name>` ``. While the default used to be `master`, many people and platforms like GitHub have updated it to `main` ``. It's recommended to use `main` if you primarily work with GitHub ``. You can also set this configuration at a local level for a specific repository ``.
    *   Example commands shown: `git config list --local`, `git config list --global`, `git config add --global init.defaultBranch main` ``.
*   **Creating a Repository (`git init`):**
    *   The first step of any project is to create a Git repository, or repo ``. A repo represents a single project, and you typically have one repo per project ``.
    *   A repo is just a directory containing project files, but it also includes a **hidden `.git` directory** ``.
    *   The `.git` directory is literally the **entire state of your Git project** ``. Everything about the repo, including branches and commits, is stored there ``.
    *   The command `git init` creates this new, empty `.git` directory ``.
    *   Example: Navigate to a directory (e.g., `webflix`), run `git init`, and you will see a `.git` folder when listing hidden files (`ls -la`) ``.

**Working with Files and Commits**

*   **File States:** A file in a Git repository can be in several states ``:
    *   **Untracked:** Git doesn't know about this file yet. It has never been added to the index (staging area) or tracked ``. If you delete an untracked file, you lose its content ``.
    *   **Staged:** The file has been added to the staging area, ready to be included in the next commit ``.
    *   **Committed:** The changes in the file have been saved as a snapshot in the repository's history ``.
*   **Checking Status (`git status`):** The `git status` command shows you the current state of your repo, including which files are untracked, staged, or modified ``.
*   **Staging Changes (`git add`):** The `git add <file>` command adds a file (or changes to a file) to the staging area ``. This is the command to add a file to the index ``.
    *   Example: After creating a file like `contents.md`, `git status` shows it as untracked. Running `git add contents.md` moves it to the staged state ``.
*   **Committing Changes (`git commit`):**
    *   A commit is a **snapshot of the repository at any given time** ``.
    *   Git **does not store diffs** (differences) per commit ``. Instead, it stores the **entire history per commit**, meaning your entire project state is in a single commit ``. More accurately, it stores **references** to the entire state ``.
    *   Commits are tied to an author, time of day, and other information ``.
    *   The command `git commit -m "<message>"` creates a new commit with the staged changes and the provided message ``. Commit messages often start with a capitalized letter ``.
    *   Example: After staging `contents.md`, run `git commit -m "Add contents"` to save it as a commit ``. `git status` will then show a clean working tree ``.
    *   You can add many commits to the graph ``.
*   **Viewing History (`git log`):** The `git log` command shows the commit history ``.
    *   `git log --oneline` shows each commit on a single line with a shortened hash ``.
    *   `git log -p` shows the diff (changes introduced) by each commit ``.
    *   `git log --graph --decorate --oneline --parents` is a useful combination to visualize the commit graph, branches, and parent relationships ``.
*   **Plumbing vs. Porcelain Commands:** Some Git commands are considered "plumbing" (low-level, internal) and others "porcelain" (high-level, user-friendly) ``. You use porcelain commands like `git log` more often, but plumbing commands like `git cat-file` are useful for understanding Git's internals ``.

**Git Internals: Objects**

*   Git stores its data as objects. Two important object types are:
    *   **Blob:** A way of storing a **file** ``.
    *   **Tree:** A way of storing a **directory** ``.
*   **Viewing Object Contents (`git cat-file -p`):**
    *   The plumbing command `git cat-file -p <hash>` allows you to see the contents of a Git object (like a commit, tree, or blob) without needing to fuss with the raw files ``. The `-p` flag pretty-prints the object ``.
    *   Example 1: Using `git cat-file -p <commit-hash>` on a commit shows the author, message, and a reference to a **tree object** ``.
    *   Example 2: Using `git cat-file -p <tree-hash>` on that tree object shows entries for files (blobs) and directories (other trees) within that snapshot, each with their own hash ``.
    *   Example 3: Using `git cat-file -p <blob-hash>` on a blob object shows the actual content of the file at that commit ``.
*   **How Git Stores Snapshots (Mind Blown Moment):** Git stores an entire snapshot of files on a per-commit level ``. When a commit references a file that hasn't changed since the parent commit, it doesn't store the file content again; it stores a **pointer** to the *same* blob object hash that the parent commit used ``. This is why it's efficient ``. If a tree (directory) hasn't changed, it can point to the *same* tree object hash as the parent ``.
    *   Analogy: Commit A points to Tree 1 (representing directory state). Tree 1 points to Blob X (contents file). Commit B adds a new file. It points to Tree 2. Tree 2 points to the *same* Blob X (for contents) and a *new* Blob Y (for the new file). Tree 2 has a different hash than Tree 1 because its contents (the list of files/blobs it points to) changed, but it reuses the hash for Blob X because the file content didn't change ``.

**Branching and Merging**

*   **Branches:** A branch is literally just a **pointer to a commit** ``. Because they are just pointers, branches are **lightweight and cheap** to create ``.
    *   `git branch` lists existing branches and shows which one you are currently on ``.
*   **Tips:** The "tip" of a branch is the **latest commit** on that branch ``.
*   **Merge Base:** The merge base, also called the **best common ancestor**, is the nearest commit that is an ancestor to **both** branches involved in a merge or rebase ``.
*   **Switching Branches (`git switch` / `git checkout`):**
    *   `git switch <branch-name>` is the newer, recommended command for simply changing branches ``.
    *   `git checkout <branch-name>` is an older command that can also switch branches, but it's less intuitive as it's used for many other things (like restoring files or resolving merge conflicts) ``. The course primarily uses `git switch` but notes older developers often use `git checkout` ``.
    *   `git switch -c <new-branch-name>` creates a new branch and switches to it ``.
*   **Diverging Branches:** Branches diverge when new commits are added to each branch independently after they split from a common ancestor (the merge base) ``.
*   **Merging (`git merge`):** Merging combines the history from one branch into another ``.
    *   When merging two branches with diverging history, Git finds the **merge base** ``.
    *   It then combines the changes from the commits on both branches (since the merge base) into a new commit ``.
    *   This new commit is called a **merge commit** ``.
    *   A merge commit is unique because it's the **only commit with two parents** (one pointing to the tip of each branch being merged) ``.
    *   Example: Merging a branch `add-classics` (which diverged from `main` at commit A and has commit D) onto `main` (which has commits B and C after A, and E after C) results in a merge commit (F) on `main` with parents C (from `main`) and D (from `add-classics`) ``.
    *   Command: `git merge <branch-to-merge-in>` ``.
*   **Fast Forward Merge:** This is the simplest type of merge ``. It happens when the tip of the branch you are merging *onto* is also the merge base ``. In this case, there's no diverging history on the target branch, so Git simply moves the pointer of the target branch forward to the tip of the branch being merged in ``. **No merge commit with two parents is created** ``.
    *   Example: If you are on `main` and merge a branch `feature` where `feature` was created off `main` and only added new commits sequentially, Git can fast-forward `main`'s pointer to the latest commit of `feature` ``.
*   **Advantages/Disadvantages of Merge:**
    *   **Advantage:** Preserves the **true history** of the project, showing where branches happened and merged ``.
    *   **Disadvantage:** Can create many merge commits, making history harder to read and understand ``.

**Rebasing**

*   **Rebase (`git rebase`):** Rebasing is different from merging; it **rewrites history** ``.
    *   When you rebase branch `feature` onto branch `main`, Git finds the merge base, moves the tip of `feature` back to the merge base, and then **replays** the commits from `feature` one by one on top of the current tip of `main` ``.
    *   This creates **new commit objects** for the changes from `feature`, effectively making it look as if `feature` branched off of the latest commit of `main` ``. The original commits from `feature` are no longer part of the history of the rebased branch ``.
    *   Command: `git rebase <target-branch>` (when on the branch you want to rebase) ``. Example: `git rebase main` (while on `band` branch) replays `band`'s commits onto `main` ``.
*   **Advantages/Disadvantages of Rebase:**
    *   **Advantage:** Creates a **linear history** that is generally easier to read, understand, and work with ``. This can be useful when preparing commits from a feature branch for a pull request ``.
    *   **Disadvantage:** **Rewrites history**, which can be problematic for collaborative branches ``.
*   **Important Warning:** **You should NEVER rebase a public branch** like `main` ``. If you do this, when others try to pull, their histories will be out of sync, leading to conflict problems ``. It is generally okay to rebase **your own private branch** on top of a public branch ``.

**Handling Conflicts**

*   Conflicts happen when changes are made to the **same lines of code** in different commits that Git tries to combine (merge or rebase), and Git cannot automatically figure out which change to keep ``.
*   Git inserts conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) into the file ``.
*   **Resolving Conflicts:** You need to manually edit the file to remove the conflict markers and keep the desired code ``.
*   **`git checkout --ours` and `git checkout --theirs`:** These commands can help resolve conflicts during both merging and rebasing ``.
    *   During a **merge**, `ours` refers to the changes on the branch you are currently on (where you ran `git merge`), and `theirs` refers to the changes on the branch you are merging *in* ``.
    *   During a **rebase**, you need to think in reverse: `theirs` represents the changes from the branch being rebased (the commits being replayed), which in reality are *your* changes on that branch. `ours` represents the changes from the target branch (the one being rebased onto, e.g., `main`) ``. So, during a rebase, `git checkout --ours` keeps the changes from the target branch (e.g., `main`), and `git checkout --theirs` keeps the changes from the branch being rebased (e.g., `band` branch changes being replayed) ``.
    *   Example: During a merge conflict, `git checkout --ours <file>` will use the version of the file from your current branch ``. `git checkout --theirs <file>` will use the version from the branch you are merging in ``.
*   After manually editing or using `git checkout` to resolve conflicts, you must `git add` the file to stage the resolution and then continue the merge or rebase ``.
    *   For merge: After staging, `git commit` completes the merge commit ``.
    *   For rebase: After staging, `git rebase --continue` continues the rebasing process ``.
*   **Resolving Conflicts in Editor:** Many code editors (like VS Code) have UI features to help resolve conflicts, often labeled "Accept incoming changes" (like `theirs` in a merge) and "Accept current changes" (like `ours` in a merge) ``.
*   **`git rerere` (Reuse Recorded Resolution):** This is a hidden feature (from `git help rerere`) that, if enabled, allows Git to **remember how you resolved a hunk conflict** ``. The next time it sees the *same* conflict, Git can **resolve it automatically** ``. This applies to both rebasing and merging ``.

**Undoing Changes**

*   **Git Reset (`git reset`):** Used to undo the last commits or changes in the index or working tree ``. It can move the branch pointer back to a previous commit ``.
    *   `git reset --soft <commit>`: Goes back to a previous commit but **keeps all of your changes**. Committed changes will be uncommitted and staged, while uncommitted changes remain as they were ``. The working directory and staging area are left untouched ``.
        *   Example: `git reset --soft HEAD~1` undoes the last commit, leaving its changes staged ``. This is useful if you want to redo the last commit or fix a commit message before it's pushed publicly ``. It's also useful for fixing mistakes during rebase or cherry-pick ``.
    *   `git reset --hard <commit>`: Goes back to a previous commit and **discards all changes** made after that commit in both the staging area and the working directory ``. All changes made *after* the target commit are lost from your working files ``.
        *   Example: `git reset --hard <commit-hash>` or `git reset --hard HEAD~1` ``.
    *   **Danger of `git reset --hard`:** If you have unstaged or staged changes that were never committed and you run `git reset --hard`, those changes will be **deleted for good** from your working tree ``. Untracked files (files Git doesn't know about) are **not** removed by `git reset --hard` ``.
    *   While `git reset --hard` loses changes from the working tree and index, the commit objects themselves are often still recoverable using `git reflog` ``.
*   **Git Revert (`git revert`):** Used to undo the changes introduced by a specific commit ``.
    *   It creates a **NEW commit** that is the **inverse** of the commit being reverted ``.
    *   This preserves the project's history, showing that the original commit happened and then a subsequent commit undid its changes ``.
    *   Command: `git revert <commit-hash>` ``. Git will often prompt you to edit the commit message for the new revert commit ``.
    *   Example: `git revert <hash>` creates a new commit that contains changes opposite to those in the specified commit ``. `git log -p` can show the inverse nature of the changes ``.
*   **Git Reflog (`git reflog`):**
    *   Keeps a **record of where the HEAD has been** ``.
    *   This is extremely useful for recovering commits or states that seem lost (e.g., after a hard reset, rebase, or deleting a branch) because the commit objects still exist and are referenced in the reflog ``.
    *   Example: If you accidentally delete a branch containing a unique commit, `git reflog` will show the history of your HEAD movements, including the hash of the "lost" commit ``. You can then use plumbing commands like `git cat-file` or even merge/cherry-pick from the reflog hash to recover the changes ``.
*   **Git Commit Amend (`git commit --amend`):**
    *   Allows you to change the **last commit's commit message** ``.
    *   You can also stage additional changes before running `git commit --amend` to add them to the last commit ``.
    *   Warning: This is a **destructive, history-altering item** because it changes the SHA hash of the last commit ``. Do not amend commits that have already been pushed to a public branch ``.
    *   Example: If you just committed and immediately realize the message is wrong, `git commit --amend` opens the editor to change the message for that last commit ``.

**Remotes and Collaboration**

*   **Remote Repositories (Remotes):** Remotes are just **other repos** ``. A repo is a collection of commits; a branch is just a pointer to a commit within a repo ``.
*   **Distributed Version Control:** Git is distributed ``. This means **one repo is not inherently the authoritative source**; every repo is its own repo, and you sync between them ``. You can have many authoritative repos, but typically teams use one (like a GitHub repo) for easy pulling and pushing ``.
*   **Origin:** When you clone a repository, Git automatically sets up a remote named `origin` that points back to the repository you cloned from ``. This is the conventional name for the primary remote ``.
*   **Adding a Remote (`git remote add`):** You can add other remotes to your local repository using `git remote add <name> <url>` ``.
    *   Example: `git remote add origin <your-github-repo-url>` ``.
*   **Listing Remotes (`git remote -v`):** Shows the names and URLs of your configured remotes ``.
*   **Fetching Changes (`git fetch`):** Downloads commits, files, and references from a remote repository into your local repository ``. It **does not** automatically merge or modify your current working branches ``. It updates the remote-tracking branches (e.g., `origin/main`) in your local repo ``.
    *   Example: `git fetch origin` downloads changes from the `origin` remote ``.
*   **Pulling Changes (`git pull`):** A shortcut that is typically equivalent to running `git fetch` followed by `git merge` `[?]`. It fetches changes from a remote and integrates them into your current local branch `[?]`.
*   **Pushing Changes (`git push`):** Uploads your local commits to a remote repository ``.
    *   Example: `git push origin main` pushes the `main` branch to the `origin` remote ``.
*   **Forking (GitHub/Hosting Feature):** A fork is a **copy of an original repository** on a hosting service like GitHub ``. You create a fork in your own account ``. Forking is **not a Git command-line operation**; it's a feature of the hosting service ``.
    *   Purpose: It allows you to modify the project without affecting the original repository, which is the standard way to contribute to open-source projects where you don't have push access to the main repo ``.
    *   Workflow for Contribution: Fork the repo on the hosting service -> Clone *your fork* to your local machine -> Create a branch -> Make changes -> Commit -> Push changes to *your fork* -> Open a Pull Request from your fork's branch to the original repo's branch ``.
*   **Upstream Remote:** When cloning your fork, it's common to add a second remote, conventionally named `upstream`, that points to the original repository you forked from ``. This allows you to easily fetch and pull in changes from the original repo (`upstream`) into your fork (`origin`) so you are working on the latest version and avoid conflicts when submitting contributions ``.
    *   Example: `git remote add upstream <original-repo-url>` ``.
*   **Pull Request (GitHub/Hosting Feature):** A mechanism offered by hosting services (like GitHub) to propose changes from one branch (e.g., your feature branch on your fork) to another branch (e.g., `main` on the original repo) ``. It allows for discussion and code review before the changes are merged ``. You cannot do a pull request directly *in Git* because Git doesn't know about GitHub's features ``.

**Ignoring Files**

*   **Git Ignore (`.gitignore`):** A file (typically placed at the root of the repository) that lists files or patterns of files that Git should **ignore** and not track ``. This is crucial for things like generated files (e.g., build outputs, logs) or dependency directories (e.g., `node_modules`) ``.
*   **Syntax:**
    *   Each line is a pattern ``.
    *   Blank lines or lines starting with `#` are ignored as comments ``.
    *   Standard shell wildcards like `*` (matches zero or more characters) can be used ``.
    *   Patterns starting with `/` are anchored to the directory containing the `.gitignore` file ``.
    *   You can **negate** a pattern by prefixing it with an exclamation mark (`!`) ``. This is useful to ignore an entire directory but include a specific file within it ``.
    *   Example: `node_modules/` ignores the `node_modules` directory ``. `*.html` ignores all HTML files ``. `/main.py` ignores `main.py` in the same directory as the `.gitignore` file, but not in subdirectories ``. `/secure/*` ignores everything directly inside the `secure` directory ``. `/secure/` ignores the directory and its contents recursively ``. `!.gitignore` might negate a previous ignore rule for `.gitignore` ``.
*   **Placement:** `.gitignore` files do not necessarily have to be at the root of the project; you can have multiple `.gitignore` files in different directories ``. Rules in a `.gitignore` file apply to that directory and its subdirectories ``. This is useful for things like monorepos ``.

**Advanced Commands**

*   **Git Squash (`git squash`):** Not a command itself, but a common action performed using interactive rebase (`git rebase -i`) ``. It allows you to **combine multiple commits into a single new commit** ``. This is often done on feature branches before merging or creating a pull request to maintain a cleaner, linear history on the main branch ``.
    *   Example: Using `git rebase -i HEAD~<number-of-commits>` opens an editor where you can mark commits to `pick` (keep) or `squash` (combine into the previous commit) ``.
*   **Git Stash (`git stash`):** Saves changes in your working directory and staging area temporarily without committing them, allowing you to switch to a clean working directory ``.
    *   `git stash` saves the current changes onto a stack ``.
    *   `git stash list` shows the list of stashed changes ``.
    *   `git stash pop` applies the most recent stash and removes it from the stack ``.
    *   `git stash drop` removes the most recent stash from the stack ``.
    *   You can add messages to stashes: `git stash save "<message>"` or the newer `git stash push -m "<message>"` ``.
*   **Git Cherry-pick (`git cherry-pick`):** Applies the changes introduced by a **specific commit** from one branch onto another branch ``. It creates a **new commit** on the target branch that contains the same changes as the picked commit ``.
    *   Requirement: A clean working tree (no uncommitted changes) on the target branch ``.
    *   Command: `git cherry-pick <commit-hash>` (while on the branch you want to apply the commit to) ``.
    *   Example: `git cherry-pick <hash-of-commit-O>` while on `main` will apply the changes from commit O to `main` by creating a new commit ``.
*   **Git Bisect (`git bisect`):** A debugging tool that uses a **binary search** algorithm to find the commit that introduced a bug ``.
    *   Workflow: Start bisecting (`git bisect start`) -> Mark the current (buggy) commit as bad (`git bisect bad`) -> Mark a known good commit (`git bisect good <good-commit-hash>`) ``.
    *   Git then checks out a commit roughly in the middle of the good and bad range ``. You test if the bug is present ``.
    *   If the bug is present, mark the commit as bad (`git bisect bad`); if not, mark it as good (`git bisect good`) ``.
    *   Git continues checking out middle commits based on your good/bad input until it narrows down to the single commit that introduced the bug ``.
    *   Exit bisect mode with `git bisect reset` ``.
    *   Analogy: Like finding a number in a sorted array using binary search ``.
*   **Git Worktree (`git worktree`):** Allows you to have **multiple working directories connected to the same repository** ``. Each worktree can have a different branch checked out ``.
    *   Command: `git worktree add <path> <branch>` creates a new linked worktree at the specified path with the specified branch checked out ``.
    *   `git worktree list` shows all working trees for the repository ``.
    *   The main working directory stores references to the linked worktrees in the `.git/worktrees` directory ``.
    *   Restriction: You **cannot** work on a branch that is currently checked out by another worktree ``.
*   **Git Tag (`git tag`):** Used to mark specific points in history as important ``.
    *   A tag is an **immutable pointer to a commit** ``. You cannot edit a tag ``.
    *   `git tag` lists existing tags ``.
    *   `git tag <tag-name> <commit-hash>` creates a tag pointing to a specific commit. If no hash is given, it tags the HEAD commit ``.
    *   `git tag -a <tag-name> -m "<message>"` creates an **annotated tag** which includes metadata like the tagger name, email, and date, and a tagging message ``.
    *   When you `git checkout <tag-name>`, you enter a **detached HEAD** state because tags are immutable and you can't commit directly on them ``.
    *   Typical Use: Tags are commonly used to mark **release versions** (e.g., v1.0.0, v2.1.3) using Semantic Versioning (Sver) ``.

