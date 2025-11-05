import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import src.db.data_driver as data_driver

app = Flask(__name__)
CORS(app)

class AnswerStatus(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    UNANSWERED = "unanswered"
    TIMEOUT = "timeout"


class GameStatus(Enum):
    FINISHED = "finished"
    IN_PROGRESS = "in_progress"


# mock game state, we can add more or delete as needed
@dataclass
class GameState:
    timer: int                    # if timer > 0, we can still answer questions, otherwise time is up
    category: str
    questions: list[str]
    answers: list[str]
    answer_status: AnswerStatus   # see AnswerStatus class for definition
    game_status: GameStatus       # see GameStatus class for definition
    current_score: int            # current player score
    game_id: int                  # this is the ID tracking which !jeopardy game we're referencing


    def __init__(self, timer, category, questions, answers, answer_status, game_status, current_score, game_id):
        self.timer = timer
        self.category = category
        self.questions = questions
        self.answers = answers
        self.answer_status = answer_status
        self.game_status = game_status
        self.current_score = current_score
        self.game_id = game_id


#To do: Migrate question specific attributes from GameState to Question?
@dataclass
class PlayerAnswer:
    question_idx: int
    user_answer: str
    username: str

    def __init__(self, question_idx, user_answer, username):
        self.question_idx = question_idx
        self.user_answer = user_answer
        self.username = username


@dataclass
class PlayerStatus:
    answer_status: AnswerStatus
    player_score: int

    def __init__(self, answer_status, player_score):
        self.answer_status = answer_status
        self.player_score = player_score


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    player_answer = PlayerAnswer(**data)
    user_answer = player_answer.user_answer

    # mock database call
    # actual_answer = categories[game_state.category][game_state.question]
    # correct = user_answer.replace(' ', '').lower() == actual_answer.replace(' ', '').lower()

    return jsonify(PlayerStatus(AnswerStatus.CORRECT.value, 200))

# Initialization function called to populate data on the frontend
# Generates the game state for internal tracking and pushes required information to frontend
@app.route('/initialize_game', methods=['GET'])
def initialize_game():
    ### On initialize call to database to generate 30 questions (6 categories of 5 questions)  ###

    ### will need to loop through and select questions ###

    mock_questions = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5',
                      'q6', 'q7', 'q8', 'q9', 'q10', 'q11',
                      'q12', 'q13', 'q14', 'q15', 'q16', 'q17',
                      'q18', 'q19', 'q20', 'q21', 'q22', 'q23',
                      'q24', 'q25', 'q26', 'q27', 'q28', 'q29']

    mock_answers = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5',
                    'a6', 'a7', 'a8', 'a9', 'a10', 'a11',
                    'a12', 'a13', 'a14', 'a15', 'a16', 'a17',
                    'a18', 'a19', 'a20', 'a21', 'a22', 'a23',
                    'a24', 'a25', 'a26', 'a27', 'a28', 'a29']

    questions, answers = data_driver.extract_questions_answers_array(Path.cwd().parent.joinpath('db'), 'notJeopardyDB.db', ['Question'])
    print(questions)
    print(answers)

    # Dummy placeholders for now
    start_game_state = GameState(
        timer=1000,
        category='finance',
        questions=questions,
        answers=answers,
        answer_status=AnswerStatus.UNANSWERED.value,
        game_status=GameStatus.IN_PROGRESS.value,
        current_score=0,
        game_id=6692
    )

    return jsonify(start_game_state)


# just adding an indexer as code documentation for frontend's board-array indexing scheme
def get_idx(row_idx, cat_idx):
    # we have six categories and five clues, so a 5 x 6 board
    limit_idx = 6
    return row_idx * limit_idx + cat_idx


if __name__ == '__main__':
    app.run(debug=True)
