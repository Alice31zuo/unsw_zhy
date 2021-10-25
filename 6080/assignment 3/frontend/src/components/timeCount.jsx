// import React from 'react';
import { CountdownCircleTimer } from 'react-countdown-circle-timer';
import './styles.css';
import API from '../tools/api'
import PropTypes from 'prop-types';

import { StoreContext } from '../tools/storeGame'
import React, { useContext } from 'react'
import '../css/questionStage.css'

import Button from '@material-ui/core/Button';

import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
// import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const TimeCount = ({ remainingTime, nextstage, playerId, setStage }) => {
  const context = useContext(StoreContext);
  const { curQuestions: [curQuestions] } = context

  let Answer = []
  let optionsSub = []
  // this is use to get the answer
  const changeAnswer = (id, e) => {
    if (curQuestions.type === 'single') {
      if (e.target.checked === true) {
        Answer = [id]
        console.log(Answer)
      } else {
        Answer = Answer.filter((e) => (e !== id))
      }
    } else {
      if (e.target.checked === true) {
        Answer.push(id)
        console.log(Answer)
      } else {
        Answer = Answer.filter((e) => (e !== id))
      }
    }
    optionsSub = {
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        answerIds: Answer,
      })
    }
  }

  const api = new API('http://localhost:5005')
  console.log(optionsSub)

  const nextbutton = (e) => {
    // firectly upload the answer and go to the result stage
    e.preventDefault();
    console.log('ok?')
    api.put(`play/${playerId}/answer`, optionsSub)
    // this have 400 problem
    setStage(nextstage)
  }
  const renderTime = ({ remainingTime }) => {
    if (Number(remainingTime) === 0) {
      // answerUpload()
      console.log(optionsSub)
      api.put(`play/${playerId}/answer`, optionsSub)
      setStage(nextstage)
      console.log('ok?')
      return <div className="timer">ok done!</div>;
    }
    return (
      <div className="timer">
        <div className="text">Remaining</div>
        <div className="value">{ Number(remainingTime) }</div>
        <div className="text">seconds</div>
      </div>
    );
  };

  return (
    <div className = 'questionstageontainer'>
      <div className = 'questionstageContentContainer'>
        <Card className = 'questionstageCardmain'>
        <CardActionArea className = 'questionstageCardaction'>
          { curQuestions.imgInfo === ''
            ? <div></div>
            : <CardMedia
            component="img"
            // height="300"
            image={curQuestions.imgInfo}
          />
          }
          { curQuestions.urlInfo === ''
            ? <div></div>
            : <CardMedia
            component="video"
            height="300"
            image={curQuestions.urlInfo}
          />
          }
        </CardActionArea>
        <CardActionArea className = 'questionstageCardaction'>
          <CardContent className = 'questionstageCardcontent'>
            <Typography gutterBottom variant="h5" component="h2">
              {curQuestions.contentInfo}
            </Typography>
            <div className="App">
              <div className="timer-wrapper">
                <CountdownCircleTimer
                  isPlaying
                  duration={Number(remainingTime)}
                  colors={[['#004777', 0.33], ['#F7B801', 0.33], ['#A30000']]}
                  onComplete={() => [true, 1000]}
                >
                  { renderTime }
                </CountdownCircleTimer>
              </div>
            </div>
          </CardContent>
        </CardActionArea>
        <CardActions className = 'questionstageCardcontentdown'>
          <div className = ''>
            <div className = ''>{ curQuestions.answer.map((answer, idx) => {
              return (<div key = { idx } className = 'questionstageCardinputarea'>
                <div className = 'questionstageCardanswer'>
                answer { idx + 1 } : { answer.answerContent }
                </div>
                <div>
                <input type = 'checkbox' onChange = { (e) => { changeAnswer(answer.id, e) } }/>
                </div>
              </div>)
            })}</div>
            <div className = ''><Button variant="contained" color="primary" onClick = { (e) => nextbutton(e) }>next question</Button></div>
          </div>

        </CardActions>
      </Card>
      </div>
    </div>
  )
}

TimeCount.propTypes = {
  remainingTime: PropTypes.any.isRequired,
  nextstage: PropTypes.string.isRequired,
  playerId: PropTypes.string.isRequired,
  setStage: PropTypes.func.isRequired,
};

export default TimeCount;
