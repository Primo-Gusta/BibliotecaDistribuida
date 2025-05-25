import React, { useEffect, useState } from 'react';
import LivroForm from './components/LivroForm';
import LivroList from './components/LivroList';

function App() {
  const [livros, setLivros] = useState([]);

  const carregarLivros = async () => {
    const res = await fetch('http://localhost:5000/livros');
    const data = await res.json();
    setLivros(data);
  };

  useEffect(() => {
    carregarLivros();
  }, []);

  return (
    <div className="container">
      <h1>Biblioteca Virtual</h1>
      <LivroForm onLivroAdicionado={carregarLivros} />
      <LivroList livros={livros} />
    </div>
  );
}

export default App;
