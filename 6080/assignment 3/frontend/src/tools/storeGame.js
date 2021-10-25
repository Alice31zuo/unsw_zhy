import { React, createContext, useState } from 'react';
import PropTypes from 'prop-types';

export const StoreContext = createContext(null);

const GameStore = ({ children }) => {
  const [games, setGames] = useState([]);
  const [singleGame, setsingleGame] = useState({});
  const [curQuestions, setcurQuestions] = useState({});

  const store = {
    games: [games, setGames],
    singleGame: [singleGame, setsingleGame],
    curQuestions: [curQuestions, setcurQuestions],
  };

  return <StoreContext.Provider value={store}>{children}</StoreContext.Provider>;
};

export default GameStore;

GameStore.propTypes = {
  children: PropTypes.element.isRequired,
};
