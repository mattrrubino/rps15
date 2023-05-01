import React from 'react'
import "./About.css"
import rps from "../assets/rps15.png"
import { Link, useNavigate } from "react-router-dom"

export default function About() {
  return (
    <div className="about--page--container">
      <h1>How To Play</h1>
      <h4>Pick one of fifteen possible moves, and try to outsmart your opponent! Matchups are shown below.</h4>
      <img className="about--page--image" src={rps} />
      <div className="about--page--info">
        <h2 className="about--page--info--title">How To Queue</h2>
        <h4>Create an account, and then click the play button. You will be matched with another player as soon as someone else queues.</h4>
        <h4>The game is best out of 5 with 15 seconds per round. First to win 3 rounds wins the game.</h4>
      </div>
      <div className="about--page--info">
        <h2 className="about--page--info--title">How Ranking Works</h2>
        <h4>Your elo indicates your skill level. The default elo is 1000.</h4>
      </div>
      <Link to="/">
        <div className="about--page--backBtn">✂️</div>
      </Link>
    </div>
  )
}
