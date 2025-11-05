from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import src.db.data_driver as data_driver

import os

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
current_dir_path = Path(current_directory)

app = Flask(__name__)
CORS(app)


game_data_dict = dict()


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
    questions: list[str]
    answers: list[str]
    game_status: GameStatus       # see GameStatus class for definition
    game_id: int                  # this is the ID tracking which !jeopardy game we're referencing


    def __init__(self, timer, questions, answers, game_status, game_id):
        self.timer = timer
        self.questions = questions
        self.answers = answers
        self.game_status = game_status
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

    game_id = 6692 # should not be hard-coded
    _questions, answers, point_values = game_data_dict[game_id]

    actual_answer = answers[player_answer.question_idx]
    answer_status = AnswerStatus.INCORRECT.value

    if user_answer.replace(' ', '').lower() == actual_answer.replace(' ', '').lower():
        answer_status = AnswerStatus.CORRECT.value

    return jsonify(PlayerStatus(answer_status, point_values[player_answer.question_idx]))


# Initialization function called to populate data on the frontend
# Generates the game state for internal tracking and pushes required information to frontend
@app.route('/initialize_game', methods=['GET'])
def initialize_game():
    questions, answers, point_values = data_driver.extract_questions_answers_array(
        current_dir_path.parent.joinpath('db'),
        'notJeopardyDB.db',
        ['Question']
    )

    game_state = GameState(
        timer=1000,
        questions=questions,
        answers=answers,
        game_status=GameStatus.IN_PROGRESS.value,
        game_id=6692
    )

    game_data_dict.setdefault(game_state.game_id, (questions, answers, point_values))

    return jsonify(game_state)


# just adding an indexer as code documentation for frontend's board-array indexing scheme
def get_idx(row_idx, cat_idx):
    # we have six categories and five clues, so a 5 x 6 board
    limit_idx = 6
    return row_idx * limit_idx + cat_idx


if __name__ == '__main__':
    app.run(debug=True)
