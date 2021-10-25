import React, { useEffect, useState, useContext } from 'react'
import { useParams, useHistory } from 'react-router-dom';
import { StoreContext } from '../tools/storeGame'
import API from '../tools/api'
import imageToDataUrl from '../tools/helpers';
import '../css/editQuestion.css'

import Input from '@material-ui/core/Input';
import Select from '@material-ui/core/Select';
import Button from '@material-ui/core/Button';

const CreateQuestionPage = () => {
  const history = useHistory()
  const context = useContext(StoreContext);
  const gameID = useParams().gameid
  const quesitonID = useParams().questionid
  // console.log(quesitonID)
  const { singleGame: [singleGame, setsingleGame] } = context;
  const idInfo = quesitonID
  // console.log(idInfo)
  const [contentInfo, setcontentInfo] = useState('')
  const [imgInfo, setimgInfo] = useState('')
  const [urlInfo, seturlInfo] = useState('')
  const [timeInfo, settimeInfo] = useState(0)
  const [pointInfo, setpointInfo] = useState(0)
  const [typeInfo, settypeInfo] = useState('single')
  const defaultAnswer = []
  const [defaultAnswerValue, setdefaultAnswerValue] = useState(['', '', '', '', '', ''])
  const [defalutCheckVaule, setdefalutCheckVaule] = useState([0, 0, 0, 0, 0, 0])

  // console.log(contentInfo)

  const api = new API('http://localhost:5005')
  const options = {
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + window.localStorage.getItem('token'),
    },
  }
  // get the game information for update the question information from it
  useEffect(() => {
    api.get(`admin/quiz/${gameID}`, options)
      .then((result) => {
        if (result) {
          setsingleGame(result)
        }
      })
  }, [gameID])

  const changeAnswer = (index, e) => {
    let newAnser = []
    newAnser = [...defaultAnswerValue]
    // console.log(newAnser)
    newAnser[index] = e.target.value
    setdefaultAnswerValue(newAnser)
    // console.log(defaultAnswerValue)
  }
  // uppdate the check need consider the check type
  const changeCheck = (index, e) => {
    if (typeInfo === 'single') {
      if (e.target.checked === true) {
        let newCheck = []
        newCheck = [0, 0, 0, 0, 0, 0]
        newCheck[index] = 1
        setdefalutCheckVaule(newCheck)
      } else {
        let newCheck = []
        newCheck = [0, 0, 0, 0, 0, 0]
        setdefalutCheckVaule(newCheck)
      }
    } else {
      let newCheck = []
      newCheck = [...defalutCheckVaule]
      if (e.target.checked === true) {
        newCheck[index] = 1
        setdefalutCheckVaule(newCheck)
      } else {
        newCheck[index] = 0
        setdefalutCheckVaule(newCheck)
      }
    }
  }

  const createSubmit = async (e) => {
    e.preventDefault();
    // alert('?')
    if (defaultAnswerValue === ['', '', '', '', '', ''] || defalutCheckVaule === [0, 0, 0, 0, 0, 0]) {
      alert('please insert answer information')
    } else {
      for (let i = 0; i < 6; i++) {
        if (defaultAnswerValue[i] !== '') {
          defaultAnswer.push({ id: i + 1, answerContent: defaultAnswerValue[i], checked: defalutCheckVaule[i] })
        }
      }
      // setanswerInfo({ ...defaultAnswer })
      // console.log(answerInfo)
      // setquestion({
      //   id: idInfo,
      //   content: contentInfo,
      //   img: imgInfo,
      //   video: urlInfo,
      //   timelimit: timeInfo,
      //   point: pointInfo,
      //   type: typeInfo,
      //   answer: answerInfo,
      // })
      // setquestion({
      //   idInfo,
      //   contentInfo,
      //   imgInfo,
      //   urlInfo,
      //   timeInfo,
      //   pointInfo,
      //   typeInfo,
      //   answerInfo,
      // }) these all wrong
      const question = {
        idInfo,
        contentInfo,
        imgInfo,
        urlInfo,
        timeInfo,
        pointInfo,
        typeInfo,
      }
      question.answer = defaultAnswer
      console.log(question)
      const newGame = { ...singleGame };
      let newQuestions = []
      if (singleGame.questions.length === 0) {
        newQuestions = [question];
      } else {
        newQuestions = [...singleGame.questions, question];
      }

      console.log(newQuestions)
      newGame.questions = newQuestions;

      const optionsSub = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + window.localStorage.getItem('token'),
        },
        body: JSON.stringify({
          questions: newQuestions,
          name: singleGame.name,
          thumbnail: singleGame.thumbnail,
        })
      }
      api.put(`admin/quiz/${gameID}`, optionsSub)
        .then(() => {
          setsingleGame(newGame)
          history.goBack()
          alert('create success!')
          // when create success ,goback
        })
    }
  }

  return (
    <div className = 'editGameContainer'>
      <div className = 'editGameContentContainer'>
        <div className = 'editGameContentContainerContent'>
          <div className = 'editGameElementcontainer'>
            <div className = 'editGameElementword'>
              content :
            </div>
            <div className = 'editGameElementinput'>
              <Input className = 'editGameInputtextfied' onChange = { (e) => { setcontentInfo(e.target.value) } }/>
            </div>
          </div>
        </div>

      <div className = 'editGameContentContainerContent'>
        <div className = 'editGameElementcontainer'>
            <div className = 'editGameElementword'>
              img :
            </div>
            <div className = 'editGameElementinput'>
              <Input className = 'editGameInputtextfied' type="file" onChange = { (e) => { setimgInfo(imageToDataUrl(e.target.files[0])) } }/>
            </div>
        </div>
      </div>

      <div className = 'editGameContentContainerContent'>
        <div className = 'editGameElementcontainer'>
          <div className = 'editGameElementword'>
            video :
          </div>
          <div className = 'editGameElementinput'>
            <Input className = 'editGameInputtextfied' onChange = { (e) => { seturlInfo(e.target.value) } }/>
          </div>
        </div>
      </div>

      <div className = 'editGameContentContainerContent'>
        <div className = 'editGameElementcontainer'>
          <div className = 'editGameElementword'>
            time :
          </div>
          <div className = 'editGameElementinput'>
            <Input className = 'editGameInputtextfied' type = 'number' onChange = { (e) => { settimeInfo(e.target.value) } }/>
          </div>
        </div>
      </div>

      <div className = 'editGameContentContainerContent'>
        <div className = 'editGameElementcontainer'>
          <div className = 'editGameElementword'>
            point :
          </div>
          <div className = 'editGameElementinput'>
            <Input className = 'editGameInputtextfied' type = 'number' onChange = { (e) => { setpointInfo(e.target.value) } }/>
          </div>
        </div>
      </div>

      <div className = 'editGameContentContainerContent'>
        <div className = 'editGameElementcontainer'>
          <div className = 'editGameElementword'>
            type :
          </div>
          <div className = 'editGameElementinput'>
            <Select defaultValue = 'single' onChange = { (e) => { settypeInfo(e.target.value) } }>
              <option value= 'single'>single</option>
              <option value= 'multiple'>multiple</option>
            </Select>
          </div>
        </div>
      </div>

      <div className = 'editGameContentContainerContent'>
        {
          defaultAnswerValue.map((answer, index) => {
            return (
                <div key = { index } className = 'editGameElementcontainer'>
                  <div key = { index } className = 'editGameElementword'>
                    answer {index + 1}:
                  </div>
                  <div className = 'editGameElementinput'>
                    <Input className = 'editGameInputtextfied' value = {answer} onChange = {(e) => { changeAnswer(index, e) }}/>
                    <input type = 'checkbox' value = { defalutCheckVaule[index] === 0 ? '0' : '1' } onChange = {(e) => { changeCheck(index, e) }}/>
                  </div>
                </div>
            )
          })
        }
        <div className = 'editGameContentContainerContent'>
          <div className = 'editGameElementcontainer'>
            <div className = 'editGamebuttonfield'>
              <Button variant="contained" color="primary" onClick = {(e) => { createSubmit(e) }}>submit</Button>
            </div>
            <div className = 'editGamebuttonfield'>
              <Button variant="contained" color="secondary" onClick = {() => { history.goBack() }}>back</Button>
            </div>
          </div>
        </div>
        </div>
      </div>
    </div>
  )
}

export default CreateQuestionPage;
