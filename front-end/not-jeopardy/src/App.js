import { useState } from 'react';

export default function App() {
  //React is a Single Page Application framework, so everything needs to be handled by this main App component function.
  const [currentScreen, setCurrentScreen] = useState('title');
  // This is the main Array of tiles for the game board. It is a 1D array representing a 6x5 grid. 
  const [tiles, setTiles] = useState(
    Array(60).fill("$100", 0, 6)
      .fill("$200", 6, 12)
      .fill("$300", 12, 18)
      .fill("$400", 18, 24)
      .fill("$500", 24, 30)
      .fill("$200", 30, 36)
      .fill("$400", 36, 42)
      .fill("$600", 42, 48)
      .fill("$800", 48, 54)
      .fill("$1000", 54, 60)
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
  const [userName, setUserName] = useState("Trent");
  const [round, setRound] = useState(0); // 0 for Jeopardy, 1 for Double Jeopardy, 2 for Final Jeopardy

  const handleTitleStart = (userInput = userName) => {
    setCurrentScreen('menu');
    setUserName(userInput);
  }

  const handleStartGame = () => {
    console.log(userName);
    const postData = {"players": [userName]}
    fetch('/initialize_game', {
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
      "username": userName,
      "question_idx":selected,
      "user_answer": answer
    }
    fetch('/submit_answer',{
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
  const handleDouble = () => {
    setRound(1);
    setCurrentScreen('double');
  }


  return (
    <div className="App">
      {currentScreen === 'title' && (
        <TitleScreen onStart={handleTitleStart}/>
      )}
      {currentScreen === 'menu' && (
        <MainMenu onStart={handleStartGame}/>
      )}
      {currentScreen === 'board' && (
        <GameBoard onSelectQuestion={handleSelectQuestion} tiles={tiles} categories={categories} round={round}/>
      )}
      {currentScreen === 'question' && (
        <QuestionScreen onSubmit={handleSubmitAnswer} question={questions[selected]}/>
      )}
      {currentScreen === 'answer' && (
        <AnswerScreen onReturn={totalSelected !== 30 ? totalSelected !== 60 ? handleReturnToBoard:handleGameEnd:handleDouble} answer={answers[selected]} answer_status={status} player_score={score}/>
      )}
      {currentScreen === 'double' && (
        <DoubleJeopardy onContinue={handleReturnToBoard}/>
      )}
      {currentScreen === 'finish' && (
        <GameOver final_score={score} onMenu={handleTitleStart}/>
      )}
    </div>
  );
}


//This component presents the Title Screen consisting of 
function TitleScreen({ onStart }) {
  const [userInput, setUserInput] = useState(''); // store the player's input

  const handleChange = (e) => {
    setUserInput(e.target.value); // update state whenever the user types
  };

  const handleStart = () => {
    onStart(userInput);
  }

    return (
        <div className="title-screen">
            <img
                src="/notJeopardy-Logo.png"
                alt="!Jeopardy Logo"
            />
            <input
                type="text"
                placeholder="Enter Your Username"
                value={userInput}
                onChange={handleChange}
              />
            <button onClick={handleStart} className="button-design" >
                Start
            </button>
        </div>
    );
}

function MainMenu({onStart}){
   return (
        <div className="title-screen">
            <img
                src="/notJeopardy-Logo.png"
                alt="!Jeopardy Logo"
            />
            <button onClick={onStart} className="button-design" >
                Start Game
            </button>
            <button className="button-design" >
                Leaderboard
            </button>
        </div>
    );
}

function GameBoard({ onSelectQuestion, tiles, categories, round}) {
  var cat_mod = round * 6; 
  var tile_mod = round * 30;

  function handleClick(i){
    if (tiles[i] === null) return;
    onSelectQuestion(i);
  }

  return (
    <div className={"board-frame"}>
    <div className = "board-row"> 
    <Category value={categories[0+cat_mod]}/>
    <Category value={categories[1+cat_mod]}/>
    <Category value={categories[2+cat_mod]}/>
    <Category value={categories[3+cat_mod]}/>
    <Category value={categories[4+cat_mod]}/>
    <Category value={categories[5+cat_mod]}/>
    </div>

    <div className = "board-row">
    <Money value={tiles[0+tile_mod]} onMoneyClick={() => handleClick(0+tile_mod)}/>
    <Money value={tiles[1+tile_mod]} onMoneyClick={() => handleClick(1+tile_mod)}/>
    <Money value={tiles[2+tile_mod]} onMoneyClick={() => handleClick(2+tile_mod)}/>
    <Money value={tiles[3+tile_mod]} onMoneyClick={() => handleClick(3+tile_mod)}/>
    <Money value={tiles[4+tile_mod]} onMoneyClick={() => handleClick(4+tile_mod)}/>
    <Money value={tiles[5+tile_mod]} onMoneyClick={() => handleClick(5+tile_mod)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[6+tile_mod]} onMoneyClick={() => handleClick(6+tile_mod)}/>
    <Money value={tiles[7+tile_mod]} onMoneyClick={() => handleClick(7+tile_mod)}/>
    <Money value={tiles[8+tile_mod]} onMoneyClick={() => handleClick(8+tile_mod)}/>
    <Money value={tiles[9+tile_mod]} onMoneyClick={() => handleClick(9+tile_mod)}/>
    <Money value={tiles[10+tile_mod]} onMoneyClick={() => handleClick(10+tile_mod)}/>
    <Money value={tiles[11+tile_mod]} onMoneyClick={() => handleClick(11+tile_mod)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[12+tile_mod]} onMoneyClick={() => handleClick(12+tile_mod)}/>
    <Money value={tiles[13+tile_mod]} onMoneyClick={() => handleClick(13+tile_mod)}/>
    <Money value={tiles[14+tile_mod]} onMoneyClick={() => handleClick(14+tile_mod)}/>
    <Money value={tiles[15+tile_mod]} onMoneyClick={() => handleClick(15+tile_mod)}/>
    <Money value={tiles[16+tile_mod]} onMoneyClick={() => handleClick(16+tile_mod)}/>
    <Money value={tiles[17+tile_mod]} onMoneyClick={() => handleClick(17+tile_mod)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[18+tile_mod]} onMoneyClick={() => handleClick(18+tile_mod)}/>
    <Money value={tiles[19+tile_mod]} onMoneyClick={() => handleClick(19+tile_mod)}/>
    <Money value={tiles[20+tile_mod]} onMoneyClick={() => handleClick(20+tile_mod)}/>
    <Money value={tiles[21+tile_mod]} onMoneyClick={() => handleClick(21+tile_mod)}/>
    <Money value={tiles[22+tile_mod]} onMoneyClick={() => handleClick(22+tile_mod)}/>
    <Money value={tiles[23+tile_mod]} onMoneyClick={() => handleClick(23+tile_mod)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[24+tile_mod]} onMoneyClick={() => handleClick(24+tile_mod)}/>
    <Money value={tiles[25+tile_mod]} onMoneyClick={() => handleClick(25+tile_mod)}/>
    <Money value={tiles[26+tile_mod]} onMoneyClick={() => handleClick(26+tile_mod)}/>
    <Money value={tiles[27+tile_mod]} onMoneyClick={() => handleClick(27+tile_mod)}/>
    <Money value={tiles[28+tile_mod]} onMoneyClick={() => handleClick(28+tile_mod)}/>
    <Money value={tiles[29+tile_mod]} onMoneyClick={() => handleClick(29+tile_mod)}/>  
    </div>

    </div>
  );
}

function Category ( {value} ) {
  return <div className="cat-tile">{value}</div>;
}

function Money ( {value, onMoneyClick} ) {
  return <button className="money-tile" onClick={onMoneyClick}>{value}</button>;
}

function DoubleJeopardy ({onContinue}) {

  function handleContinue() {
    onContinue();
  }

  return (
    <div className="double-jeopardy-tile">
      <h2>Double Jeopardy!</h2>
      <button onClick={handleContinue}>Continue</button>
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

function GameOver({final_score, onMenu}) {

  function handleMenu() {
    onMenu();
  }

  return (
    <div className={"game-over-screen"}>
        <img
            src="/notJeopardy-Logo.png"
            alt="!Jeopardy Logo"
        />
      <h1 className={"game-over-text"}>CONGRATULATIONS!</h1>
      <p className={"score-display"}>Final Score: ${final_score}</p>
      <button onClick = {handleMenu} className="button-design" >
          Main Menu 
      </button>
    </div>
  )
}

