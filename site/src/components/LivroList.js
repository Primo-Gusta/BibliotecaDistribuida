import React from 'react';

function LivroList({ livros }) {
  return (
    <div className="livros">
      {livros.map((livro) => (
        <div className="livro" key={livro.id}>
          {livro.foto && <img src={`http://localhost:5000${livro.foto}`} alt={livro.titulo} />}
          <h3>{livro.titulo}</h3>
          <p>{livro.autor}</p>
        </div>
      ))}
    </div>
  );
}

export default LivroList;
