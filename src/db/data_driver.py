from pathlib import Path
import re
import sqlite3
from src.db.dbExtractGame import extract_game


filePath = Path(__file__).parent.resolve()

def print_rows(dbPath: Path, dbFilename: str, tblnames: list):
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

def extract_questions_answers_array(dbPath: Path, dbFilename: str, tblnames: list):
    """ Function to extract questions and answers from the database """
    dbPath = dbPath.joinpath(dbFilename)
    questions, answers, point_values = [], [], []
    con = sqlite3.connect(dbPath)
    cur = con.cursor()

    #Positios in row:
    # 0 - Question Number
    # 1 - Category
    # 2 - J/DJ/FJ
    # 3 - Point Value
    # 4 - Question
    # 5 - Answer

    for tbl in tblnames:
        print(f'\n{tbl}:')
        res = cur.execute(f"SELECT * FROM {tbl};")
        for _question_idx, _category, _round, point_value, question, answer in res.fetchall():
            point_values.append(point_value)
            questions.append(question)
            answers.append(answer)

    con.close()

    return questions, answers, point_values


if __name__ == '__main__':
   questions, answers = extract_questions_answers_array(filePath, 'notJeopardyDB.db', ['Question'])
   print(questions)
   print(answers)
