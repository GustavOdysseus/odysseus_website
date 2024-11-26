import React from 'react';
import { Provider } from 'jotai';
import SpaceScene from './scenes/SpaceScene';
import './styles/styles.css';

function App() {
  return (
    <Provider>
      <div className="App w-full h-screen bg-black">
        <SpaceScene />
      </div>
    </Provider>
  );
}

export default App;
