import sqlite3
from sqlite3 import Error

def create_db(db_file):
    # if we error, we rollback automatically, else commit!

    with sqlite3.connect('/Temp/testDB.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT SQLITE_VERSION()')
        data = cursor.fetchone()
        print('SQLite version:', data)
    return


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"notification.db"

    sql_create_job_table = """ CREATE TABLE IF NOT EXISTS jobdetails (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        name text NOT NULL UNIQUE,
                                        creator text NOT NULL,
                                        isrepeat integer DEFAULT 1,
                                        create_date text NOT NULL,
                                        start_date text  NOT NULL,
                                        cron_string text,
                                        message text NOT NULL
                                    ); """

    sql_create_subscriber_table = """CREATE TABLE IF NOT EXISTS subscriberdetails (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    name text NOT NULL UNIQUE,
                                    phone text NOT NULL,
                                    email text NOT NULL, 
                                    messengerid text NOT NULL,
                                );"""

    sql_create_subscription_table = """CREATE TABLE IF NOT EXISTS subscriptiondetails (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    job_name text NOT NULL UNIQUE,
                                    job_id integer NOT NULL,
                                    subscriber_name text NOT NULL UNIQUE,
                                    subscriber_id integer NOT NULL,
                                    transport integer DEFAULT 1,
                                    FOREIGN KEY (job_id) REFERENCES jobdetails (id),
                                    FOREIGN KEY (subscriber_id) REFERENCES subscriberdetails (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create job table
        create_table(conn, sql_create_job_table)

        # create subscriber table
        create_table(conn, sql_create_subscriber_table)

        # create subscription table
        create_table(conn, sql_create_subscription_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
