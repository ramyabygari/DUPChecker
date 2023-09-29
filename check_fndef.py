import os
from git import Repo

# Repository information
repo_url = "https://github.com/apache/hbase.git"  # Repository URL
branch_name = "master"  # Branch to analyze

# Clone the repository locally
repo_path = "hbase_repo"
if not os.path.exists(repo_path):
    Repo.clone_from(repo_url, repo_path)

# Function to check if a line contains a Java function definition
def is_function_definition(line):
    # You may need to adjust this logic to match your specific codebase's function definition style
    return line.strip().endswith("{") and "(" in line and ")" in line

# Iterate through commits
repo = Repo(repo_path)
commits = list(repo.iter_commits(branch_name))
for i in range(len(commits) - 1):
    new_commit = commits[i + 1]
    print(new_commit.message)
    # Check if the commit message contains "bump" (case-insensitive)

    if "bump" not in new_commit.message.lower():
        old_commit = commits[i]
        
        # Get the diff between two commits
        diff = repo.git.diff(old_commit, new_commit)

        # Split the diff into lines
        diff_lines = diff.splitlines()

        # Check if any lines in the diff represent function definition changes
        function_definition_changes = [line for line in diff_lines if is_function_definition(line)]

        if function_definition_changes:
            print(f"Commit: {new_commit.hexsha}")
            print("Function Definition Changes:")
            for line in function_definition_changes:
                print(f"  {line}")

            print("\n---\n")