import sqlite3 as sql
from pathlib import Path
from enum import Enum


class ScoreUpdate(Enum):
    INCREMENT = 0
    DECREMENT = 1


def add_players(db_file: Path, usernames: list[str]):
    print(db_file)
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


def update_player_score(db_file: Path, update_type: ScoreUpdate, username: str, score):
    with sql.connect(db_file) as conn:
        cursor = conn.cursor()

        if update_type == ScoreUpdate.INCREMENT:
            cursor.execute(
            '''
                UPDATE Player
                SET HighScore = HighScore + ?
                WHERE UserName = ?
                ''', (score, username))
        else:
            cursor.execute(
            '''
                UPDATE Player
                SET HighScore = HighScore - ?
                WHERE UserName = ?
                ''', (score, username))

        high_score = cursor.execute("SELECT HighScore FROM Player WHERE UserName = ?", (username,)).fetchone()[0]

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