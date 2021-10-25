import React, { useEffect, useContext } from 'react'
import { useHistory } from 'react-router-dom';
import { StoreContext } from '../tools/storeGame'
import API from '../tools/api'
import PropTypes from 'prop-types';

import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

import EditIcon from '@material-ui/icons/Edit';
import DeleteForeverOutlinedIcon from '@material-ui/icons/DeleteForeverOutlined';

import Tooltip from '@material-ui/core/Tooltip';

import '../css/questionCard.css'

const QuestionCard = ({ gameid, questionID, content, time }) => {
  // console.log(questionID)
  // this is use to show basic question information
  const context = useContext(StoreContext)
  const { singleGame: [singleGame, setsingleGame] } = context
  const { curQuestions: [, setcurQuestions] } = context
  const history = useHistory()
  let Thisquesiton = []
  const api = new API('http://localhost:5005')
  const options = {
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + window.localStorage.getItem('token'),
    },
  }
  useEffect(() => {
    api.get(`admin/quiz/${gameid}`, options)
      .then((result) => {
        if (result) {
          setsingleGame(result)
          if (singleGame.questions) {
            Thisquesiton = singleGame.questions.find((question) => (question.idInfo === questionID))
            setcurQuestions(Thisquesiton)
          }
        }
      })
  }, [gameid])
  // get the quesiton information first
  const editQuestion = (e) => {
    e.preventDefault();
    history.push(`/editquestion/${gameid}/${questionID}`)
  }

  const deleteQuestion = async (e) => {
    // delete the quesiton = updata the game
    e.preventDefault();
    const updateQuestion = singleGame.questions.filter((question) => (question.idInfo !== questionID))
    const optionsSub = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + window.localStorage.getItem('token'),
      },
      body: JSON.stringify({
        questions: updateQuestion,
        name: singleGame.name,
        thumbnail: singleGame.thumbnail,
      })
    }
    api.put(`admin/quiz/${gameid}`, optionsSub)
      .then(() => {
        api.get(`admin/quiz/${gameid}`, options)
          .then((result) => {
            if (result) {
              setsingleGame(result)
              alert('delete success')
            }
          })
      })
  }

  return (
    <div>
      <Card className = 'questionCardcontainer' variant="outlined">
        <CardContent className = 'questionCardmain'>
          <Typography color="textSecondary" gutterBottom>
            question content : { content }
          </Typography>
          <Typography variant="body2" component="p">
            <br />
            time (s): { time }
          </Typography>
        </CardContent>
        <CardActions className = 'questionCardbuttonmain'>
          {/* <Button size="small">Learn More</Button> */}
          <Tooltip title="edit the question">
            <Button onClick = { (e) => { editQuestion(e) } }><EditIcon/></Button>
          </Tooltip>
          <Tooltip title="delete the question">
            <Button onClick = { (e) => { deleteQuestion(e) } }><DeleteForeverOutlinedIcon /></Button>
          </Tooltip>
        </CardActions>
      </Card>
    </div>
  )
}

QuestionCard.propTypes = {
  gameid: PropTypes.any.isRequired,
  questionID: PropTypes.any.isRequired,
  content: PropTypes.string.isRequired,
  time: PropTypes.string.isRequired,
};

export default QuestionCard;
