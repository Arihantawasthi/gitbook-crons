import os
import subprocess
from datetime import datetime, UTC
import csv

def get_repo_metadata(repo_path):
    try:
        repo_name = os.path.basename(repo_path)

        last_commit_at = subprocess.check_output(["git", "--git-dir", repo_path, "log", "-1", "--format=%ct"]).decode().strip()
        last_commit_at = datetime.fromtimestamp(int(last_commit_at), UTC) if last_commit_at else None

        default_branch = subprocess.check_output(["git", "--git-dir", repo_path, "symbolic-ref", "--short", "HEAD"]).decode().strip()

        created_at = subprocess.check_output(["git", "--git-dir", repo_path, "log", "--reverse", "--format=%ct", "--max-count=1"]).decode().strip()
        created_at = datetime.fromtimestamp(int(created_at), UTC) if created_at else None

        desc_file = os.path.join(repo_path, "description")
        repo_desc = open(desc_file).read().strip() if os.path.exists(desc_file) else ""

        author = subprocess.check_output(["git", "--git-dir", repo_path, "log", "--reverse", "--format=%an", "--max-count=1"]).decode().strip()

        visibility_map = {}
        with open("../repos_visibility_data.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                name, visibility = row
                visibility_map[name] = visibility

        return {
            "repo_name": repo_name,
            "desc": repo_desc,
            "visibility": visibility_map[repo_name],
            "is_pinned": False,
            "default_branch": default_branch,
            "author": author,
            "created_at": created_at,
            "last_commit_at": last_commit_at
        }

    except Exception as err:
        print(err)

