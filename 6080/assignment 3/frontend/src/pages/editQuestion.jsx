import React, { useState, useContext } from 'react'
import { useParams, useHistory } from 'react-router-dom';
import { StoreContext } from '../tools/storeGame'
import API from '../tools/api'
import imageToDataUrl from '../tools/helpers';
import '../css/editQuestion.css'
import Input from '@material-ui/core/Input';
import Select from '@material-ui/core/Select';
import Button from '@material-ui/core/Button';

const EditQuestionPage = () => {
  const api = new API('http://localhost:5005')
  const history = useHistory()
  const context = useContext(StoreContext);
  const gameID = useParams().gameid
  const quesitonID = useParams().questionid
  const { singleGame: [singleGame, setsingleGame] } = context;
  const { curQuestions: [curQuestions, setcurQuestions] } = context;
  const [QuesitonAnswer, setQuesitonAnswer] = useState(curQuestions.answer)
  const answerLength = QuesitonAnswer.length
  // edit quesitons of games
  let NewAnswer = []
  NewAnswer = new Array(6).fill('')
  let NewCheck = []
  NewCheck = new Array(6).fill(0)
  for (let i = 0; i < 6; i++) {
    if (i < answerLength) {
      NewAnswer[i] = QuesitonAnswer[i].answerContent
      NewCheck[i] = QuesitonAnswer[i].checked
    } else {
      NewAnswer[i] = ''
      NewCheck[i] = 0
    }
  }
  // console.log(NewCheck)
  // these are functions to change values
  const changeItem = (indexName, e) => {
    const question = { ...curQuestions }
    question[indexName] = e.target.value
    setcurQuestions(question)
  }

  const changeImg = async (indexName, e) => {
    const question = { ...curQuestions }
    question[indexName] = await imageToDataUrl(e.target.files[0])
    console.log(await imageToDataUrl(e.target.files[0]))
    setcurQuestions(question)
  }

  const ChangeAnswer = (index, e) => {
    NewAnswer[index] = e.target.value
    console.log(NewAnswer)
  }

  const ChangeCheck = (index, e) => {
    if (curQuestions.type === 'single') {
      if (e.target.checked === true) {
        NewCheck = [0, 0, 0, 0, 0, 0]
        NewCheck[index] = 1
      } else {
        NewCheck = [0, 0, 0, 0, 0, 0]
      }
    } else {
      if (e.target.checked === true) {
        NewCheck[index] = 1
      } else {
        NewCheck[index] = 0
      }
    }
  }

  const updateSubmit = () => {
    if (NewAnswer === ['', '', '', '', '', ''] || NewCheck === [0, 0, 0, 0, 0, 0]) {
      alert('please insert right answer information')
    } else {
      const tempAnswer = []
      for (let i = 0; i < 6; i++) {
        if (NewAnswer[i] !== '') {
          tempAnswer.push({ id: i + 1, answerContent: NewAnswer[i], checked: NewCheck[i] })
        }
      }
      // update the answer as new answer
      setQuesitonAnswer(tempAnswer)
      // console.log(QuesitonAnswer)
      let updateGame = []
      updateGame = { ...singleGame }
      let updataquestions = []
      updataquestions = [...singleGame.questions]
      let updateIndex = 0
      updateIndex = updataquestions.findIndex((quesiton) => (quesiton.idInfo === quesitonID))
      console.log(updateIndex)
      let updataQuestion = {}
      updataQuestion = { ...curQuestions }
      updataQuestion.answer = tempAnswer
      updataquestions[updateIndex] = updataQuestion
      updateGame.questions = updataquestions
      // console.log(updateGame.questions)
      // setsingleGame(updateGame)
      const optionsSub = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + window.localStorage.getItem('token'),
        },
        body: JSON.stringify({
          questions: updateGame.questions,
          name: singleGame.name,
          thumbnail: singleGame.thumbnail,
        })
      }
      const options = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + window.localStorage.getItem('token'),
        },
      }
      api.put(`admin/quiz/${gameID}`, optionsSub)
        .then(() => {
          api.get(`admin/quiz/${gameID}`, options)
            .then((result) => {
              if (result) {
                setsingleGame(result)
                // after edit the quesiton ,need update the context content in the card
                // alert('edit success')
                console.log(result)
                history.goBack()
                alert('edit success')
              }
            })
        })
    }
  }

  return (
    <div className = 'editGameContainer'>
      <div className = 'editGameContentContainer'>
        <div className = 'editGameContentContainerContent'>
          <div className = 'editGameElementcontainer'>
            <div className = 'editGameElementword'>content : </div>
            <div className = 'editGameElementinput'>
            <Input className = 'editGameInputtextfied' defaultValue = { curQuestions.contentInfo } onChange = { (e) => { changeItem('contentInfo', e) } }/>
            </div>
          </div>
        </div>
        <div className = 'editGameContentContainerContent'>
          <div className = 'editGameElementcontainer'>
            <div className = 'editGameElementword'> img : </div>
            <div className = 'editGameElementinput'>
              <Input className = 'editGameInputtextfied' type="file" onChange = { (e) => { changeImg('imgInfo', e) } }/>
            </div>
          </div>
        </div>
        <div className = 'editGameContentContainerContent'>
          <div className = 'editGameElementcontainer'>
            <div className = 'editGameElementword'>video :  </div>
            <div className = 'editGameElementinput'>
              <Input className = 'editGameInputtextfied' defaultValue = { curQuestions.urlInfo } onChange = { (e) => { changeItem('urlInfo', e) } }/>
            </div>
          </div>
        </div>
        <div className = 'editGameContentContainerContent'>
          <div className = 'editGameElementcontainer'>
            <div className = 'editGameElementword'>
            time :
            </div>
            <div className = 'editGameElementinput'>
              <Input className = 'editGameInputtextfied' defaultValue = { curQuestions.timeInfo } onChange = { (e) => { changeItem('timeInfo', e) } }/>
            </div>
          </div>
        </div>
        <div className = 'editGameContentContainerContent'>
          <div className = 'editGameElementcontainer'>
            <div className = 'editGameElementword'>
              point :
            </div>
            <div className = 'editGameElementinput'>
              <Input className = 'editGameInputtextfied' defaultValue = { curQuestions.pointInfo } onChange = { (e) => { changeItem('pointInfo', e) } }/>
            </div>
          </div>
        </div>
        <div className = 'editGameContentContainerContent'>
        <div className = 'editGameElementcontainer'>
          <div className = 'editGameElementword'>
              type :
          </div>
          <div className = 'editGameElementinput'>
            <Select defaultValue = { curQuestions.typeInfo } onChange = { (e) => { changeItem('typeInfo', e) } }>
              <option value= 'single'>single</option>
              <option value= 'multiple'>multiple</option>
            </Select>
          </div>
        </div>
        </div>
        <div className = 'editGameContentContainerContent'>
          <div>
            {
              NewAnswer.map((answer, index) => {
                return (
                  <div key = {index} className = 'editGameElementcontainer'>
                    <div className = 'editGameElementword'> answer { index + 1 }:  </div>
                    <div className = 'editGameElementinput'>
                    <Input className = 'editGameInputtextfied' defaultValue = { answer } onChange = { (e) => { ChangeAnswer(index, e) } }/>
                    <input type = 'checkbox' value = { NewCheck[index] === 0 ? '0' : '1' } onChange = { (e) => { ChangeCheck(index, e) } }/>
                    </div>
                  </div>
                )
              })
            }
          </div>
            <div className = 'editGameContentContainerContent'>
              <div className = 'editGameElementcontainer'>
                <div className = 'editGamebuttonfield'>
                  <Button variant="contained" color="primary" onClick = { () => { updateSubmit() } }>submit</Button>
                </div>
                <div className = 'editGamebuttonfield'>
                  <Button variant="contained" color="secondary" onClick = { () => { history.goBack() } }>back</Button>
                </div>
              </div>
            </div>
        </div>
      </div>
    </div>
  )
}

export default EditQuestionPage;
