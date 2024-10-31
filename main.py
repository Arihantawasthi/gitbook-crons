from git_stats import gather_stats
from db_handler import insert_data_into_db

if __name__ == "__main__":
    data = gather_stats()
    print(data)
    insert_data_into_db(data)
