import React from 'react';
import { CountdownCircleTimer } from 'react-countdown-circle-timer';
import './styles.css';
import PropTypes from 'prop-types';

const TimeCountR = ({ remainingTime, nextstage, setStage }) => {
  // const timeInput = remainingTime
  const renderTime = ({ remainingTime }) => {
    if (Number(remainingTime) === 0) {
      setStage(nextstage)
      return <div className="timer">ok done!</div>;
    }
    return (
      <div className="timer">
        <div className="text">Remaining</div>
        <div className="value">{Number(remainingTime)}</div>
        <div className="text">seconds</div>
      </div>
    );
  };

  return (
    <div className="App">
      <div className="timer-wrapper">
        <CountdownCircleTimer
          isPlaying
          duration={Number(remainingTime)}
          colors={[['#004777', 0.33], ['#F7B801', 0.33], ['#A30000']]}
          onComplete={() => [true, 1000]}
        >
          {renderTime}
        </CountdownCircleTimer>
      </div>
    </div>
  )
}

TimeCountR.propTypes = {
  remainingTime: PropTypes.number.isRequired,
  nextstage: PropTypes.string.isRequired,
  setStage: PropTypes.func.isRequired,
};

export default TimeCountR;
