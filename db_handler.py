import psycopg2
from datetime import datetime
from cfg import DATABASE_CONFIG

def insert_data_into_db(data):
    try:
        connection = psycopg2.connect(
            dbname=DATABASE_CONFIG["dbname"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"],
            port=DATABASE_CONFIG["port"]
        )
        with connection.cursor() as cursor:
            insert_query = """
                INSERT INTO stats (num_of_lines, num_of_commits, num_of_files, date, num_of_repos)
                VALUES (%s, %s, %s, %s, %s)
            """
            current_date = datetime.now().date()
            cursor.execute(insert_query, (
                data["num_of_lines"],
                data["num_of_commits"],
                data["num_of_files"],
                current_date,
                data["num_of_repos"],
            ))
            print("Data inserted successfully into the stats table: ", data)
        connection.commit()
        connection.close()

    except (Exception, psycopg2.DatabaseError) as err:
        print(f"Error while inserting data into PostgreSQL: {err}")


def insert_repo_metadata(data):
    try:
        connection = psycopg2.connect(
            dbname=DATABASE_CONFIG["dbname"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"],
            port=DATABASE_CONFIG["port"]
        )
        with connection.cursor() as cursor:
            insert_query = """
                INSERT INTO repos (name, description, visibility, is_pinned, default_branch, author, created_at, last_commit_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                data["repo_name"],
                data["desc"],
                data["visibility"],
                data["is_pinned"],
                data["default_branch"],
                data["author"],
                data["created_at"],
                data["last_commit_at"]
            ))

            print("Data inserted successfully into the repos table: ", data)
        connection.commit()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as err:
        print(f"Error while inserting data into PostgreSQL: {err}")
