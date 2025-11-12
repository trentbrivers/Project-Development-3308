# Execute `PRAGMA foreign_keys = ON` for all connections; https://sqlite.org/foreignkeys.html

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
    cur.execute('PRAGMA foreign_keys = ON;')

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
    cur.execute('PRAGMA foreign_keys = ON;')
    
    cur.executemany("INSERT INTO Question (GameCode, Round, Category, PointValue, QuestionText, QuestionAns) VALUES(?, ?, ?, ?, ?, ?)", input)
    con.commit()

    con.close()

def Game_CreateNewGame(dbFilePath):
    """Simulates the process of a signed-in user starting 
    a new game. Under the hood, a new row is created in 
    TABLE Game."""
    # New row inserted into Game
    con = sqlite3.connect(dbFilePath) 
    cur = con.cursor()
    cur.execute('PRAGMA foreign_keys = ON;')
    
    cur.execute('INSERT INTO Game DEFAULT VALUES;')
    con.commit()

    con.close()

def Contestant_CreateNewContestant(dbFilePath, username:str):
    """Continues the simulated the process of a signed-in user 
    starting a new game. Under the hood, the unique PlayerID/GameID 
    combo created Game_CreateNewGame is called becomes a new row in 
    TABLE Contestant."""

    con = sqlite3.connect(dbFilePath) 
    cur = con.cursor()
    cur.execute('PRAGMA foreign_keys = ON;')

    # Subquery to get the PlayerID
    UserID = cur.execute("SELECT PlayerID FROM Player WHERE UserName = ?;", (username,)).fetchone()[0]
    # Subquery to get the GameID
    # How do I know what Game I just created? 
    # Would bundling CreateNewGame and CreateNewContestant in a TRANSACTION guarantee this is right?
    GameID = cur.execute("SELECT MAX(GameID) FROM Game;").fetchone()[0]
    # Main Query: Create a new row in Contestant
    cur.execute("INSERT INTO Contestant (GameID, PlayerID) VALUES (?, ?);", (GameID, UserID))
    con.commit()

    con.close()

def GameQuestion_SetupGameboard(dbFilePath:Path, gameID:str):
    """Simulates the process of storing a game board in
    GameQuestion when the backend receives an entire game
    (e.g., game_6692) as an request rather than a set of categories."""
    
    con = sqlite3.connect(dbFilePath) 
    cur = con.cursor()
    cur.execute('PRAGMA foreign_keys = ON;')
    
    gameID = (gameID, )
    QuestionIDs = cur.execute('SELECT QuestionID FROM Question WHERE GameCode = (?)', gameID).fetchall()
    GameID = cur.execute("SELECT MAX(GameID) FROM Game;").fetchone()[0]

    insertRows = [(GameID, QuestionID[0]) for QuestionID in QuestionIDs]
    cur.executemany('INSERT INTO GameQuestion (GameID, QuestionID) VALUES (?, ?)', insertRows)
    con.commit()

    con.close()
    

    