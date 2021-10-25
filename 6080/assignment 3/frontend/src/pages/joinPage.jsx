import React, { useState } from 'react'
import { useParams, useHistory } from 'react-router-dom';
import API from '../tools/api'
import '../css/joinPage.css'
import Button from '@material-ui/core/Button';
import Input from '@material-ui/core/Input';

const JoinPage = () => {
  // this is use to give a game name to join the game
  const api = new API('http://localhost:5005')
  console.log(useParams().code)
  const gameID = useParams().gameid;
  const sessionID = useParams().code;
  const [gameName, setgameName] = useState('')

  const history = useHistory()
  const changeName = (e) => {
    setgameName(e.target.value)
  }
  const submit = async (e) => {
    e.preventDefault();
    const optionsSub = {
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: gameName
      })
    }
    const result = await api.post(`play/join/${sessionID}`, optionsSub)
    console.log(result)
    if (result.playerId) {
      // console.log(`/play/${gameID}/${sessionID}/${result.playerId}`)
      history.push(`/play/${gameID}/${sessionID}/${result.playerId}`)
      // after submit the name ,direct fo play page
    }
  }
  return (
    <div className = 'joinpagemian'>
      <div className = 'joinpagecontainer'>
        <div className = 'joinpagecontainerelement'>
          <h2 className = 'joinpagecontainerword'>please insert your game name :</h2>
        </div>
        <div className = 'joinpagecontainerelement'>
          <Input className = 'joinpagecontainerinput' placeholder = 'insert your game name here' onChange= { (e) => { changeName(e) } }/>
        </div>
        <div className = 'joinpagecontainerelement'>
          <Button variant="contained" color="primary" onClick = { (e) => { submit(e) } }>submit and play</Button>
        </div>
      </div>
    </div>
  )
}

export default JoinPage;
