import sqlite3 as sql
from pathlib import Path

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

        for _question_idx, category, _round, points, question, answer in res.fetchall():
            categories.append(category)
            questions.append(question)
            answers.append(answer)
            point_values.append(points)

        cursor.close()

    return categories, questions, answers, point_values