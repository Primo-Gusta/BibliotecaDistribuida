import React from 'react';

function LivroForm({ onLivroAdicionado }) {
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    await fetch('http://localhost:5000/livros', {
      method: 'POST',
      body: formData,
    });
    e.target.reset();
    onLivroAdicionado();
  };

  return (
    <form id="formLivro" className="formulario" onSubmit={handleSubmit}>
      <input type="text" name="titulo" placeholder="Título do livro" required />
      <input type="text" name="autor" placeholder="Autor do livro" required />
      <input type="file" name="foto" accept="image/*" />
      <button type="submit">Cadastrar Livro</button>
    </form>
  );
}

export default LivroForm;
