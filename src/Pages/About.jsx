import React from 'react'
import "./About.css"
import rps from "../assets/rps15.png"
import { Link, useNavigate } from "react-router-dom"

export default function About() {
  return (
    <div className="about--page--container">
      <h1>How To Play</h1>
      <img className="about--page--image" src={rps} />
      <div className="about--page--info">
        <h2 className="about--page--info--title">How To Queue</h2>
        <h4>Click the play button then best out of 5/first to 3, players get 15 seconds to make a move, each move beats 7 and loses to 7</h4>
      </div>
      <div className="about--page--info">
        <h2 className="about--page--info--title">How Ranking Works</h2>
        <h4>Your elo</h4>
      </div>
      <Link to="/">
        <div className="about--page--backBtn">✂️</div>
      </Link>
    </div>
  )
}
