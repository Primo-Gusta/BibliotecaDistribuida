# 📚 Biblioteca Virtual - Aplicação Web Distribuída

## 📖 Descrição do Projeto

Esta aplicação é uma plataforma de **biblioteca virtual** composta por três principais componentes:

- **Frontend**: Interface web responsiva desenvolvida com HTML e CSS para cadastro e consulta de livros.
- **Backend**: API RESTful desenvolvida com Python e Flask, responsável pelo gerenciamento dos dados da biblioteca.
- **Banco de Dados**: Sistema de persistência de dados usando PostgreSQL.

Todos os componentes são conteinerizados com **Docker** e orquestrados com **Docker Compose**.

---

## 🧱 Arquitetura da Aplicação

- **Frontend (HTML/CSS)**  
  Interface de usuário para cadastro e visualização dos livros.

- **Backend (Python/Flask)**  
  API RESTful que gerencia o cadastro e a consulta de livros.

- **Banco de Dados (PostgreSQL)**  
  Sistema de armazenamento e persistência das informações da biblioteca.

---

## 🌐 Conceitos de Sistemas Distribuídos Aplicados

- **Comunicação**: Os serviços se comunicam via requisições HTTP RESTful entre contêineres.
- **Transparência**:
  - **De acesso**: O usuário interage apenas com o frontend, sem visibilidade da API.
  - **De localização**: Os serviços não precisam conhecer a localização física dos dados.
- **Concorrência**: Suporte a múltiplos acessos simultâneos.
- **Independência**: Cada componente pode ser atualizado de forma independente.
- **Tolerância a Falhas**: Contêineres permitem reinício rápido e isolamento de falhas.
- **Escalabilidade**: Possibilidade de escalar frontend e backend separadamente.

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11  
- Flask  
- SQLAlchemy  
- PostgreSQL  
- HTML5, CSS3  
- Docker  
- Docker Compose  

---

## ▶️ Como Executar com Docker Compose

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   ```

2. Acesse a pasta do projeto:

   ```bash
   cd nome-do-repositorio
   ```

3. Execute o comando para construir e iniciar os serviços:

   ```bash
   docker compose up --build
   ```

4. Acesse a aplicação no navegador:

   ```
   http://localhost:8080
   ```

---

## 📡 Exemplos de Requisições à API

### 📚 Cadastrar um livro

- **Método**: `POST`  
- **URL**: `http://localhost:5000/livros`  
- **Corpo da Requisição**:

```json
{
  "titulo": "1984",
  "autor": "George Orwell",
  "foto": "1984.jpg"
}
```

---

### 🔍 Consultar livros

- **Método**: `GET`  
- **URL**: `http://localhost:5000/livros`

---

## 🧩 Justificativa Arquitetural

A escolha por uma arquitetura baseada em **microserviços** proporciona:

- **Modularidade** e **facilidade de manutenção**
- Componentes evoluindo **de forma independente**
- Comunicação padronizada com **APIs RESTful**
- **Portabilidade** e **isolamento** via Docker