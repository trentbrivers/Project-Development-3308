from pathlib import Path
import sqlite3

dbPath = Path(__file__).parent.resolve().joinpath('notJeopardyDB.db')
con = sqlite3.connect(dbPath)
cur = con.cursor()

# Cleanup actions - start w/ blank slate
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

# Create tables and constraints de novo
cur.executescript("""
    BEGIN;
    CREATE TABLE IF NOT EXISTS Game(GameID INTEGER PRIMARY KEY,
                                    DisplayName VARCHAR(50) NOT NULL,
                                    StartDate DATETIME NOT NULL,
                                    EndDate DATETIME NOT NULL,
                                    IsCompleteGame CHAR(1),
                                    IsCanceledGame CHAR(1)
                                    );
    
    CREATE TABLE IF NOT EXISTS Player(PlayerID INTEGER PRIMARY KEY,
                                      UserName VARCHAR(50) NOT NULL,
                                      TotalGamesPlayed INT NOT NULL,
                                      TotalGamesWon INT NOT NULL,
                                      TotalGamesRunnerUp INT NOT NULL,
                                      HighScore INT NOT NULL,
                                      CONSTRAINT UniqueName UNIQUE (Username)
                                      );
                  
    CREATE TABLE IF NOT EXISTS Question(QuestionID INTEGER PRIMARY KEY,
                                        Category VARCHAR(50) NOT NULL,
                                        PointValue INT NOT NULL,
                                        QuestionText VARCHAR(500) NOT NULL,
                                        QuestionAns VARCHAR(500) NOT NULL,
                                        CONSTRAINT UniqueQ UNIQUE (QuestionText)
                                        );
                  
    CREATE TABLE IF NOT EXISTS Contestant(GameID INT,
                                          PlayerID INT,
                                          PlayerScore INT NOT NULL,
                                          CONSTRAINT GameContestFK FOREIGN KEY (GameID) REFERENCES Game (GameID)
                                              ON DELETE CASCADE
                                              ON UPDATE CASCADE,
                                          CONSTRAINT PlayerConstestFK FOREIGN KEY (PlayerID) REFERENCES Player (PlayerID)
                                              ON DELETE CASCADE
                                              ON UPDATE CASCADE
                                          );
    
    CREATE TABLE IF NOT EXISTS GameQuestion(GameID INT,
                                            QuestionID INT,
                                            IsAnswered CHAR(1) NOT NULL,
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
                                           IsCorrect CHAR(1) NOT NULL,
                                           CONSTRAINT AnsweringPlayerFK FOREIGN KEY (PlayerID) REFERENCES Player (PlayerID)
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE,
                                           CONSTRAINT AnswerGameFK FOREIGN KEY (GameID) REFERENCES GameQuestion (GameID)
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE,
                                            CONSTRAINT AnsweredQFK FOREIGN KEY (QuestionID) REFERENCES GameQuestion (QuestionID)
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE
                                            );
    COMMIT;
    """)

con.commit()
con.close()