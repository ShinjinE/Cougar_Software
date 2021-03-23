# Cougar_Software
Will be used to collaborate and share all code for each section of the overall cougar system

# Github Directory Setup
First open a bash terminal then cd into whatever folder you want to keep all the code then run:
	git init
	git remote add [remote-name] [URL]
	git fetch [remote-name]
	git checkout [remote-branch-name]
Note: The remote-name does not need to match any existing name. Typical names used include "origin" and "upstream".

An example for the above:
	git init
	git remote add origin https://github.com/ShinjinE/Cougar_Software.git
	git fetch origin
	git checkout BrainPi

If a new branch is being created, the folling command can be used:
	git checkout -b [local-branch-name] [remote-name]/[remote-branch-name]
Note: The local branch name doesn't need to match anything, but the remote branch needs to match a branch name in the remote git repository

To send changes to the online repository, use the folling commands:
	git add .
	git commit -m "[commit description, not past tense]"
	git push
Note 1: The "." for the add command is used to add all changed files to the commit. A specific filename can be used if desired.
Note 2: When pushing commits for the first time after initializing, your github username and password need to be entered.

If the github branch hasn't been used yet, the following must be entered before changes can be committed:
	git config --global user.email "{you@example.com}"
	git config --global user.name "{Your Name}"