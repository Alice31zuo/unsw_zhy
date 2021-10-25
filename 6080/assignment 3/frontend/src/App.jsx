import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from 'react-router-dom';
import GameStore from './tools/storeGame';
import { Breadcrumbs } from '@material-ui/core';
import Logout from './components/logout'
import Dashboard from './pages/dashboard.jsx'
import EditQuestionPage from './pages/editQuestion'
import EditGame from './pages/editGame'
import HomePage from './pages/homePage'
import Login from './pages/logIn'
import Register from './pages/register'
import CreateQuestionPage from './pages/createQuestion'
import JoinPage from './pages/joinPage'
import PlayPage from './pages/playPage'
import Result from './pages/result'

import HomeIcon from '@material-ui/icons/Home';
import VideogameAssetOutlinedIcon from '@material-ui/icons/VideogameAssetOutlined';
import ExitToAppOutlinedIcon from '@material-ui/icons/ExitToAppOutlined';
import './css/bar.css'

function App () {
  return (
    <GameStore>
      <Router>
        <Breadcrumbs aria-label="breadcrumb" bgcolor="secondary.main" className = 'barcontainer'>
        <div>
          <Link color="inherit" to = "/">
          <HomeIcon />
            Home
          </Link>
          <Link color="inherit" to = "/dashboard">
            <VideogameAssetOutlinedIcon />
            Dashboard
          </Link>
          <Link color="inherit" href="/">
            <ExitToAppOutlinedIcon />
            <Logout />
          </Link>
        </div>
        </Breadcrumbs>
        <Switch>
          <Route exact path="/"><HomePage /></Route>
          <Route exact path ='/logIn'><Login /></Route>
          <Route exact path ='/register'><Register /></Route>
          <Route exact path='/dashboard'><Dashboard /></Route>
          <Route exact path='/editgame/:gameid'><EditGame /></Route>
          <Route exact path='/editquestion/:gameid/:questionid'><EditQuestionPage /></Route>
          <Route exact path='/createquestion/:gameid/:questionid'><CreateQuestionPage /></Route>
          <Route exact path='/join/:gameid/:code'><JoinPage /></Route>
          <Route path='/play/:gameid/:sessionid/:playerid'><PlayPage /></Route>
          {/* when use exact path , can not go to the play page */}
          <Route path='/result'><Result /></Route>
        </Switch>
      </Router>
    </GameStore>
  );
}

export default App;
