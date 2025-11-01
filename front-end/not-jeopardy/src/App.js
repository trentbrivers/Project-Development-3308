import { useState } from 'react';

export default function App() {
  //React is a Single Page Application framework, so everything needs to be handled by this main App component function.
  const [currentScreen, setCurrentScreen] = useState('title');
  // This is the main Array of tiles for the game board. It is a 1D array representing a 6x5 grid. 
  const [tiles, setTiles] = useState(
    Array(30).fill("$200", 0, 6)
      .fill("$400", 6, 12)
      .fill("$600", 12, 18)
      .fill("$800", 18, 24)
      .fill("$1000", 24, 30)
  );

  const handleStartGame = () => setCurrentScreen('board');
  const handleSelectQuestion = () => setCurrentScreen('question');
  const handleReturnToBoard = () => setCurrentScreen('board');

  return (
    <div className="App">
      {currentScreen === 'title' && (
        <TitleScreen onStart={handleStartGame} />
      )}
      {currentScreen === 'board' && (
        <GameBoard onSelectQuestion={handleSelectQuestion} tiles={tiles} setTiles = {setTiles}/>
      )}
      {currentScreen === 'question' && (
        <QuestionScreen onBack={handleReturnToBoard} />
      )}
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

function GameBoard({ onSelectQuestion, tiles, setTiles }) {

  function handleTileClick(index) {
    // Logic to handle tile click, e.g., mark as answered
    if (tiles[index] === null) return; // Already answered
    const newTiles = tiles.slice();
    newTiles[index] = null; // Mark as answered
    console.log(`Tile ${index} clicked`);
    console.log(newTiles);
    setTiles(newTiles);
    onSelectQuestion();
  }

  return (
    <>
    <div className = "board-row"> 
    <Category value={"Category 1"}/>
    <Category value={"Category 2"}/>
    <Category value={"Category 3"}/>
    <Category value={"Category 4"}/>
    <Category value={"Category 5"}/>
    <Category value={"Category 6"}/>
    </div>

    <div className = "board-row">
    <Money value={tiles[0]} onMoneyClick={() => handleTileClick(0)}/>
    <Money value={tiles[1]} onMoneyClick={() => handleTileClick(1)}/>
    <Money value={tiles[2]} onMoneyClick={() => handleTileClick(2)}/>
    <Money value={tiles[3]} onMoneyClick={() => handleTileClick(3)}/>
    <Money value={tiles[4]} onMoneyClick={() => handleTileClick(4)}/>
    <Money value={tiles[5]} onMoneyClick={() => handleTileClick(5)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[6]} onMoneyClick={() => handleTileClick(6)}/>
    <Money value={tiles[7]} onMoneyClick={() => handleTileClick(7)}/>
    <Money value={tiles[8]} onMoneyClick={() => handleTileClick(8)}/>
    <Money value={tiles[9]} onMoneyClick={() => handleTileClick(9)}/>
    <Money value={tiles[10]} onMoneyClick={() => handleTileClick(10)}/>
    <Money value={tiles[11]} onMoneyClick={() => handleTileClick(11)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[12]} onMoneyClick={() => handleTileClick(12)}/>
    <Money value={tiles[13]} onMoneyClick={() => handleTileClick(13)}/>
    <Money value={tiles[14]} onMoneyClick={() => handleTileClick(14)}/>
    <Money value={tiles[15]} onMoneyClick={() => handleTileClick(15)}/>
    <Money value={tiles[16]} onMoneyClick={() => handleTileClick(16)}/>
    <Money value={tiles[17]} onMoneyClick={() => handleTileClick(17)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[18]} onMoneyClick={() => handleTileClick(18)}/>
    <Money value={tiles[19]} onMoneyClick={() => handleTileClick(19)}/>
    <Money value={tiles[20]} onMoneyClick={() => handleTileClick(20)}/>
    <Money value={tiles[21]} onMoneyClick={() => handleTileClick(21)}/>
    <Money value={tiles[22]} onMoneyClick={() => handleTileClick(22)}/>
    <Money value={tiles[23]} onMoneyClick={() => handleTileClick(23)}/>  
    </div>

    <div className = "board-row">
    <Money value={tiles[24]} onMoneyClick={() => handleTileClick(24)}/>
    <Money value={tiles[25]} onMoneyClick={() => handleTileClick(25)}/>
    <Money value={tiles[26]} onMoneyClick={() => handleTileClick(26)}/>
    <Money value={tiles[27]} onMoneyClick={() => handleTileClick(27)}/>
    <Money value={tiles[28]} onMoneyClick={() => handleTileClick(28)}/>
    <Money value={tiles[29]} onMoneyClick={() => handleTileClick(29)}/>  
    </div>

    </>
  );
}

function QuestionScreen({ onBack }) {
  const [answer, setAnswer] = useState(''); // store the player's input

  const handleChange = (e) => {
    setAnswer(e.target.value); // update state whenever the user types
  };

  const handleSubmit = () => {
    console.log('User answer:', answer);
    onBack();
  };

  return (
    <div>
      <h3>Question: What is React?</h3>
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

function Category ( {value} ) {
  return <div className="cat-tile">{value}</div>;
}

function Money ( {value, onMoneyClick} ) {
  return <button className="money-tile" onClick={onMoneyClick}>{value}</button>;
}

/*
function Money ( {value} ) {
  function handleClick() {

  }
  return <button className="money-tile">{value}</button>;
}

function Category ( {value} ) {
  return <button className="cat-tile">{value}</button>;
}

export default function Tilescreen() {
  return (
    <> 
    <div className = "board-row"> 
    <Category value={"Category 1"}/>
    <Category value={"Category 2"}/>
    <Category value={"Category 3"}/>
    <Category value={"Category 4"}/>
    <Category value={"Category 5"}/>
    <Category value={"Category 6"}/>
    </div>


    <div className = "board-row">
    <Money value={"$200"}/>
    <Money value={"$200"}/>
    <Money value={"$200"}/>
    <Money value={"$200"}/>
    <Money value={"$200"}/>
    <Money value={"$200"}/>  
    </div>

    <div className = "board-row">
    <Money value={"$400"}/>
    <Money value={"$400"}/>
    <Money value={"$400"}/>
    <Money value={"$400"}/>
    <Money value={"$400"}/>
    <Money value={"$400"}/>  
    </div>

    <div className = "board-row">
    <Money value={"$600"}/>
    <Money value={"$600"}/>
    <Money value={"$600"}/>
    <Money value={"$600"}/>
    <Money value={"$600"}/>
    <Money value={"$600"}/>  
    </div>

    <div className = "board-row">
    <Money value={"$800"}/>
    <Money value={"$800"}/>
    <Money value={"$800"}/>
    <Money value={"$800"}/>
    <Money value={"$800"}/>
    <Money value={"$800"}/>  
    </div>

    <div className = "board-row">
    <Money value={"$1000"}/>
    <Money value={"$1000"}/>
    <Money value={"$1000"}/>
    <Money value={"$1000"}/>
    <Money value={"$1000"}/>
    <Money value={"$1000"}/>  
    </div>

    </>
  )
}
*/

/*

function Square({value, onSquareClick}) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

export default function Board() {
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));

  function handleClick(i) {
    if (calculateWinner(squares) || squares[i]) {
      return;
    }
    const nextSquares = squares.slice();
    if (xIsNext) {
      nextSquares[i] = 'X';
    } else {
      nextSquares[i] = 'O';
    }
    setSquares(nextSquares);
    setXIsNext(!xIsNext);
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = 'Winner: ' + winner;
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
  }

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
*/
