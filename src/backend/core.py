from flask import Flask, request, jsonify
from flask_cors import CORS
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import src.db.data_driver as data_driver
from src.db.db_api import add_players, extract_questions_data


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


@dataclass
class InitGameRequest:
    players = list[str]

    def __init__(self, players):
        self.players = players


@dataclass
class InitGameResponse:
    game_idx: int
    timer: int  # if timer > 0, we can still answer questions, otherwise time is up
    categories: list[str]
    questions: list[str]
    answers: list[str]
    questions: list[str]
    answers: list[str]
    game_status: GameStatus  # see GameStatus class for definition
    game_id: int  # this is the ID tracking which !jeopardy game we're referencing

    def __init__(self, game_idx, timer, categories, questions, answers, game_status, game_id):
        self.game_idx = game_idx
        self.timer = timer
        self.categories = categories
        self.questions = questions
        self.answers = answers
        self.game_status = game_status
        self.game_id = game_id


# @app.route('/submit_answer', methods=['POST'])
# def submit_answer():
#     player_answer = PlayerAnswer(**request.get_json())
#     global GAME_IDX
#     game_data = GAME_DATA[PLAYER_DATA[player_answer.username]]
#
#     answer_status = AnswerStatus.INCORRECT.value
#
#     if correct_answer(player_answer.user_answer, game_data.answers[player_answer.question_idx]):
#         answer_status = AnswerStatus.CORRECT.value
#         game_data.scores[player_answer.username] += game_data.point_values[player_answer.question_idx]
#     else:
#         game_data.scores[player_answer.username] -= game_data.point_values[player_answer.question_idx]
#
#     return jsonify(
#         PlayerStatus(
#             answer_status,
#             game_data.scores[player_answer.username]
#         )
#     )


# Populates database with player information and pushes required info to frontend
@app.route('/initialize_game', methods=['POST'])
def initialize_game():
    init_game_request = InitGameRequest(**request.get_json())
    db_file = Path(__file__).absolute().parent.parent.joinpath('db/notJeopardyDB.db')

    categories, questions, answers, _points = extract_questions_data(db_file)

    init_game_response = InitGameResponse(
        game_idx=0,
        timer=10,
        categories=categories,
        questions=questions,
        answers=answers,
        game_status=GameStatus.IN_PROGRESS.value,
        game_id=6692
    )

    add_players(db_file, init_game_request.players)

    return jsonify(init_game_response)


def correct_answer(user_answer, actual_answer):
    return user_answer.replace(' ', '').lower() == actual_answer.replace(' ', '').lower()


# just adding an indexer as code documentation for frontend's board-array indexing scheme
def get_idx(row_idx, cat_idx):
    # we have six categories and five clues, so a 5 x 6 board
    limit_idx = 6
    return row_idx * limit_idx + cat_idx


if __name__ == '__main__':
    app.run(debug=True)
