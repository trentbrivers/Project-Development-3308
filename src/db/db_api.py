import sqlite3 as sql
from pathlib import Path
from datetime import datetime


def add_players(db_file: Path, usernames: list[str]):
    with sql.connect(db_file) as conn:
        cursor = conn.cursor()

        for username in usernames:
            cursor.execute(
            '''
                INSERT INTO Player (UserName, TotalGamesPlayed, TotalGamesWon, TotalGamesRunnerUp, HighScore)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, 0, 0, 0, 0))

        cursor.close()
        conn.commit()


def update_player_score(db_file: Path, username: str, score):
    with sql.connect(db_file) as conn:
        cursor = conn.cursor()

        cursor.execute(
        '''
            UPDATE Player
            SET HighScore = HighScore + ?
            WHERE UserName = ?
        ''', (score, username))

        high_score = cursor.execute("SELECT HighScore FROM Player WHERE UserName = ?", (username,)).fetchone()

        cursor.close()
        conn.commit()

    return high_score


def extract_questions_data(db_file: Path):
    """ Function to extract questions and answers from the database """

    # Positions in row:
    # 0 - Question
    # 1 - Category
    # 2 - J/DJ/FJ
    # 3 - Point Value
    # 4 - Question
    # 5 - Answer

    categories, questions, answers, point_values = [], [], [], []

    with sql.connect(db_file) as conn:
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM Question")

        for question_idx, category, _round, points, question, answer in res.fetchall():
            questions.append(question)
            answers.append(answer)
            point_values.append(points)

            if 1 <= question_idx <= 6 or 31 <= question_idx <= 36 or question_idx == 61:
                categories.append(category)

        cursor.close()

    return categories, questions, answers, point_values



#API for creating the game record upon the completion of a game - internal tracking purposes
#Need to ensure that the game_id is passed into the backend code at some point if this is used as a tracking entry
def create_game_record(db_file: Path, username: str, game_id):
    """ Function to generate a new game entry into the Game Table. Internal Tracking of games user has played """
    current_date_time = datetime.now()
    current_date_time = current_date_time.strftime('%Y-%m-%d %H:%M:%S')
    with sql.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Game (GameID,DisplayName, StartDate, EndDate, IsCompleteGame, IsCanceledGame)
            VALUES (?,?,?,?,?,?) """,(game_id, username, current_date_time, current_date_time, 'N', 'N'))

        cursor.close()
        conn.commit()


#API for completing the game record upon the completion of a game - internal tracking purposes
#Need to ensure that the game_id is passed into the backend code at some point if this is used as a tracking entry
def complete_game_record(db_file: Path, username: str, game_id):
    """ Function to complete the new game entry in the Game Table. Internal Tracking of games user has played """
    current_date_time = datetime.now()
    current_date_time = current_date_time.strftime('%Y-%m-%d %H:%M:%S')
    with sql.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Game
            SET IsCompleteGame = 'Y', EndDate = ?
            WHERE GameID = ? AND UserName = ? """, (current_date_time, game_id, username)
        )

        cursor.close()
        conn.commit()


