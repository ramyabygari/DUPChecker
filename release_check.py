from github import Github, GithubException
import os
import difflib
import re

# Function to compare two files and print the differences
def compare_files(file1_content, file2_content):
    differ = difflib.Differ()
    diff = list(differ.compare(file1_content, file2_content))
    
    # Print the differences
    for line in diff:
        print(line)

# Function to download a file from a release or commit
def download_file(repo, file_path, release):
    return repo.get_contents(file_path, ref=release.tag_name).decoded_content.decode("utf-8")




# Initialize the GitHub API client
g = Github(os.getEnv("ACCESS_TOKEN"))

# Repository information
repository_name = "hbase"

# Specify the repository
repo = g.get_repo(f"apache/{repository_name}")

# Get the list of releases
releases = list(repo.get_releases())

# Output directory
output_dir = "/Users/ramyabygari/cs527/hbase_repo"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)



def is_function_definition(line):
    return line.strip().endswith("{") and "(" in line and ")" in line

def compare_files(file1_content, file2_content, file_path):
    # Regular expression to match Java function signatures
    function_signature_pattern = r'\s*(public|private|protected)?\s*(\w+(\[\])*)\s+(\w+)\s*\(([^)]*)\)'

    # Iterate through lines in the files
    original_lines = []
    changed_lines = []
    differ = difflib.Differ()
    diff = list(differ.compare(file1_content, file2_content))
    fl

    if original_lines:
        print(f"File: {file_path}")
        for original_line, changed_line in zip(original_lines, changed_lines):
            print(f"Original: {original_line}")
            print(f"Changed:  {changed_line}")
            match = re.search(function_signature_pattern, line[1:])
            if match:
                print(f"File: {file_path}")
                print(f"  {line[1:]}") 
    for line in difflib.unified_diff(file1_content, file2_content):
        if line.startswith(' '):
            continue  # Skip unchanged lines
        if line.startswith('-'):
            original_line = line[2:]
            # Check if the line is a function signature
            match = re.search(function_signature_pattern, line[1:])
            if match:
                print(f"File: {file_path}")
                print(f"  {line[1:]}") 
        # if line.starts

# Iterate through releases
for i in range(len(releases) - 1):
    from_release = releases[i]
    to_release = releases[i + 1]

    # Compare the two releases
    comparison = repo.compare(from_release.tag_name, to_release.tag_name)
    
    # Get the list of files that have changed between the two releases
    changed_files = comparison.files

    # Output the list of changed files
    for file in changed_files:
        file_path = file.filename

        # Access the file content directly from GitHub without downloading
        if file_path.endswith(".java"):
            try:
                file1_content = download_file(repo, file_path, from_release)
                file2_content = download_file(repo, file_path, to_release)

                # Perform the diff
                # differ = difflib.Differ()
                # diff = list(differ.compare(file1_content.splitlines(), file2_content.splitlines()))

                compare_files(file1_content.splitlines(), file2_content.splitlines(), file_path)
                
                # Print the differences
                # for line in diff:
                #     function_signatures = re.finditer(function_signature_pattern, line)
                #     for match in function_signatures:
                #         access_modifier = match.group(1) or "default"
                #         return_type = match.group(2) or "void"
                #         method_name = match.group(3)
                #         parameter_list = match.group(4)
                #         print(file_path)
                #         print(line)
                #         print(f"Access Modifier: {access_modifier}")
                #         print(f"Return Type: {return_type}")
                #         print(f"Method Name: {method_name}")
                #         print(f"Parameter List: {parameter_list}")
                    # if is_function_definition(line) and re.finditer(function_signature_pattern, line):
                    #     print(f"  {line}")
    
            except GithubException as e:
                if e.status == 404:
                    print(f"File not found: {file_path}")
                else:
                    print(f"Error processing file: {e}")
