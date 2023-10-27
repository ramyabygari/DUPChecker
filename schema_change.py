from github import Github, GithubException
import os
import difflib
import re

# Function to compare two files and print the differences
def compare_files(file1_content, file2_content):
    differ = difflib.Differ()
    diff = list(differ.compare(file1_content, file2_content))
    return diff

# Function to download a file from a release or commit
def download_file(repo, file_path, release):
    return repo.get_contents(file_path, ref=release.tag_name).decoded_content.decode("utf-8")

# Initialize the GitHub API client
g = Github(os.environ["ACCESS_TOKEN"])

# Repository information
repository_name = "cassandra"

# Specify the repository
repo = g.get_repo(f"apache/{repository_name}")

# Get the list of releases
releases = list(repo.get_releases())

# Output directory
output_dir = "/Users/ramya/CS527/DUPChecker/commits"  # Replace with the desired directory

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Regular expression to match Java function signatures
function_signature_pattern = r'\s*(public|private|protected)?\s*(\w+(\[\])*)\s+(\w+)\s*\(([^)]*)\)'
schema_change_patterns = [
    r'(CREATE|ALTER|DROP) (TABLE|KEYSPACE)',
    # Add more patterns as needed to cover different types of schema changes
]

# Function to check if a code change contains schema-related patterns
def has_schema_changes(change_text):
    for pattern in schema_change_patterns:
        if re.search(pattern, change_text, re.IGNORECASE):
            return True
    return False

# Function to remove single-line and multi-line comments from Java code
def remove_comments(java_code):
    # Remove single-line comments (//)
    java_code = re.sub(r'//.*', '', java_code)
    
    # Remove multi-line comments (/* ... */)
    java_code = re.sub(r'/\*.*?\*/', '', java_code, flags=re.DOTALL)
    
    return java_code

# Output file path
output_file_path = os.path.join(output_dir, "output.txt")

# Open the output file for writing
with open(output_file_path, "w") as output_file:
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

                    # Remove comments from Java code
                    file1_content = remove_comments(file1_content)
                    file2_content = remove_comments(file2_content)

                    # Perform the diff and check for schema changes in function signatures
                    differ = difflib.Differ()
                    diff = compare_files(file1_content.splitlines(), file2_content.splitlines())

                    # Track whether @Override and the specified method are found
                    override_found = False
                    method_found = False

                    for line in diff:
                        # Check if the line has schema-related patterns
                        if has_schema_changes(line):
                            output_text = f"Schema change detected in file: {file_path}\n"
                            output_text += f"Difference: {line}\n"
                            print(output_text)
                            # Write to the output file
                            output_file.write(output_text)

                        # Check for @Override and the specified method
                        if line.startswith("  @Override"):
                            override_found = True
                        elif method_found and line.strip().startswith("return element.referencesUserType(name);"):
                            # Found the specified method
                            output_text = f"Method found in file: {file_path}\n"
                            output_text += line
                            print(output_text)
                            output_file.write(output_text)
                            break  # No need to search further

                        # Check for the start of the specified method
                        if line.strip().startswith("public boolean referencesUserType(String name)"):
                            method_found = True

                    if override_found and method_found:
                        # Exit the loop as we have found what we were looking for
                        break

                except GithubException as e:
                    if e.status == 404:
                        print(f"File not found: {file_path}")
                    else:
                        print(f"Error processing file: {e}")

# Print a message to indicate where the output is saved
print(f"Output saved to: {output_file_path}")
