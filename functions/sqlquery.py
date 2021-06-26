import os
import sqlite3

Jobheaders = ['name', 'creator', 'isrepeat', 'create_date', 'start_date', 'cron_string', 'message']
Subscriberheaders = ['name', 'phone', 'email', 'messengerid']
Subscriptionheaders = ['job_name','job_id', 'subscriber_id', 'subscriber_name', 'transport']


# Create a database
conn = sqlite3.connect('example.db')
conn.row_factory = sqlite3.Row


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
