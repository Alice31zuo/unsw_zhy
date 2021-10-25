import React, { useContext } from 'react'
import API from '../tools/api'
import { StoreContext } from '../tools/storeGame'
import PropTypes from 'prop-types';
import '../css/start.css'
import Button from '@material-ui/core/Button';
import hello from '../img/hello.jpg'

const StartStage = ({ setstage, sessionId, gameID }) => {
  const api = new API('http://localhost:5005')
  const context = useContext(StoreContext);
  const { curQuestions: [, setcurQuestions] } = context
  const options = {
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + window.localStorage.getItem('token'),
    },
  }
  const startSubmit = async (e) => {
    e.preventDefault();
    const results = await api.get(`admin/session/${sessionId}/status`, options)
    console.log(results.results)
    if (results.results.position === -1) {
      // change the state to start and get the quesiton
      setcurQuestions(results.results.questions[0]);
      console.log(results.results.questions[0])
      await api.post(`admin/quiz/${gameID}/advance`, options);
      setstage('question')
    } else {
      setstage('question')
    }
  }

  return (
    <div className = 'startpagemian'>
      <div className = 'startpagecontainer'>
        <div className = 'startpagecontainerelement'>
          <h1 className = 'startpagecontainerword'>are you ready to start ?</h1>
        </div>
        <div>
          <img src = {hello} className = 'startpagecontainerimg'/>
        </div>
        <div className = 'startpagecontainerelement'>
          <Button variant="contained" color="secondary" className = 'startpagecontainerinput' onClick = { (e) => { startSubmit(e) } }>yes!</Button>
        </div>
      </div>
    </div>
  )
}

StartStage.propTypes = {
  setstage: PropTypes.any.isRequired,
  sessionId: PropTypes.string.isRequired,
  gameID: PropTypes.string.isRequired,
};

export default StartStage;
