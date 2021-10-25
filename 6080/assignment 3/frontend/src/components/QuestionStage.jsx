import React, { useContext } from 'react'
import { StoreContext } from '../tools/storeGame'
import TimeCount from './timeCount';
import PropTypes from 'prop-types';

const QuestionStage = ({ playerID, setStage }) => {
  const context = useContext(StoreContext);
  const { curQuestions: [curQuestions] } = context
  // when time up ,go to the stage of result
  // but upload the answer wrong
  return (
  <div>
    < TimeCount
      nextstage = { 'result' }
      setStage = { setStage }
      playerId = { playerID }
      remainingTime = { curQuestions.timeInfo }
    />
  </div>
  )
}

QuestionStage.propTypes = {
  playerID: PropTypes.string.isRequired,
  setStage: PropTypes.func.isRequired,
};

export default QuestionStage;
