import psycopg2
from datetime import datetime
from cfg import DATABASE_CONFIG

class Storage:
    def __init__(self):
        self.dbname = DATABASE_CONFIG.get("dbname")
        self.user=DATABASE_CONFIG["user"]
        self.password=DATABASE_CONFIG["password"]
        self.host=DATABASE_CONFIG["host"]
        self.port=DATABASE_CONFIG["port"]

    def connect(self):
       return psycopg2.connect(
            dbname = self.dbname,
            user = self.user,
            password = self.password,
            host = self.host,
            port = self.port
        )

    def insert_data_into_db(self, data):
        try:
            connection = self.connect()
            with connection.cursor() as cursor:
                insert_query = """
                    INSERT INTO stats (num_of_lines, num_of_commits, num_of_files, date, num_of_repos)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (date) DO UPDATE
                      SET num_of_repos = EXCLUDED.num_of_repos,
                          num_of_commits = EXCLUDED.num_of_commits,
                          num_of_files = EXCLUDED.num_of_files,
                          num_of_lines = EXCLUDED.num_of_lines;
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

    def insert_repo_metadata(self, data):
        try:
            connection = self.connect()
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

    def get_public_repo_count(self):
        connection = self.connect()
        with connection.cursor() as cursor:
            query = """
                SELECT * FROM repos WHERE visibility='public';
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
