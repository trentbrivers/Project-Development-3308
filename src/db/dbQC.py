from pathlib import Path
import sqlite3

filePath = Path(__file__).parent.resolve()

def print_tables(dbPath:Path, dbFilename:str):
    
    dbPath = dbPath.joinpath(dbFilename) 
    con = sqlite3.connect(dbPath)
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

def print_rows(dbPath:Path, dbFilename:str, tblnames:list):
    """Helper function to check that test data inserted into
    the database displays correctly."""
    
    dbPath = dbPath.joinpath(dbFilename) 
    con = sqlite3.connect(dbPath) 
    cur = con.cursor()

    for tbl in tblnames:
        print(f'\n{tbl}:')
        res = cur.execute(f"SELECT * FROM {tbl};")
        print(res.fetchall())

    con.close()

def testQuestion(dbPath:Path, dbFilename:str):
    """Prototype tests for table Question"""
    
    dbPath = dbPath.joinpath(dbFilename) 
    con = sqlite3.connect(dbPath) 
    cur = con.cursor()

    # Positive Control: This should work & show rowid aliasing in action
    PosCtrl = [('Testing', 100, 'Why are we doing this?', 'To test basic RI actions.'),
               ('Birds', 500, 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")]
    
    cur.executemany("INSERT INTO Question (Category, PointValue, QuestionText, QuestionAns) VALUES(?, ?, ?, ?)", PosCtrl)
    con.commit()
    con.close()

def cleanupHelper(dbPath:Path, dbFilename:str, tbls:list=[]):
    """Truncates the tables passed in parameter list.
    If the default empty list is passed, all tables are
    truncated."""

    dbPath = dbPath.joinpath(dbFilename) 
    con = sqlite3.connect(dbPath) 
    cur = con.cursor()

    if tbls == []:
        cur.executescript("""
                          BEGIN;
                          DELETE FROM Contestant;
                          DELETE FROM PlayerAnswer;
                          DELETE FROM GameQuestion;
                          DELETE FROM Player;
                          DELETE FROM Question;
                          DELETE FROM Game;
                          COMMIT;
                          """)
    
    else:
        for tbl in tbls:
            cur.execute(f"DELETE FROM {tbl};")

# QC after DDL
print_tables(filePath, 'notJeopardyDB.db')

# DML and constraints QC here
testQuestion(filePath, 'notJeopardyDB.db')
print_rows(filePath, 'notJeopardyDB.db', ['Question'])
# cleanupHelper(filePath, 'notJeopardyDB.db')
# print_rows(filePath, 'notJeopardyDB.db', ['Question'])
