import React from 'react';
import SpaceGraphWrapper from './scenes/SpaceGraph'; // Atualizado para usar o novo caminho
import './styles/styles.css'; // Importa os estilos globais

function App() {
  return (
    <div className="App">
      <SpaceGraphWrapper /> {/* Usa o SpaceGraph com JotaiProvider */}
    </div>
  );
}

export default App;
