import React from 'react'

const buttonNEXT = ({ setstage }) => {
  // need show result first
  const nextQuestion = () => {
    setstage('result')
  }
  return (
    <div>
      <button onClick = { () => { nextQuestion() } }>next quesiton</button>
    </div>
  )
}

export default buttonNEXT;
