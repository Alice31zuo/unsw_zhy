import React from 'react';
import { useHistory } from 'react-router-dom';
import API from '../tools/api';
import Button from '@material-ui/core/Button';

const Logout = () => {
  const history = useHistory()
  const api = new API('http://localhost:5005')
  const LogoutSubmit = (e) => {
    e.preventDefault();
    if (window.localStorage.getItem('token')) {
      // may directly click the submit
      const options = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + window.localStorage.getItem('token'),
        },
      }
      api.post('admin/auth/logout', options)
        .then(() => {
          window.localStorage.removeItem('token')
          history.push('/')
        })
    } else {
      history.push('/')
    }
  }
  return (
    <Button onClick = { (e) => { LogoutSubmit(e) } }>logout</Button>
  )
}
export default Logout;
