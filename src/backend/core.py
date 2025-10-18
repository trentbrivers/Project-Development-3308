from flask import Flask, request, jsonify, render_template
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
# NOTE: to run app --> flask --app core run --debug

# mock game state, we can add more or delete as needed
@dataclass
class GameState:
    timer: int                   # if timer > 0, we can still answer questions, otherwise time is up
    category: str
    question: str
    question_value: int
    answer: str
    answer_status: AnswerStatus  # see AnswerStatus class for definition
    game_status: GameStatus      # see GameStatus class for definition
    current_score: int            # current player score
    game_id: int                 # this is the ID tracking which jeopardy! game we're referencing


    def __init__(self, timer, category, question, question_value, answer, answer_status, game_status, current_score, game_id):
        self.timer = timer
        self.category = category
        self.question = question
        self.question_value = question_value
        self.answer = answer
        self.answer_status = answer_status
        self.game_status = game_status
        self.current_score = current_score
        self.game_id = game_id

#To do: Migrate question specific attributes from GameState to Question?
@dataclass
class Question:
    question: str
    question_value: int
    answer: str
    answer_status: AnswerStatus
    def __init__(self, question, question_value, answer, answer_status):
        self.question = question
        self.question_value = question_value
        self.answer = answer
        self.answer_status = answer_status


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
        question_value=game_state.question_value,
        answer=game_state.answer,
        answer_status=AnswerStatus.CORRECT.value if correct else AnswerStatus.INCORRECT.value,
        game_status=GameStatus.IN_PROGRESS.value,
        current_score=game_state.current_score, #plus if correct, minus if incorrect will need to add
        game_id=6692
    )

    return jsonify(new_game_state)

#Initial function called to populate data on the frontend
#Generates the game state for internal tracking and pushes
#required information to frontend
@app.route('/initialize_game', methods=['GET'])
def initialize_game():
    ### On initialize call to database to generate 30 questions (6 categories of 5 questions)  ###

    ### will need to loop through and select questions ###

    # Dummy placeholders for now
    start_game_state = GameState(
        timer=1000,  #don't need to use for now
        category='finance',
        question='in value investing this is the most commonly used metric for finding intrinsic value',
        question_value=1000,
        answer='discounted cash flow',
        answer_status=AnswerStatus.UNANSWERED.value,
        game_status=GameStatus.IN_PROGRESS.value,
        current_score=0,
        game_id=6692
    )

    return jsonify(start_game_state)


# just adding an indexer as code documentation for frontend's board-array indexing scheme
def get_idx(cat_idx, clue_idx):
    # we have six categories and five clues, so a 5 x 6 board
    m, n = (5, 6)
    assert clue_idx < m and cat_idx < n

    return cat_idx * n + clue_idx
