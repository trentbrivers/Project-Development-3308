from pathlib import Path
import sqlite3
import sys

# Pass python dbDDL.py notJeopardyDB.db to Terminal
dbPath = Path(__file__).parent.resolve().joinpath(sys.argv[1])

# Cleanup actions - start w/ blank slate
def preClean(filePath: Path):
    """Ensures that all extant tables are 
    removed from the database prior to DDL."""
    con = sqlite3.connect(filePath)
    cur = con.cursor()

    cur.executescript("""
        BEGIN;
        DROP TABLE IF EXISTS Contestant;
        DROP TABLE IF EXISTS PlayerAnswer;
        DROP TABLE IF EXISTS GameQuestion;
        DROP TABLE IF EXISTS Player;
        DROP TABLE IF EXISTS Question;
        DROP TABLE IF EXISTS Game;
        COMMIT;
        """)
    
    con.commit()
    con.close()

# Create tables and constraints de novo
def dbDDL(filePath: Path):
    """Performs data definition language (DDL) to
    specify all tables, including column and table
    constraints."""
    
    con = sqlite3.connect(filePath)
    cur = con.cursor()

    # Put CHECK NOT NULL CONSTRAINT on EndDate of completed game in Game?
    # Put CHECK IsX = 'Y' or 'N
    cur.executescript("""
        BEGIN;
        CREATE TABLE IF NOT EXISTS Game(GameID INTEGER PRIMARY KEY,
                                        DisplayName VARCHAR(50) NOT NULL DEFAULT ('Game ' || strftime('%Y-%m-%d %H:%M:%S', 'now')),
                                        StartDate DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                                        EndDate DATETIME,
                                        IsCompleteGame CHAR(1) DEFAULT 'N',
                                        IsCanceledGame CHAR(1) DEFAULT 'N'
                                        );
    
        CREATE TABLE IF NOT EXISTS Player(PlayerID INTEGER PRIMARY KEY,
                                          UserName VARCHAR(50) NOT NULL,
                                          TotalGamesPlayed INT NOT NULL DEFAULT 0,
                                          TotalGamesWon INT NOT NULL DEFAULT 0,
                                          TotalGamesRunnerUp INT NOT NULL DEFAULT 0,
                                          HighScore INT NOT NULL DEFAULT 0,
                                          CONSTRAINT UniqueName UNIQUE (Username)
                                          );
                  
        CREATE TABLE IF NOT EXISTS Question(QuestionID INTEGER PRIMARY KEY,
                                            GameCode VARCHAR(9) NOT NULL,
                                            Category VARCHAR(50) NOT NULL,
                                            Round VARCHAR(2) NOT NULL,
                                            PointValue INT NOT NULL,
                                            QuestionText VARCHAR(500) NOT NULL,
                                            QuestionAns VARCHAR(500) NOT NULL,
                                            CONSTRAINT UniqueQ UNIQUE (QuestionText)
                                            );
                  
        CREATE TABLE IF NOT EXISTS Contestant(GameID INT,
                                              PlayerID INT,
                                              PlayerScore INT NOT NULL DEFAULT 0,
                                              CONSTRAINT GameContestFK FOREIGN KEY (GameID) REFERENCES Game (GameID)
                                                  ON DELETE CASCADE
                                                  ON UPDATE CASCADE,
                                              CONSTRAINT PlayerConstestFK FOREIGN KEY (PlayerID) REFERENCES Player (PlayerID)
                                                  ON DELETE CASCADE
                                                  ON UPDATE CASCADE
                                              );
    
        CREATE TABLE IF NOT EXISTS GameQuestion(GameID INT,
                                                QuestionID INT,
                                                IsAnswered CHAR(1) NOT NULL DEFAULT 'N',
                                                CONSTRAINT GameLogFK FOREIGN KEY (GameID) REFERENCES Game (GameID)
                                                    ON DELETE CASCADE
                                                    ON UPDATE CASCADE,
                                                CONSTRAINT QuestionBankFK FOREIGN KEY (QuestionID) REFERENCES Question (QuestionID)
                                                    ON DELETE CASCADE
                                                    ON UPDATE CASCADE
                                                );
    
        CREATE TABLE IF NOT EXISTS PlayerAnswer(PlayerID INT,
                                                GameID INT,
                                                QuestionID INT,
                                                AnswerText VARCHAR(500) NOT NULL,
                                                IsCorrect CHAR(1),
                                                CONSTRAINT AnsweringPlayerFK FOREIGN KEY (PlayerID) REFERENCES Player (PlayerID)
                                                    ON DELETE CASCADE
                                                    ON UPDATE CASCADE,
                                                CONSTRAINT AnswerGameFK FOREIGN KEY (GameID) REFERENCES Game (GameID)
                                                    ON DELETE CASCADE
                                                    ON UPDATE CASCADE,
                                                CONSTRAINT AnsweredQFK FOREIGN KEY (QuestionID) REFERENCES Question (QuestionID)
                                                    ON DELETE CASCADE
                                                    ON UPDATE CASCADE
                                                );
        COMMIT;
        """)
    con.commit()
    con.close()

if __name__ == '__main__':
    preClean(dbPath)
    dbDDL(dbPath)