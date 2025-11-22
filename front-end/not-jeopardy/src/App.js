import { useState } from 'react';

export default function App() {
  //React is a Single Page Application framework, so everything needs to be handled by this main App component function.
  const [currentScreen, setCurrentScreen] = useState('title');
  // This is the main Array of tiles for the game board. It is a 1D array representing a 6x5 grid. 
  const [tiles, setTiles] = useState(
    Array(30).fill("$100", 0, 6)
      .fill("$200", 6, 12)
      .fill("$300", 12, 18)
      .fill("$400", 18, 24)
      .fill("$500", 24, 30)
  );
  const [questions, setQuestions] = useState(
    Array(61).fill(null)
  );
  const [answers, setAnswers] = useState(
    Array(61).fill(null)
  );
  const [categories, setCategories] = useState(
    Array(6).fill(null)
  );
  const [selected, setSelected] = useState(null);
  const [score, setScore] = useState(null);
  const [status, setStatus] = useState(null);
  const [totalSelected, setTotalSelected] = useState(0);

  const handleStartGame = () => {
    const postData = {"players": ["Trent"]}
    fetch('http://localhost:5000/initialize_game', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(postData)
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // This returns a Promise that resolves to your JSON
    })
    .then(data => {
      console.log('Backend response data:', data);
      setCategories(data['categories']);
      setQuestions(data['questions']);
      setAnswers(data['answers']);
    })
    .catch(error => {
      console.error('Fetch error:', error);
    });
    setCurrentScreen('board');
  };

  const handleSelectQuestion = (i) => {
    const newTiles = tiles.slice();
    newTiles[i] = null; 
    setTiles(newTiles); 
    setSelected(i);
    setTotalSelected(totalSelected+1);
    setCurrentScreen('question');
  };

  const handleSubmitAnswer = (answer) => {
    const postData = {
      "username": "Trent",
      "question_idx":selected,
      "user_answer": answer
    }
    fetch('http://localhost:5000/submit_answer',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }, 
      body: JSON.stringify(postData)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // This returns a Promise that resolves to your JSON
    })
        .then(data => {
      console.log('Backend response data:', data);
      setScore(data['player_score']);
      setStatus(data['answer_status']);

    })
    .catch(error => {
      console.error('Fetch error:', error);
    });
    setCurrentScreen('answer');
  };
  const handleReturnToBoard = () => setCurrentScreen('board'); 
  const handleGameEnd = () => setCurrentScreen('finish');

  return (
    <div className="App">
      {currentScreen === 'title' && (
        <TitleScreen onStart={handleStartGame} />
      )}
      {currentScreen === 'board' && (
        <GameBoard onSelectQuestion={handleSelectQuestion} tiles={tiles} categories={categories}/>
      )}
      {currentScreen === 'question' && (
        <QuestionScreen onSubmit={handleSubmitAnswer} question={questions[selected]}/>
      )}
      {currentScreen === 'answer' && (
        <AnswerScreen onReturn={totalSelected < 30 ? handleReturnToBoard:handleGameEnd} answer={answers[selected]} answer_status={status} player_score={score}/>
      )}
      {
      currentScreen === 'finish' && (
        <GameOver final_score={score}/>
        )
      }
    </div>
  );
}

//This component presents the Title Screen consisting of 
function TitleScreen({ onStart }) {
    return (
        <div className="title-screen">
            <img
                src="/notJeopardy-Logo.png"
                alt="!Jeopardy Logo"
            />
            <button onClick={onStart} className="button-design" >
                Start Game
            </button>
        </div>
    );
}

