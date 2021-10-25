import React, { useEffect, useState, useContext } from 'react'
import { useHistory } from 'react-router-dom';
import { StoreContext } from '../tools/storeGame'
import API from '../tools/api'
import Modal from '@material-ui/core/Modal';
import Gamecard from '../components/GameCard';
import '../css/dashboard.css'
import AddIcon from '@material-ui/icons/Add';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';
import Button from '@material-ui/core/Button';
import Input from '@material-ui/core/Input';

// this is directly use the code from material-ui web
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

const Dashboard = () => {
  const [modalStyle] = useState(getModalStyle);
  const [open, setOpen] = useState(false);
  const context = useContext(StoreContext)
  const { games: [games, setGames] } = context
  const [GameName, setGameName] = useState('')
  const api = new API('http://localhost:5005')
  const history = useHistory()
  const options = {
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + window.localStorage.getItem('token'),
    },
  }
  useEffect(() => {
    // get all the games first
    if (window.localStorage.getItem('token')) {
      api.get('admin/quiz', options)
        .then((results) => {
          if (results.quizzes) {
            // console.log(games)
            setGames(results.quizzes)
            // console.log(games)
          }
        })
    } else {
      // when user not log in
      history.push('/')
      alert('please log in first')
    }
  }, [setGames])

  const handleClose = () => {
    setOpen(false);
  };

  const changeName = (e) => {
    setGameName(e.target.value)
  }

  const newGameCreate = async () => {
    // only need a name so the name can not empty
    if (GameName !== '') {
      const optionsSub = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + window.localStorage.getItem('token'),
        },
        body: JSON.stringify({
          name: GameName,
        })
      }
      api.post('admin/quiz/new', optionsSub)
        .then(() => {
          alert('create success !')
          setOpen(false);
          api.get('admin/quiz', options)
            .then((results) => {
              if (results.quizzes) {
                // console.log(games)
                setGames(results.quizzes)
                // console.log(games)
              }
            })
        })
    } else {
      alert('please insert right name')
    }
  }

  const body = (
    // <div style={modalStyle} className={classes.paper}>
    <div style={modalStyle} className='dashboardPOpUp'>
      <div className='dashboardPOpUpelement'>
      <h3 id="simple-modal-title">please insert the new game name!</h3>
      </div>
      <div className='dashboardPOpUpelement'>
      <Input name ='dashboardPOpUpinput' className = 'dashboardPOpUpinput' placeholder ='please insert the game name' onChange = {(e) => { changeName(e) }}/>
      </div>
      <Button name ='dashboardPOpUpbutton' variant="outlined" color="primary" onClick = {() => { newGameCreate() }}>confirm</Button>
    </div>
  );

  return (
    <div className = 'dashboardContainer'>
      <div className = 'dashboardGameArea' >
        <div className ='dashboardGameButtonArea'>
        <Tooltip title="Add a new game!" aria-label="add">
          <Fab name = 'fabcreate' color="primary" aria-label="add" onClick = { () => { setOpen(true) } }><AddIcon /></Fab>
        </Tooltip>
        </div>
        <div className = 'dashboardGameCardArea'>
          { games.map((game, index) => {
            return (
              <div key = {index}>
                <Gamecard
                id = {game.id}
                name = {game.name}
                thumbnail = {game.thumbnail}
                active = {game.active}
              />
              </div>
            )
          })}
        </div>
      </div>
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

export default Dashboard;
