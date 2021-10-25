import React, { useEffect, useState, useContext } from 'react'
import { useParams, useHistory } from 'react-router-dom';
import { StoreContext } from '../tools/storeGame'
import API from '../tools/api'
import imageToDataUrl from '../tools/helpers';
import QuestionCard from '../components/questionCard'
import '../css/editGame.css'
import Button from '@material-ui/core/Button';
import Input from '@material-ui/core/Input';

import AddIcon from '@material-ui/icons/Add';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';

const EditGame = () => {
  const history = useHistory()
  const gameID = useParams().gameid;
  const context = useContext(StoreContext);
  const { singleGame: [singleGame, setsingleGame] } = context;
  // console.log(singleGame)
  const [gameName, setgameName] = useState('')
  const [gameURL, setgameURL] = useState('')
  const api = new API('http://localhost:5005')
  const options = {
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + window.localStorage.getItem('token'),
    },
  }
  // this use to get the game information
  useEffect(() => {
    api.get(`admin/quiz/${gameID}`, options)
      .then((result) => {
        if (result) {
          setsingleGame(result)
          console.log(result)
          // alert('ok')
        }
      })
  }, [gameID, setsingleGame])

  // these functions use to update value

  const changeName = (e) => {
    setgameName(e.target.value)
  }

  const changeURL = async (e) => {
    const url = await imageToDataUrl(e.target.files[0])
    setgameURL(url)
  }

  const editSubmit = async (e) => {
    // this is submit the new inforamtion, only change name is not allowed
    e.preventDefault();
    // alert('change success')
    if (gameName && gameURL) {
      const optionsSub = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + window.localStorage.getItem('token'),
        },
        body: JSON.stringify({
          questions: singleGame.questions,
          name: gameName,
          thumbnail: gameURL,
        })
      }
      api.put(`admin/quiz/${gameID}`, optionsSub)
        .then((result) => {
          if (result) {
            // alert('change success')
            api.get(`admin/quiz/${gameID}`, options)
              .then((result) => {
                if (result) {
                  setsingleGame(result)
                  alert('edit success')
                  console.log(result)
                }
              })
          }
        })
    } else {
      alert('please insert full information')
    }
  }

  const newQuestion = () => {
    // use the length +1 as the index of question
    const questionINDEX = singleGame.questions.length + 1
    // console.log(questionINDEX)
    history.push(`/createquestion/${gameID}/${questionINDEX}`)
  }
  // console.log(singleGame.questions)
  // this should can add a neww quiz ,directly go to a new page? then there are two page edit and create
  return (
    <div className = 'editGameContainer'>
      <div className = 'editGameArea'>
        <div>
          <div className = 'editGameinputelement'>
            <Input className = 'editGameInputtextfied' placeholder = 'please insert new name' defaultValue = { singleGame.name } value = { gameName } onChange = { (e) => { changeName(e) } } />
          </div>
          <div className = 'editGameinputelement'>
            <Input className = 'editGameInputtextfied' type="file" onChange = { (e) => { changeURL(e) } } />
          </div>
          <div><Button variant="contained" color="primary" onClick = { (e) => { editSubmit(e) } }>submit</Button></div>
        </div>
      </div>
      <div className = 'quesitonCardArea'>
        <div>
          <Tooltip title="create new question!" aria-label="add">
            <Fab color="primary" aria-label="add" onClick = { () => { newQuestion() } }><AddIcon /></Fab>
          </Tooltip>
        </div>
        { JSON.stringify(singleGame) === JSON.stringify({})
          ? <div></div>
          : singleGame.questions.map((question, index) => (
            <div key = { index }>
              <QuestionCard
                gameid = {gameID}
                questionID = {question.idInfo}
                content = {question.contentInfo}
                time = {question.timeInfo}
                />
            </div>))}
      </div>
    </div>
  )
}

export default EditGame;
