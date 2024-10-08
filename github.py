import os
import subprocess
from datetime import datetime, timedelta

# Configuration variables
REPO_PATH = r'C:\Users\alexm\Desktop\py'  # Path to the local Git repository
COMMIT_MESSAGE = 'Hack the contribution graph'  # Commit message to be used
START_DATE = '2024-04-01'  # Start date for generating commits
DAYS = 60  # Number of commits to make (one commit per day)
DAYS_TO_SKIP = 0  # Number of days to skip between commits (e.g., 1 means skipping a day)
TEMP_FILE_NAME = 'temp.txt'  # Temporary file to modify for each commit
BRANCH_NAME = 'main'  # The branch to push the changes to

def run_command(command, env=None):
    """
    Runs a shell command and returns its output.
    :param command: The shell command to run.
    :param env: Optional environment variables to pass.
    :return: The output of the command.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
    return result.stdout.strip()

def change_date_and_commit(date, counter):
    """
    Changes the GIT_AUTHOR_DATE and GIT_COMMITTER_DATE, modifies a file, and makes a commit.
    :param date: The date to set for the commit (affects Git contribution graph).
    :param counter: The commit number for tracking purposes in the commit message.
    """
    env = os.environ.copy()  # Copy current environment variables
    env['GIT_AUTHOR_DATE'] = date  # Set the author date for the commit
    env['GIT_COMMITTER_DATE'] = date  # Set the committer date for the commit
    
    # Modify the temp file to create a change
    with open(TEMP_FILE_NAME, 'a') as temp_file:
        temp_file.write(f'Commit {counter}\n')  # Add a new line for each commit
    
    # Stage the changes and commit with the provided date
    run_command('git add .')  # Add all changes to staging
    run_command(f'git commit -m "{COMMIT_MESSAGE} {counter}"', env=env)  # Make a commit with the date set in env

def main():
    """
    Main function that automates the process of creating multiple Git commits with different dates.
    """
    # Change to the Git repository directory
    os.chdir(REPO_PATH)
    
    # Parse the start date
    start_date = datetime.strptime(START_DATE, '%Y-%m-%d')
    commit_counter = 1  # Initialize commit counter
    
    # Iterate through the specified number of days, generating commits
    for i in range(DAYS):
        commit_date = start_date + timedelta(days=i * (DAYS_TO_SKIP + 1))  # Calculate commit date
        commit_date_str = commit_date.strftime('%Y-%m-%dT%H:%M:%S')  # Format date for Git
        print(f"Creating commit for {commit_date_str}")  # Print status
        change_date_and_commit(commit_date_str, commit_counter)  # Make the commit with the calculated date
        commit_counter += 1  # Increment the commit counter
    
    # Push all the changes to the remote repository
    push_output = run_command(f'git push origin {BRANCH_NAME}')
    print(push_output)  # Output the result of the push command

if __name__ == "__main__":
    main()  # Run the script
