import os
import sqlite3

filepath = './src/db'

def print_tables(db_filename:str):
    global filepath
    file = os.path.join(filepath, db_filename) 
    
    con = sqlite3.connect(db_filename)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

    print ("\nTables:")
    for t in cur.fetchall() :
        print ("\t[%s]"%t[0])

     ##   print ("\tColumns of", t[0])
        cur.execute("PRAGMA table_info(%s);"%t[0])
        for attr in cur.fetchall() :
            print ("\t\t", attr)
        
        print ("")

def print_rows(db_filename:str, tblnames:list):
    """Helper function to check that test data inserted into
    the database displays correctly."""
    global filepath
    file = os.path.join(filepath, db_filename) 
    
    con = sqlite3.connect(file)
    cur = con.cursor()

    for tbl in tblnames:
        print(f'\n{tbl}:')
        res = cur.execute(f"SELECT * FROM {tbl};")
        print(res.fetchall())

    con.close()

def testQuestion(db_filename:str):
    """Prototype tests for table Question"""
    global filepath
    file = os.path.join(filepath, db_filename) 
    
    con = sqlite3.connect(file)
    cur = con.cursor()

    # Positive Control: This should work & show rowid aliasing in action
    PosCtrl = [('Testing', 100, 'Why are we doing this?', 'To test basic RI actions.'),
               ('Birds', 500, 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")]
    
    cur.executemany("INSERT INTO Question (Category, PointValue, QuestionText, QuestionAns) VALUES(?, ?, ?, ?)", PosCtrl)

print_tables('notJeopardyDB.db')
testQuestion('notJeopardyDB.db')
print_rows('notJeopardyDB.db', ['Question'])
