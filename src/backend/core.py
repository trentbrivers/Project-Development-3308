from flask import Flask, request, jsonify
from flask_cors import CORS
from flask.wrappers import Request
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from src.db.db_api import add_players, extract_questions_data, update_player_score


app = Flask(__name__)
CORS(app)


# ENUMS

class AnswerStatus(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    UNANSWERED = "unanswered"
    TIMEOUT = "timeout"


class GameStatus(Enum):
    FINISHED = "finished"
    IN_PROGRESS = "in_progress"


class RoundType(Enum):
    NORMAL = 0
    FINAL = 1


# REQUESTS

@dataclass
class InitGameRequest:
    players: list[str]


@dataclass
class PlayerAnswer:
    question_idx: int     # If 0 <= i <= 29 => jeopardy, 30 <= i <= 60 => double-jeopardy
    user_answer: str
    username: str


@dataclass
class PlayerFinalAnswer:
    user_answer: str
    username: str
    wager: int


# RESPONSES

@dataclass
class PlayerStatus:
    answer_status: str
    player_score: int


@dataclass
class InitGameResponse:
    game_idx: int
    timer: int
    categories: list[str]
    questions: list[str]
    answers: list[str]
    questions: list[str]
    answers: list[str]
    game_status: str
    game_id: int


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


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    return handle_answer_submission(RoundType.NORMAL, request)


@app.route('/submit_final_answer', methods=['POST'])
def submit_final_answer():
    return handle_answer_submission(RoundType.FINAL, request)


def handle_answer_submission(round_type: RoundType, user_request: Request):
    player_answer = PlayerAnswer(**user_request.get_json()) if round_type == RoundType.NORMAL else PlayerFinalAnswer(**user_request.get_json())
    db_file = Path(__file__).absolute().parent.parent.joinpath('db/notJeopardyDB.db')
    _, _, answers, points = extract_questions_data(db_file)

    answer_status = AnswerStatus.INCORRECT.value
    increment_value = points[player_answer.question_idx] if round_type == RoundType.NORMAL else player_answer.wager

    if correct_answer(player_answer.user_answer, answers[player_answer.question_idx]):
        answer_status = AnswerStatus.CORRECT.value
        player_score = update_player_score(db_file, player_answer.username, increment_value)
    else:
        player_score = update_player_score(db_file, player_answer.username, -1 * increment_value)

    return jsonify(PlayerStatus(answer_status, player_score))


def correct_answer(user_answer, actual_answer):
    return user_answer.replace(' ', '').lower() == actual_answer.replace(' ', '').lower()


if __name__ == '__main__':
    app.run(debug=True)
