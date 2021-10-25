import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import API from '../tools/api';
import '../css/login.css'
import Button from '@material-ui/core/Button';
import Input from '@material-ui/core/Input';

const Login = () => {
  const [userEmail, setuserEmail] = useState('')
  const [userPassWord, setuserPassWord] = useState('')
  const history = useHistory()
  const api = new API('http://localhost:5005')
  const EmailInsert = (e) => {
    setuserEmail(e.target.value)
  }
  const PassWordInsert = (e) => {
    setuserPassWord(e.target.value)
  }
  const logInSubmit = () => {
    if (userEmail && userPassWord) {
      // need to insure insert all information
      const options = {
        headers: {
          accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: userEmail,
          password: userPassWord,
        }),
      }
      console.log(options)
      api.post('admin/auth/login', options)
        .then((result) => {
          console.log(result)
          if (result !== undefined) {
            window.localStorage.setItem('token', result.token)
            history.push('./dashboard')
          } else {
            history.push('/register')
            alert('please register first')
          }
        })
    } else {
      alert('please insert full information')
    }
    // when test ,may need change the Button to button ,same as input
  }
  return (
    <div className ='loginContainer'>
      <div className = 'loginimg'>
      </div>
      <div className = 'logininput'>
        <div className ='logininputelement'>
          <div className ='loginwordelement'>
            <p>Email</p>
          </div>
          <div className ='logininputareaelement'>
            <Input name = 'nameinput' type = 'text' className = 'loginInputtextfied' placeholder = 'please insert user email' defaultValue = {userEmail} onChange = { (e) => { EmailInsert(e) } } />
          </div>
        </div>
        <div className ='logininputelement'>
          <div className ='loginwordelement'>
            <p>Password</p>
          </div>
          <div className ='logininputareaelement'>
            <Input name = 'passwordinput' type = 'password' className = 'loginInputtextfied' placeholder = 'please insert password' defaultValue = {userPassWord} onChange = { (e) => { PassWordInsert(e) } } />
          </div>
        </div>
        <div>
          <Button name = 'signinsubmit' variant="contained" color="primary" onClick = {() => { logInSubmit() } }>submit</Button>
        </div>
      </div>
    </div>
  )
}

export default Login;
