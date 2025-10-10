from flask import Flask, request, jsonify
from dataclasses import dataclass
from enum import Enum


app = Flask(__name__)

class AnswerStatus(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    UNANSWERED = "unanswered"
    TIMEOUT = "timeout"


class GameStatus(Enum):
    FINISHED = "finished"
    IN_PROGRESS = "in_progress"


# mock front-end request template
# curl -X POST -H "Content-type: application/json" -d "{\"category\": \"numbers\", \"timer\": 3, \"answer\": \"decimal\", \"question\": \"humans commonly do math and accounting with this system\", \"answer_status\": \"unanswered\", \"game_id\": 6692, \"game_status\": \"in_progress\"}" http://localhost:5000/submit_answer

# mock game state, we can add more or delete as needed
@dataclass
class GameState:
    timer: int                   # if timer > 0, we can still answer questions, otherwise time is up
    category: str
    question: str
    answer: str
    answer_status: AnswerStatus  # see AnswerStatus class for definition
    game_status: GameStatus      # see GameStatus class for definition
    game_id: int                 # this is the ID tracking which jeopardy! game we're referencing


    def __init__(self, timer, category, question, answer, answer_status, game_status, game_id):
        self.timer = timer
        self.category = category
        self.question = question
        self.answer = answer
        self.answer_status = answer_status
        self.game_status = game_status
        self.game_id = game_id


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    # mock database

    categories = {
        'finance': {
            'in value investing this is the most commonly used metric for finding intrinsic value':
             'discounted cash flow',
            'assets minus liabilities equal shareholders equity, also known as this ....': 'book value'
        },
        'numbers': {
            'the system of numbers widely used in modern computing architecture': 'binary',
            'the system of numbers used for managing permissions in linux file systems': 'octal',
            'humans commonly do math and accounting with this system': 'decimal'
        }
    }

    data = request.get_json()
    game_state = GameState(**data)

    if not data:
        return jsonify({'error': 'Invalid request'})

    user_answer = game_state.answer

    # mock database call
    actual_answer = categories[game_state.category][game_state.question]
    correct = user_answer.replace(' ', '').lower() == actual_answer.replace(' ', '').lower()

    new_game_state = GameState(
        timer=0 if correct else game_state.timer,
        category=game_state.category,
        question=game_state.question,
        answer=game_state.answer,
        answer_status=AnswerStatus.CORRECT.value if correct else AnswerStatus.INCORRECT.value,
        game_status=GameStatus.IN_PROGRESS.value,
        game_id=6692
    )

    return jsonify(new_game_state)
