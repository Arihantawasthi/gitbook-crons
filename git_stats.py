import subprocess
from cfg import GIT_DIR
from db_handler import Storage


def num_of_commits(repo_path):
    try:
        result = subprocess.run(
            ["git", "--git-dir", repo_path, "rev-list", "--all", "--count"],
            capture_output=True,
            text=True,
            check=True
        )
        total_commits = int(result.stdout.strip())
        return total_commits
    except subprocess.CalledProcessError as err:
        print(f"Error counting commits in {repo_path}: {err}")
        return 0

def num_of_lines(file_names, repo_path):
    total_lines = 0
    try:
        for name in file_names:
            file_content = subprocess.run(
                ["git", "--git-dir", repo_path, "cat-file", "-p", f"HEAD:{name}"],
                capture_output=True,
                text=True,
                errors="ignore", # ignore decoding errors
                check=True
            )
            total_lines += len(file_content.stdout.splitlines())
    except subprocess.CalledProcessError as err:
        print(f"Error reading file in {repo_path}: {err}")

    return total_lines

def gather_stats():
    data = {
        "num_of_files": 0,
        "num_of_lines": 0,
        "num_of_commits": 0,
        "num_of_repos": 0
    }

    try:
        repos = Storage().get_public_repo_count()
        data["num_of_repos"] = len(repos)
        try:
            for repo in repos:
                repo_name = repo[1]+".git"
                repo_path = GIT_DIR+repo_name
                result = subprocess.run(
                    ["git", "--git-dir", repo_path, "ls-tree", "-r", "HEAD", "--name-only"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                files = result.stdout.splitlines()

                data["num_of_files"] += len(files)
                data["num_of_lines"] += num_of_lines(files, repo_path)
                data["num_of_commits"] += num_of_commits(repo_path)
        except subprocess.CalledProcessError as err:
            print(f"Error processing repo: {err}")

    except Exception as err:
        print(f"Failed to get repositories: {err}")

    return data
