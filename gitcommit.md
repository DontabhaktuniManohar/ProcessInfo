
This is an alternative way of fixing your commit messages if you are not familiar or facing issues with the git rebase command. Git Soft Reset to your original/first/oldest commit will get rid of all the commit messages that followed it but keep the actual changes
# Always pull changes from remote first. Use --rebase to avoid any additional commit messages (only do this on non-master/release branches since it git pull --rebase
# reset to your base commit. Example: I
git logoneline -n 4
16d9d63 (HEAD->feature/fixing-multiple-commit-demo) My BaD Commit ff17dc6 fix(hello): correct typo
711f3ba my-bad-commit
2e97727 (origin/master, origin/HEAD, master) test: use squash strategy
HEAD or topmost commit in your feature branch
------> Base or first commit you made in your feature branch Master branch
# Get rid of all commit messages after 711f3ba, but keep the actual changes git reset soft 711f3ba
# You will see that the files changes in the commits that were reset will show up as staged git status
rate your changes in the base commit. Also fix the commit message 'my-bad-commit' of the base commit 711f3ba since it doesn't follow the standards git commit amend -m 'feat: add foo'
# you need to force push because reset command re-writes the commit history git push -f
Like 8 people like this
commitlint best-practice git
