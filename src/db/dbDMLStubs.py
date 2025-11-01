from pathlib import Path
import sqlite3
import sys

# Pass python dbDDL.py notJeopardyDB.db to Terminal
dbPath = Path(__file__).parent.resolve().joinpath(sys.argv[1])

# Name functions for game actions
def Player_newUserSignup(dbFilePath, input):
    """Simulates the process of receiving a request to register 
    a new user to TABLE Player. Intended to check that the 
    CONSTRAINT UniqueName and the DEFAULT values work as 
    designed."""
    
    con = sqlite3.connect(dbFilePath)
    cur = con.cursor()

    # Get input into sqlite3 expected format
    values = (input,)
    cur.execute("INSERT INTO Player (UserName) VALUES (?)", values)
    # print(cur.execute("SELECT * FROM Player;").fetchall())
    con.commit()
    
    con.close()

def Question_InsertRow(dbFilePath, input):
    """Simulates the process of entering multiple rows of question data 
    into TABLE Question. Intended to check that the CONSTRAINT 
    UniqueQ successfully prohibits duplicate questions."""

    con = sqlite3.connect(dbFilePath) 
    cur = con.cursor()
    
    cur.executemany("INSERT INTO Question (Round, Category, PointValue, QuestionText, QuestionAns) VALUES(?, ?, ?, ?, ?)", input)
    con.commit()

    con.close()
    