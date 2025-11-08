# SQL_TESTING: Database Schema for Not Applicable's !Jeopardy App

![ERD](img/SQL_ERD_v3.png)


# Table Descriptions
---
## 1) Table Question

### Description
This strong entity contains all question, answers, and associated metadata sourced from [J-Archive](https://j-archive.com/). It has a one-to-many relationship with the weak entity GameQuestion wherein each QuestionID can be utilized on the game board of zero or more individual games.

### Attributes (incl. column & table constraints, where applicable)
- QuestionID INTEGER PRIMARY KEY
- Category VARCHAR(50) NOT NULL
- RoundName VARCHAR(2) NOT NULL
- PointValue INT NOT NULL
- QuestionText VARCHAR(500) NOT NULL
- QuestionAns VARCHAR(500) NOT NULL
- CONSTRAINT UniqueQ UNIQUE (QuestionText)

### List of Unit Tests for Constraint Validation
- test_Question_InsertRow

### Data Access Methods

---
## 2) Table Game

### Description
This strong entity contains one entry for each unique game instantiated by one or more player contestants. Its attributes capture game metadata like the date initiated and whether the game is in progress or completed. It has a one-to-many relationship with the weak entity GameQuestion that captures the set of QuestionIDs that populated the game boards of a specific GameID. Likewise, it has a one-to-many relationship with the weak entity Contestant that captures the PlayerIDs of all individual(s) that participated in a specific GameID.

### Attributes (incl. column & table constraints, where applicable)
- GameID INTEGER PRIMARY KEY
- DisplayName VARCHAR(50) NOT NULL DEFAULT ('Game ' || strftime('%Y-%m-%d %H:%M:%S', 'now'))
- StartDate DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
- EndDate DATETIME
- IsCompleteGame CHAR(1) DEFAULT 'N'
- IsCanceledGame CHAR(1) DEFAULT 'N'

### List of Unit Tests for Constraint Validation
- test_Game_CreateNewGame

### Data Access Methods

---
## 3) Table Player

### Description
This strong entity contains one entry for each unique player who registers to play games in the application. It has a one-to-many relationship with the weak entity Contestant that tracks each of the zero or more games a player has participated in. It also has a one-to-any relationship with the weak entity PlayerAnswer that tracks each of the answers a player has submitted for each instance of a question in a game.

### Attributes (incl. column & table constraints, where applicable)
- PlayerID INTEGER PRIMARY KEY
- UserName VARCHAR(50) NOT NULL
- TotalGamesPlayed INT NOT NULL DEFAULT 0
- TotalGamesWon INT NOT NULL DEFAULT 0
- TotalGamesRunnerUp INT NOT NULL DEFAULT 0
- HighScore INT NOT NULL DEFAULT 0
- CONSTRAINT UniqueName UNIQUE (Username)

### List of Unit Tests for Constraint Validation
- test_Player_newPlayerSignup

### Data Access Methods

---
## 4) Table GameQuestion

### Description
This weak entity maps Questions (QuestionID) to the games (GameID) they have appeared in through foreign key relationships and is the means by which the database logs the contents of individual game boards. It also contains a metadata field that records whether a question has been answered and removed from the board.

### Attributes (incl. column & table constraints, where applicable)
- GameID INT
- QuestionID INT
- IsAnswered CHAR(1) NOT NULL DEFAULT 'N'
- CONSTRAINT GameLogFK FOREIGN KEY (GameID) REFERENCES Game (GameID) ON DELETE CASCADEON UPDATE CASCADE
- CONSTRAINT QuestionBankFK FOREIGN KEY (QuestionID) REFERENCES Question (QuestionID) ON DELETE CASCADE ON UPDATE CASCADE

### List of Unit Tests for Constraint Validation

### Data Access Methods

---
## 5) Table PlayerAnswer

### Description
This weak entity maps answers submitted by specific players (PlayerID) to the specific gameboard (GameID) and Question (QuestionID) the individual was playing. It also contains metadata attributes to capture the text submitted and whether it was scored as correct by the backend answer evaluation function.

### Attributes (incl. column & table constraints, where applicable)
- PlayerID INT
- GameID INT
- QuestionID INT
- AnswerText VARCHAR(500) NOT NULL
- IsCorrect CHAR(1)
- CONSTRAINT AnsweringPlayerFK FOREIGN KEY (PlayerID) REFERENCES Player (PlayerID) ON DELETE CASCADE ON UPDATE CASCADE
- CONSTRAINT AnswerGameFK FOREIGN KEY (GameID) REFERENCES Game (GameID) ON DELETE CASCADE ON UPDATE CASCADE
- CONSTRAINT AnsweredQFK FOREIGN KEY (QuestionID) REFERENCES Question (QuestionID) ON DELETE CASCADE ON UPDATE CASCADE

### List of Unit Tests for Constraint Validation

### Data Access Methods

---
## 6) Table Contestant

### Description
This weak entity maps players (PlayerID) to the games (GameID) they have participated in. It contains an additional attribute for tracking the player's score in each game.

### Attributes (incl. column & table constraints, where applicable)
- GameID INT
- PlayerID INT
- PlayerScore INT NOT NULL DEFAULT 0
- CONSTRAINT GameContestFK FOREIGN KEY (GameID) REFERENCES Game (GameID) ON DELETE CASCADE ON UPDATE CASCADE
- CONSTRAINT PlayerConstestFK FOREIGN KEY (PlayerID) REFERENCES Player (PlayerID) ON DELETE CASCADE ON UPDATE CASCADE

### List of Unit Tests for Constraint Validation
- test_Game_CreateNewContestant
- test_Contestant_DropPlayersOrGames

### Data Access Methods
---
# Function Descriptions
---
## 1) extract_questions_answers_array

### Description
- This function is called from initialize_game and extracts question and answer array from the Table Question.  

### Parameters
- filePath to DB 
- DB File
- Table Name (Question)

### Return Values
- Question Array in 6 column x 5 row format
- Answer Array in 6 column x 5 row format

### Associated Tests
- Game_6692

## 2) update_highscore

### Description
- This function updates the Player Table upon the completion of a game. It creates an entry in the table if the playerid/username is not already present in the table and updates TotalGamesPlayed, TotalGamesWon, TotalGamesRunnerUp and HighScore.
  
### Parameters
- Player Name - STRING
- GameID - INT 
- Score from the Game - INT 
- win - BOOLEAN
- runner_up - BOOLEAN
  
### Return Values
- None
  
### Associated Tests
- add_trentknowsall

## 3) 
### Description
### Parameters
### Return Values
### Associated Tests

## 4) 
### Description
### Parameters
### Return Values
### Associated Tests

## 5) 
### Description
### Parameters
### Return Values
### Associated Tests

## 6) 
### Description
### Parameters
### Return Values
### Associated Tests
