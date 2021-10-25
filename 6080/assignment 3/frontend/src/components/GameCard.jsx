import React, { useEffect, useState, useContext } from 'react'
import { useHistory } from 'react-router-dom';
import { StoreContext } from '../tools/storeGame'
import API from '../tools/api'
import Modal from '@material-ui/core/Modal';
// import { makeStyles, createStyles } from '@material-ui/core/styles';
import copy from 'copy-to-clipboard';
import PropTypes from 'prop-types';
import '../css/gamecard.css'
import hello from '../img/back.JPG'

import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

import EditIcon from '@material-ui/icons/Edit';
import DeleteForeverOutlinedIcon from '@material-ui/icons/DeleteForeverOutlined';
import PlayCircleFilledWhiteOutlinedIcon from '@material-ui/icons/PlayCircleFilledWhiteOutlined';
import StopRoundedIcon from '@material-ui/icons/StopRounded';

import Tooltip from '@material-ui/core/Tooltip';

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

const Gamecard = ({ id, name, thumbnail, active }) => {
  const context = useContext(StoreContext);
  const history = useHistory();
  const [stopOrResult, setstopOrResult] = useState(0)
  const [startOrStop, setstartOrStop] = useState(0)
  const [code, setcode] = useState('')

  // getModalStyle is not a pure function, we roll the style only on the first render
  const [modalStyle] = useState(getModalStyle);
  const [open, setOpen] = useState(false);
  const [url, seturl] = useState('');
  //
  const { games: [games, setGames] } = context;
  const { singleGame: [singleGame, setsingleGame] } = context;

  const [totalTime, settotalTime] = useState(0)
  const [quesitonNUM, setquesitonNUM] = useState(0)

  const api = new API('http://localhost:5005')
  const options = {
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + window.localStorage.getItem('token'),
    },
  }

  useEffect(() => {
    api.get(`admin/quiz/${id}`, options)
      .then((result) => {
        if (result) {
          setsingleGame(result)
          if (singleGame.questions !== undefined) {
            let total = 0
            for (let i = 0; i < result.questions.length; i += 1) {
              total += Number(result.questions[i].timeInfo)
            }
            settotalTime(total)
            setquesitonNUM(result.questions.length)
          } else {
            settotalTime(0)
          }
        }
      })
  }, [id])

  const editGame = () => {
    history.push(`./editgame/${id}`)
  }

  const deleteGame = async (e) => {
    e.preventDefault();
    api.delete(`admin/quiz/${id}`, options)
      .then(() => {
        const newGames = games.filter((game) => (game.id !== id))
        setGames(newGames)
        // or use the getdocumentbyid to change the display
      })
  }

  const startGame = async (e) => {
    e.preventDefault();
    if (quesitonNUM === 0) {
      alert('please create questions first')
    } else {
      if (startOrStop === 0) {
        setstopOrResult(0)
        setstartOrStop(1)
        await api.post(`admin/quiz/${id}/start`, options)
        const resultNew = await api.get(`admin/quiz/${id}`, options)
        console.log(resultNew)
        if (resultNew) {
          console.log(resultNew.active)
          console.log(resultNew)
          setcode(resultNew.active)
          setsingleGame(resultNew)
          console.log(id)
          console.log(resultNew.active)
          seturl(`http://localhost:3000/join/${id}/${resultNew.active}`)
          setOpen(true)
        }
      } else {
        alert('the game has already start ,please join the session')
        setOpen(true)
        // then pop up the modal
        setstopOrResult(0)
        setstartOrStop(1)
      }
    }
  }

  const stopGame = async (e) => {
    e.preventDefault();
    // use o and 1 judge the situation stop or result
    if (!startOrStop && stopOrResult === 0) {
      alert('the game did not start')
    } else {
      if (stopOrResult === 0) {
        const stop = window.confirm('are you sure to stop the game')
        if (stop) {
          setstopOrResult(1)
          setstartOrStop(0)
          api.post(`admin/quiz/${id}/end`, options)
            .then((result) => {
              if (result) {
                const results = window.confirm('are you want to get the result ?')
                if (results) {
                  setstopOrResult(0)
                  history.push(`./result/${code}`)
                }
              }
            })
        }
      } else {
        setstopOrResult(0)
        history.push(`./result/${code}`)
      }
    }
  }

  const handleClose = () => {
    setOpen(false);
  };

  const copythelink = () => {
    copy(url)
    setOpen(false);
  }
  const body = (
    <div style={modalStyle} className='gameCardPOpUp'>
      <h3 id="simple-modal-title">you can play game now!</h3>
      <h4 id="simple-modal-description">
        please join the game via this link
      </h4>
      <p id = 'url'>{url}</p>
      <Button variant="outlined" color="primary" onClick = {() => { copythelink() }}>copy the link</Button>
    </div>
  );

  return (
    <div className = 'gameCardcontainer'>
      <Card className='gameCardmain'>
      <CardActionArea>
        { thumbnail === null
          ? <CardMedia
            component = "img"
            height = "300"
            src = {hello}
            />
          : <CardMedia
            component = "img"
            height = "300"
            image = {thumbnail}
            />
        }
        <CardContent className='gameCardmain'>
          <Typography gutterBottom variant="h5" component="h2">
            Game Name :{name}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Time (s) : {totalTime}
            <br/>
            Question Number : {quesitonNUM}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions className='gameCardbuttonmain'>
      <Tooltip title="edit the game">
        <Button size="small" color="primary" onClick = { (e) => editGame(e) }>
          <EditIcon/>
        </Button>
        </Tooltip>
        <Tooltip title="delete the game">
        <Button size="small" color="primary" onClick = { (e) => deleteGame(e) }>
          <DeleteForeverOutlinedIcon />
        </Button>
        </Tooltip>
        <Tooltip title="start the game">
        <Button type="button" onClick={ (e) => startGame(e) }>
          <PlayCircleFilledWhiteOutlinedIcon />
        </Button>
        </Tooltip>
        <Tooltip title="stop the game or show result">
          <Button onClick = { (e) => stopGame(e) }>{ stopOrResult ? 'result' : <StopRoundedIcon /> }</Button>
        </Tooltip>
      </CardActions>
    </Card>
      <div>
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="simple-modal-title"
          aria-describedby="simple-modal-description"
        >
          {body}
        </Modal>
      </div>
    </div>
  )
}

Gamecard.propTypes = {
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
  thumbnail: PropTypes.any,
  active: PropTypes.any,
};

export default Gamecard;
