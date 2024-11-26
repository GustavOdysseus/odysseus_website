import React from 'react';
import SpaceScene from './scenes/SpaceScene';
import './styles/styles.css';

const App: React.FC = () => {
  return (
    <div className="App w-full h-screen bg-black overflow-hidden">
      <SpaceScene />
    </div>
  );
};

export default App;
