import React, { useEffect, useRef } from 'react'
import './Game.css'
import { useState } from 'react'
import Select from 'react-select';
import PieChart from '../components/PieChart'
import { SetOnMessage, Send, CloseGame } from '../components/WebSocket';
import { useNavigate } from 'react-router-dom';

const Game = (props) => {
  const navigate = useNavigate();

  const [round, setRound] = useState(1);
  const [player, setPlayer] = useState("");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [playerScore, setPlayerScore] = useState(0);
  const [opponent, setOpponent] = useState("");
  const [opponentScore, setOpponentScore] = useState(0);
  const [gameMessage, setGameMessage] = useState("Starting game...");
  const [selectedOption, setSelectedOption] = useState(0); // for dropdown selection
  const [canMove, setCanMove] = useState(false);
  const [moveCounts, setMoveCounts] = useState({});
  const cleanupCount = useRef(0);

  async function updateMoveDistribution() {
    var xhr = new XMLHttpRequest()
    xhr.open("GET", `/api/user/${opponent}`)

    xhr.onreadystatechange = (e) => {
      if (xhr.readyState === 4) {
        const response = JSON.parse(xhr.responseText)
        setMoveCounts(response.MoveCounts)
      }
    }

    xhr.send()
  }

  useEffect(() => {
    SetOnMessage(onMessage)
    Send(JSON.stringify({"operation": "get_names"}))
    return function cleanup() {
      if (cleanupCount.current > 0) {
        CloseGame()
      }
      cleanupCount.current++
    }
  }, [])

  useEffect(() => {
    if (opponent !== "") {
      updateMoveDistribution()
    }
  }, [opponent, round])

  function onMessage(event) {
    const message = JSON.parse(event.data)

    switch (message.operation) {
      case "send_names":
        setPlayer(message.you)
        setOpponent(message.opponent)
        break
      case "start_round":
        setRound(message.number)
        setGameMessage("Select your move")
        setCanMove(true)
        break
      case "end_round":
        setGameMessage(message.message)
        setCanMove(false)
        setPlayerScore(message.you)
        setOpponentScore(message.opponent)
        break
      case "send_message":
        setMessages(messages => [...messages, message])
        break
      case "end_game":
        setGameMessage(`${message.winner} WINS!`)
        setTimeout(() => navigate("/"), 5000)
        break
    }
  }

  const onSendMove = (e) => {
    e.preventDefault();

    Send(JSON.stringify({"operation": "send_move", "move": selectedOption.value}))
    setCanMove(false)
  }

  // For submitting chats
  const onSubmit = (e) => {
    e.preventDefault();
  
    Send(JSON.stringify({"operation": "send_message", "message": message}))
    setMessage('');
  }

  const options = [
    {value: 0, label: "Rock"},
    {value: 1, label: "Fire"},
    {value: 2, label: "Scissors"},
    {value: 3, label: "Snake"},
    {value: 4, label: "Human"},
    {value: 5, label: "Tree"},
    {value: 6, label: "Wolf"},
    {value: 7, label: "Sponge"},
    {value: 8, label: "Paper"},
    {value: 9, label: "Air"},
    {value: 10, label: "Water"},
    {value: 11, label: "Dragon"},
    {value: 12, label: "Devil"},
    {value: 13, label: "Lightning"},
    {value: 15, label: "Gun"}
  ];

  const selectStyles = {
    control: (base, state) => ({
      ...base,
      background: "#1e1e1e",
      width: "125px",
      borderRadius: state.isFocused ? "3px 3px 0 0" : 3,
      boxShadow: state.isFocused ? null : null,
      "&:hover": {
      }
    }),
    singleValue: (provided, state) => ({
      ...provided,
      color: 'inherit',
      background: "#1e1e1e",
    }),
    menu: (provided, state) => ({
      ...provided,
      'z-index': 9,
      background: "#1e1e1e",
    }),
    multiValue: (provided, state) => ({
      ...provided,
      color: state.isDisabled ? "#000" : "#fff",
      background: "#1e1e1e",
    }),
  };

  return (
    <div className='game-page'>
      <div className='page-container'>
        <div className='round-tracker page-item'>
          Round {round}
        </div>
        <div className='game-message page-item'>
          {gameMessage}
        </div>
        <div className='game-container page-item'>
          <div className='player-side game-item'>
          <div className='opponent-score'>
              {player}: {playerScore}
            </div>
            <Select 
              styles={selectStyles}
              className='select-sign'
              value={selectedOption}
              onChange={setSelectedOption}
              options={options}  
            />
            <button onClick={onSendMove} disabled={!canMove}>
              Send Move
            </button>
          </div>
          <div className='opponent-side game-item'>
            <div className='opponent-score'>
              {opponent}: {opponentScore}
            </div>
            <div className='chart'>
              <PieChart data={moveCounts} />
            </div>
          </div>
        </div>
        <div className='chat-container page-item'>
          <div className='chat-display'>
            {messages.map(({ username, message }, i) => (
              <div key={i}>{username}: {message}</div>
            ))}
          </div>
          <form className='chat-input' onSubmit={onSubmit}>
            <label htmlFor='message'></label>
            <input 
              type="text"
              id='message'
              name='message'
              className='message-input'
              value={message}
              placeholder='Message: (Enter to submit)'
              onChange={(e) => setMessage(e.target.value)}
            />
          </form>
        </div>
      </div>
    </div>
  )
}

export default Game