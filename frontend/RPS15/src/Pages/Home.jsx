import './Home.css'
import { useNavigate } from "react-router-dom"

export default function Home() {
  const navigate = useNavigate()

  function onAccount() {
    navigate('../login')
  }

  function onPlay() {
    navigate('../game')
  }

  function onAbout() {
    navigate('../about')
  }

  return (
    <div className="home-div">
      <div className="home-container">
        <p className='flex-item title'>RPS-15</p>
        <p className='flex-item description'>Welcom to RPS-15, a modern take on the classic rock-paper-scissors game</p>
        <button className='flex-item home-button' onClick={onAccount}>
          Account
        </button>
        <br/>
        <button className='flex-item home-button' onClick={onPlay}>
          Play
        </button>
        <br/>
        <button className='flex-item home-button' onClick={onAbout}>
          About
        </button>
      </div>
    </div>
  );
}
