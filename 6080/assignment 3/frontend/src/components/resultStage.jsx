import React, { useEffect, useState, useContext } from 'react'
import { useHistory } from 'react-router-dom';
import { StoreContext } from '../tools/storeGame'
import API from '../tools/api'
import Modal from '@material-ui/core/Modal';
import TimeCountR from './timeCountR';
import { makeStyles, createStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';

function rand () {
  return Math.round(Math.random() * 20) - 10;
}

function getModalStyle () {
  const top = 50 + rand();
  const left = 50 + rand();

  return {
    top: `${top}%`,
    left: `${left}%`,
    transform: `translate(-${top}%, -${left}%)`,
  };
}

const useStyles = makeStyles(() =>
  createStyles({
    paper: {
      position: 'absolute',
      width: 400,
      border: '5px solid #000',
    },
  }),
);

const ResultStage = ({ gameID, sessionID, playerID, setStage }) => {
  // use to get and show the result
  const context = useContext(StoreContext);
  const { curQuestions: [curQuestions, setcurQuestions] } = context
  const history = useHistory()
  const [ReturnAnswer, setReturnAnswer] = useState('')
  const [open, setOpen] = useState(false);
  let nextQuestion = ''
  const classes = useStyles();

  const [modalStyle] = useState(getModalStyle);
  const api = new API('http://localhost:5005')
  const options = {
    headers: {
      'Content-Type': 'application/json',
    },
  }
  setReturnAnswer([0])
  useEffect(() => {
    api.get(`admin/session/${sessionID}/status`, options)
      .then((result) => {
        if (result.results.position + 1 < result.results.questions.length - 1) {
          // this means there still have quesitons
          nextQuestion = result.results.questions[result.results.position + 1]
          console.log(nextQuestion)
          api.post(`admin/quiz/${gameID}/advance`, options)
            .then(() => {
              setcurQuestions(nextQuestion)
              // then change the question to next
            })
        } else {
          // if not ,means need to end the game go back to the dash borad to see the result
          setOpen(open)
        }
      })
  })

  const close = () => {
    history.push('./dashboard')
    setOpen(false);
  }

  const body = (
    <div style={modalStyle} className={classes.paper}>
      <h2 id="simple-modal-title">you have finish all the question!</h2>
      <p id="simple-modal-description">
        please go to the dash borad to see the result
      </p>
      <button onClick = {() => { close() }}>close</button>
    </div>
  );

  const handleClose = () => {
    history.push('/dashboard')
    setOpen(false);
  };

  const findTrueAnswer = (id) => {
    // this function is use to find the ture anwer
    for (let i = 0; i < ReturnAnswer.length; i++) {
      if (id === ReturnAnswer[i]) {
        return true
      }
    }
    return false
  }
  return (
  // when time stop ,the answer will upload or click the next button
  // means go to the result stage show the right result like 5s then go to the middle stage to judge we can go to next question or end
  <div>
    <div>{curQuestions.content}</div>
    <div>
      <p>right answer</p>
      {curQuestions.answer.filter((everyAnswer) => (findTrueAnswer(everyAnswer.id))).map((answer, index) => (
        <div key = { index }>{answer.content}</div>
      ))}
    </div>
    < TimeCountR
      remainingTime = {3}
      nextstage = {'question'}
      setStage = {setStage}/>
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="simple-modal-title"
      aria-describedby="simple-modal-description"
    >
      {body}
    </Modal>
  </div>
  )
}

ResultStage.propTypes = {
  gameID: PropTypes.string.isRequired,
  sessionID: PropTypes.string.isRequired,
  playerID: PropTypes.string.isRequired,
  setStage: PropTypes.func.isRequired,
};

export default ResultStage;
