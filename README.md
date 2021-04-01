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

	git config --global user.email "[you@example.com]"
	git config --global user.name "[Your Name]"

# Merging Updates on Master to a Branch
When a commit is sent from a local repository (on your computer) to the remote repository branch (on the internet), Github will prompt to merge the branch with Master. However, no such prompt is ever provided to do so for merging the updates to the Master into the branches. In order to do this a pull request on the online repository must be made in order to keep the upstream remote branches for each user's local branch up to date. The following are the step by step instructions to do so:
1. Go to the main page https://github.com/ShinjinE/Cougar_Software
2. Above the file directory, left click the "Pull request" option
3. Left click the green "New pull request" button
4. This should take you to a page with two drop down menus. The one on the left says "base: master" and on the right it says "compare: master" with an arrow pointing from compare to base. Change the base drop down from master to the desired branch to merge updates to. Lets say you were wanting to merge updates to the BrainPi branch, then the result would look like "[base: BrainPi] <- [compare: master]".
5. After the base is selected, the webpage will update to show the changes that will be made to base and whether the branches can be automatically merged. Under most cases, there will not be any merge conflicts. Github will provide instructions on how to resolve conflicts if there are any. If additional help to merge conflicts is needed, perform a web search.
6. Given there are no conflicts, left click the green "Create pull request" button.
7. To create the pull request, a title for the request must be given. Something like "Update branch" is fine, but the exact title is not very important.
8. After a title is entered, left click the green "Create pull request" button.
9. You will now be taken to a page that shows a review of the commits that will be merged. Scroll down to below the list of commits to find the green "Merge pull request" button. Left click this button.
10. A title and comment section will appear in the place where the button was. If changes to the title and comment are desired, make them. Left click the green "Confirm merge" button to complete the request.
11. Now these changes can be merged into a local branch by navigating on the computer in the terminal to folder the local repository is in and using the command "git pull".
