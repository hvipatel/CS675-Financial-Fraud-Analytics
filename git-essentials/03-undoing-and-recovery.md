# Undoing & Recovery

Mistakes happen. Git lets you undo almost anything — edits, commits, even commits you thought you destroyed. The only rule to remember: **`reset` rewrites history (don't use on shared branches), `revert` adds new history (always safe).**

## Discard unsaved edits to a file

You messed up a file but haven't staged or committed yet:

```bash
$ echo "broken nonsense" >> README.md
$ git restore README.md
$ git status
nothing to commit, working tree clean
```

The file is back to its last committed state.

## Unstage a file (keep your edits)

You added something you didn't mean to include:

```bash
$ git add secret.env
$ git restore --staged secret.env
$ git status
Untracked files:
        secret.env
```

The file is no longer staged, but your changes to it remain.

## Undo your last commit, keep the work

You committed too early — wrong message, or you want to split it into smaller commits:

```bash
$ git reset --soft HEAD~1
$ git status
Changes to be committed:
        modified:   features.py
```

The commit is gone, but everything is staged — recommit it however you want. `HEAD~1` means "one commit before HEAD". `HEAD~2` is two before, etc.

## Throw away the last commit AND its changes

```bash
$ git reset --hard HEAD~1
HEAD is now at 1a9e3c2 Describe project
```

Destructive — but recoverable via `reflog` (below) for ~30 days.

## Undo a commit that's already pushed

You can't safely rewrite shared history. Add a new commit that reverses the bad one:

```bash
$ git revert 7d2a4f1
[main 4b8e1f3] Revert "Try x_squared feature"
```

Both commits are now in history: the original and the one that undoes it. Collaborators stay happy.

## Stash work in progress

You're mid-edit when you need to switch branches:

```bash
$ git status
        modified:   features.py

$ git stash
Saved working directory and index state WIP on main: 1a9e3c2 Describe project

$ git switch main           # do the urgent thing
$ git switch experiment/foo
$ git stash pop
On branch experiment/foo
Changes not staged for commit:
        modified:   features.py
```

`git stash list` shows all stashes if you've made several.

## Recover a "lost" commit with reflog

Even after `reset --hard`, commits live for ~30 days. The reflog tracks every move HEAD has made:

```bash
$ git reflog
1a9e3c2 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~1
b8d3e10 HEAD@{1}: commit: Broken experiment
1a9e3c2 HEAD@{2}: pull: Fast-forward
```

Get the lost commit back:

```bash
$ git reset --hard b8d3e10
HEAD is now at b8d3e10 Broken experiment
```

If you committed it, you can probably recover it. If you only edited it (never committed), it's gone.

> **Next:** [Remotes & Collaboration](./04-remotes-and-collaboration.md)
