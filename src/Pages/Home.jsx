import { useState } from 'react'
import './Home.css'
import { useNavigate } from "react-router-dom"
import { OpenGame, SetOnMessage, SetOnClose, CloseGame } from '../components/WebSocket'

export default function Home() {
  const navigate = useNavigate()
  const [waiting, setWaiting] = useState(false)

  function onAccount() {
    navigate('../login')
  }

  function onProfile() {
    navigate('../profile')
  }

  function onMessage(event) {
    const message = JSON.parse(event.data)
    if (message.operation == "start_game") {
      // TODO: Pass player names
      navigate('/game')
    }
  }

  function onPlay() {
    OpenGame()

    SetOnMessage(onMessage)
    SetOnClose(() => setWaiting(false))

    setWaiting(true)
  }

  function onCancel() {
    CloseGame()
  }

  function onAbout() {
    navigate('../about')
  }

  return (
    <div className="home-div">
      <div className="home-container">
        <div className='flex-item title'>RPS-15</div>
        <br/>
        <p className='flex-item description'>Welcome to RPS-15, a modern take on the classic rock-paper-scissors game</p>
        <br/>
        <button className='flex-item home-button' onClick={onAccount}>
          Account
        </button>
        <br/>
        <button className='flex-item home-button' onClick={onProfile}>
          Profile
        </button>
        <br/>
        <button className='flex-item home-button' onClick={waiting ? onCancel : onPlay}>
          {waiting ? "Cancel" : "Play"}
        </button>
        <br/>
        <button className='flex-item home-button' onClick={onAbout}>
          About
        </button>
      </div>
    </div>
  );
}
