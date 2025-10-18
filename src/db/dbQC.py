import os
import sqlite3

def print_tables(db_filename:str):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")

    print ("\nTables:")
    for t in c.fetchall() :
        print ("\t[%s]"%t[0])

     ##   print ("\tColumns of", t[0])
        c.execute("PRAGMA table_info(%s);"%t[0])
        for attr in c.fetchall() :
            print ("\t\t", attr)
        
        print ("")

print_tables('notJeopardyDB.db')