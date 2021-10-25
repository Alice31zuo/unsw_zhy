import React, { useState } from 'react'
import { useHistory } from 'react-router-dom';
import API from '../tools/api'
import '../css/register.css'
import Button from '@material-ui/core/Button';
import Input from '@material-ui/core/Input';

const Register = () => {
  const [userEmail, setuserEmail] = useState('')
  const [userPassWord, setuserPassWord] = useState('')
  const [userName, setuserName] = useState('')
  const history = useHistory()
  const api = new API('http://localhost:5005')
  // these func to change value
  const EmailInsert = (e) => {
    setuserEmail(e.target.value)
  }
  const PassWordInsert = (e) => {
    setuserPassWord(e.target.value)
  }
  const UserNameInsert = (e) => {
    setuserName(e.target.value)
  }
  const RegisterSubmit = () => {
    if (userEmail && userPassWord && userName) {
      // insure has insert the input
      const options = {
        headers: {
          accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: userEmail,
          password: userPassWord,
          name: userName,
        }),
      }
      console.log(options)
      api.post('admin/auth/register', options)
        .then((result) => {
          if (result === undefined) {
            // this is to avoid the email has already use
            alert('this email has already register')
          } else {
            window.localStorage.setItem('token', result.token)
            history.push('./dashboard')
          }
        })
    } else {
      alert('please insert full information')
    }
  }
  return (
    <div className ='registerContainer'>
      <div className = 'registerinput'>
        <div className = 'registerinputelement'>
          <div className = 'registerwordelement'><p>Email</p></div>
          <div className = 'registerinputareaelement'>
            <Input name = 'emailinput' className = 'registerInputtextfied' placeholder = 'please insert user email' defaultValue = { userEmail } onChange = { (e) => { EmailInsert(e) } } />
          </div>
        </div>
        <div className = 'registerinputelement'>
          <div className = 'registerwordelement'><p>Password</p></div>
          <div className = 'registerinputareaelement'>
            <Input name = 'passwordinput' type = 'password' className = 'registerInputtextfied' placeholder = 'please insert password' defaultValue = { userPassWord } onChange = { (e) => { PassWordInsert(e) } } />
          </div>
        </div>
        <div className = 'registerinputelement'>
          <div className = 'registerwordelement'><p>Name</p></div>
          <div className = 'registerinputareaelement'>
            <Input name = 'usernameinput' className = 'registerInputtextfied' placeholder = 'please insert user name' defaultValue = { userName } onChange = { (e) => { UserNameInsert(e) } } />
          </div>
        </div>
        <div className = 'registerinputelement'>
          <Button name = 'signinsubmit' variant="contained" color="primary" onClick = { () => { RegisterSubmit() } }>submit</Button>
        </div>
      </div>
    </div>
  )
}

export default Register;
