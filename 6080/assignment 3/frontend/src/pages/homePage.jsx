import React from 'react'
import { useHistory } from 'react-router-dom';
import '../css/home.css'
import Button from '@material-ui/core/Button';

const HomePage = () => {
  // home page enable user to choose login or register
  const history = useHistory()
  return (
    <div className = 'mainpage'>
      <div className ='homeButtondiv'>
        <div>
          <h1 className = 'homeword'>welcome !</h1>
        </div>
        <div className = 'homebuttonarea'>
          <div>
              <Button variant="outlined" color="primary" name = 'logInButton' className = 'logInButton' onClick = { () => { history.push('/login') } }>Log in</Button>
          </div>
          <div>
              <Button variant="outlined" color="secondary" name = 'registerButton' className = 'registerButton' onClick = { () => { history.push('/register') } }>Register</Button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage;