function GameBoard({ onSelectQuestion, tiles, categories}) {

  function handleClick(i){
    if (tiles[i] === null) return;
    onSelectQuestion(i);
  }

  return (
    <div className={"board-frame"}>
    <div className = "board-row"> 
    <Category value={categories[0]}/>
    <Category value={categories[1]}/>
    <Category value={categories[2]}/>
    <Category value={categories[3]}/>
    <Category value={categories[4]}/>
    <Category value={categories[5]}/>
    </div>

    <div className = "board-row">
    <Money value={tiles[0]} onMoneyClick={() => handleClick(0)}/>
    <Money value={tiles[1]} onMoneyClick={() => handleClick(1)}/>
    <Money value={tiles[2]} onMoneyClick={() => handleClick(2)}/>
    <Money value={tiles[3]} onMoneyClick={() => handleClick(3)}/>
    <Money value={tiles[4]} onMoneyClick={() => handleClick(4)}/>
    <Money value={tiles[5]} onMoneyClick={() => handleClick(5)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[6]} onMoneyClick={() => handleClick(6)}/>
    <Money value={tiles[7]} onMoneyClick={() => handleClick(7)}/>
    <Money value={tiles[8]} onMoneyClick={() => handleClick(8)}/>
    <Money value={tiles[9]} onMoneyClick={() => handleClick(9)}/>
    <Money value={tiles[10]} onMoneyClick={() => handleClick(10)}/>
    <Money value={tiles[11]} onMoneyClick={() => handleClick(11)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[12]} onMoneyClick={() => handleClick(12)}/>
    <Money value={tiles[13]} onMoneyClick={() => handleClick(13)}/>
    <Money value={tiles[14]} onMoneyClick={() => handleClick(14)}/>
    <Money value={tiles[15]} onMoneyClick={() => handleClick(15)}/>
    <Money value={tiles[16]} onMoneyClick={() => handleClick(16)}/>
    <Money value={tiles[17]} onMoneyClick={() => handleClick(17)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[18]} onMoneyClick={() => handleClick(18)}/>
    <Money value={tiles[19]} onMoneyClick={() => handleClick(19)}/>
    <Money value={tiles[20]} onMoneyClick={() => handleClick(20)}/>
    <Money value={tiles[21]} onMoneyClick={() => handleClick(21)}/>
    <Money value={tiles[22]} onMoneyClick={() => handleClick(22)}/>
    <Money value={tiles[23]} onMoneyClick={() => handleClick(23)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[24]} onMoneyClick={() => handleClick(24)}/>
    <Money value={tiles[25]} onMoneyClick={() => handleClick(25)}/>
    <Money value={tiles[26]} onMoneyClick={() => handleClick(26)}/>
    <Money value={tiles[27]} onMoneyClick={() => handleClick(27)}/>
    <Money value={tiles[28]} onMoneyClick={() => handleClick(28)}/>
    <Money value={tiles[29]} onMoneyClick={() => handleClick(29)}/>  
    </div>

    </div>
  );
}

function QuestionScreen({ onSubmit, question }) {
  const [answer, setAnswer] = useState(''); // store the player's input

  const handleChange = (e) => {
    setAnswer(e.target.value); // update state whenever the user types
  };

  const handleSubmit = () => {
    console.log('User answer:', answer);
    onSubmit(answer);
  };

  return (
    <div className="question-screen">
      <h3>Question: {question}</h3>
      <input
        type="text"
        placeholder="Your answer"
        value={answer}
        onChange={handleChange}
      />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

function AnswerScreen({ onReturn, answer, answer_status, player_score }) {
    return (
      <div className="answer-screen">
        <h1 className="answer-reveal"> Official Answer: {answer}</h1> <br></br>

          <h2 className={`answer-status ${answer_status === "correct" ? "correct" : "incorrect"}`}>
              {answer_status}
          </h2>

          <p className={"score-display"}>
            {(player_score >= 0 ? "$" : "-$") + Math.abs(player_score)}
        </p>
        <button onClick={onReturn} className="button-design" >
            Return to Game
        </button>
      </div>
    );
}

function GameOver({final_score}) {
  return (
    <div className={"game-over-screen"}>
        <img
            src="/notJeopardy-Logo.png"
            alt="!Jeopardy Logo"
        />
      <h1 className={"game-over-text"}>CONGRATULATIONS!</h1>
      <p className={"score-display"}>Final Score: ${final_score}</p>
    </div>
  )
}

function Category ( {value} ) {
  return <div className="cat-tile">{value}</div>;
}

function Money ( {value, onMoneyClick} ) {
  return <button className="money-tile" onClick={onMoneyClick}>{value}</button>;
}

