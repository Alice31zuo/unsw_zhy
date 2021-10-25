import React, { useState } from 'react'
import { useParams } from 'react-router-dom';
import StartStage from '../components/startStage'
import QuestionStage from '../components/QuestionStage'
import ResultStage from '../components/resultStage'

const PlayPage = () => {
  // console.log('ok?')
  const gameID = useParams().gameid;
  const playerID = useParams().playerid;
  const sessionID = useParams().sessionid;
  const [stage, setstage] = useState('start')

  const stageChange = () => {
    // this has three stage first is start then is question and resutl switch
    switch (stage) {
      case 'question' :
        return (
          <QuestionStage
            playerID = {playerID}
            setStage = {setstage}
          />
        );
      case 'result' :
        return (
          <ResultStage
            gameID = {gameID}
            sessionID = {sessionID}
            playerID = {playerID}
            setStage = {setstage}
          />);
      default :
        return (
          <StartStage
            setstage = {setstage}
            sessionId = {sessionID}
            gameID = {gameID}
          />);
    }
  }

  return (
    <div>
      { stageChange() }
    </div>
  )
}

export default PlayPage;
