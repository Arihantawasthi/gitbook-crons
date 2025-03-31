import os
import sys

from cfg import GIT_DIR

from db_handler import Storage
from git_stats import gather_stats
from repo_handler import get_repo_metadata

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <task>")
        print("Available tasks: update_stats, insert_metadata")
        sys.exit(1)

    task = sys.argv[1]

    if task == "update_stats":
        data = gather_stats()
        Storage().insert_data_into_db(data)

    elif task == "insert_metadata":
        for repo in os.listdir(GIT_DIR):
            repo_path = os.path.join(GIT_DIR, repo)
            if os.path.isdir(repo_path):
                metadata = get_repo_metadata(repo_path)
                Storage().insert_repo_metadata(metadata)

    else:
        print(f"Error: unknown task {task}")
        sys.exit(1)


if __name__ == "__main__":
    main()
