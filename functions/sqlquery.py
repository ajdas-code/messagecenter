import os
import sqlite3

Jobheaders = ['id','name', 'creator', 'isrepeat', 'create_date', 'start_date', 'cron_string', 'message']
Subscriberheaders = ['id','name', 'phone', 'email', 'messengerid']
Subscriptionheaders = ['id','job_name', 'job_id', 'subscriber_id', 'subscriber_name', 'transport']

# Create a database
conn = sqlite3.connect('example.db',check_same_thread=False)
conn.row_factory = sqlite3.Row


# Setup Schema
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)
        raise RuntimeError("Failed to create schema ....{}".format(create_table_sql))


def setup_schema():
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
                                    messengerid text NOT NULL
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
        raise RuntimeError("Failed to open sqlite3 DB connection!!!!")


# Make a convenience function for running SQL queries
# CRUD operations on our database

def sql_query(query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def sql_edit_insert(query, var):
    cur = conn.cursor()
    cur.execute(query, var)
    conn.commit()


def sql_delete(query, var):
    cur = conn.cursor()
    cur.execute(query, var)


def sql_query2(query, var):
    cur = conn.cursor()
    cur.execute(query, var)
    rows = cur.fetchall()
    return rows
