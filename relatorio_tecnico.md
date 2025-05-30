# Relatório Técnico: Aplicação Web Distribuída - Biblioteca Virtual

## 1. Introdução

Este relatório detalha a implementação de uma aplicação web distribuída para uma biblioteca virtual, desenvolvida como parte da disciplina de Sistemas Distribuídos. O objetivo principal foi aplicar conceitos práticos de arquitetura de microserviços, containerização com Docker e comunicação via APIs RESTful. A aplicação permite o cadastro e a consulta de livros através de uma interface web simples, interagindo com um backend que gerencia os dados persistidos em um banco de dados relacional.

## 2. Arquitetura da Aplicação

A arquitetura da aplicação foi projetada seguindo o padrão de microserviços, onde cada componente principal opera em um contêiner Docker isolado, facilitando o desenvolvimento, a implantação e a escalabilidade independentes.

Os componentes são:

*   **Frontend (Serviço `site`):** Uma interface de usuário web responsiva, desenvolvida com HTML e CSS. É responsável por permitir que os usuários visualizem a lista de livros e adicionem novos títulos. Este serviço é servido estaticamente por um contêiner Nginx, que atua como um servidor web leve e eficiente.
*   **Backend (Serviço `api`):** Uma API RESTful desenvolvida em Python utilizando o framework Flask. Este serviço expõe endpoints para operações CRUD (Create, Read, Update, Delete - embora apenas Create e Read tenham sido implementados neste escopo) sobre os livros. Ele lida com a lógica de negócios e a comunicação com o banco de dados. A comunicação entre o frontend e o backend ocorre via requisições HTTP para esta API.
*   **Banco de Dados (Serviço `db`):** Um sistema de gerenciamento de banco de dados PostgreSQL, responsável pela persistência dos dados dos livros (título e autor). Ele é executado em seu próprio contêiner e acessado exclusivamente pelo serviço de backend.
*   **Orquestração (Docker Compose):** A ferramenta Docker Compose é utilizada para definir e gerenciar a aplicação multi-contêiner. O arquivo `docker-compose.yml` descreve os serviços, redes e volumes necessários, permitindo que toda a aplicação seja iniciada e parada com comandos simples.

### Diagrama Simplificado da Arquitetura:

```
+-----------------+      HTTP Request      +-----------------+      SQL Query       +-----------------+
|  Usuário        |<--------------------->|  Frontend (Nginx)|<---------------->| Backend (Flask) |<--------------->| Banco de Dados  |
| (Navegador Web) |                      |  (Container)    |   (API RESTful)   |  (Container)    |   (PostgreSQL)  |  (Container)    |
+-----------------+                      +-----------------+                   +-----------------+                 +-----------------+
      |                                      | Port 3000                     | Port 5000                     | Port 5432
      +---------------------------------------> Docker Network <-------------------------------------+-----------------+
```

## 3. Associação com Conceitos de Sistemas Distribuídos

A arquitetura implementada exemplifica diversos conceitos fundamentais de Sistemas Distribuídos:

*   **Comunicação:** A comunicação entre o frontend e o backend é realizada através de uma API RESTful sobre HTTP. O backend, por sua vez, comunica-se com o banco de dados usando o protocolo padrão do PostgreSQL. Essa separação clara de interfaces de comunicação é essencial em sistemas distribuídos.
*   **Transparência:**
    *   **Transparência de Acesso:** O frontend acessa o backend através de uma URL definida (ex: `http://api:5000`), sem precisar conhecer a localização física ou o endereço IP específico do contêiner do backend. O Docker Compose e a rede interna do Docker gerenciam essa resolução de nomes.
    *   **Transparência de Localização:** Os serviços (frontend, backend, banco de dados) podem ser executados em diferentes máquinas (em um cenário de produção mais complexo) sem que os outros componentes precisem ser alterados, graças à abstração fornecida pelos contêineres e pela orquestração.
*   **Concorrência:** Tanto o servidor web Nginx (frontend) quanto o servidor Flask (backend) são capazes de lidar com múltiplas requisições de usuários simultaneamente. O banco de dados PostgreSQL também é projetado para gerenciar acessos concorrentes.
*   **Independência:** Cada componente (frontend, backend, banco de dados) é encapsulado em seu próprio contêiner Docker. Isso significa que eles podem ser desenvolvidos, atualizados, implantados e escalados de forma independente. Uma falha em um componente (ex: frontend) não necessariamente derruba os outros (backend ou banco de dados), embora a funcionalidade completa possa ser afetada.
*   **Tolerância a Falhas (Potencial):** Embora não configurado explicitamente neste exemplo simples, a arquitetura de contêineres facilita a implementação de tolerância a falhas. O Docker Compose permite definir políticas de reinicialização (`restart: always` ou `on-failure`) para que os contêineres sejam reiniciados automaticamente em caso de falha. Em ambientes de produção, orquestradores como Kubernetes ofereceriam mecanismos mais avançados.
*   **Escalabilidade (Potencial):** A separação em serviços permite escalar componentes individualmente. Se o backend se tornar um gargalo, seria possível aumentar o número de réplicas do contêiner `api` usando `docker compose up --scale api=3`, por exemplo (requer um balanceador de carga na frente, não incluído neste escopo básico).

## 4. Tecnologias Utilizadas

*   **Backend:** Python 3.11, Flask, Flask-SQLAlchemy (ORM), psycopg2-binary (Driver PostgreSQL), Flask-CORS (para permitir requisições do frontend).
*   **Frontend:** HTML5, CSS3, JavaScript (básico, para interagir com a API).
*   **Servidor Web (Frontend):** Nginx (imagem `nginx:alpine`).
*   **Banco de Dados:** PostgreSQL (imagem `postgres:15-alpine`).
*   **Containerização e Orquestração:** Docker, Docker Compose.

## 5. Instruções de Execução com Docker Compose

**Pré-requisitos:**

*   Docker instalado e em execução.
*   Docker Compose (geralmente incluído nas instalações mais recentes do Docker Desktop ou instalado como plugin `docker-compose-plugin`).
*   **Ambiente Compatível:** Conforme observado durante o desenvolvimento, a execução do Docker pode exigir privilégios específicos ou módulos de kernel (como `iptable_raw`) que podem não estar disponíveis em todos os ambientes (como o sandbox utilizado). Recomenda-se executar estes comandos em sua máquina local, uma máquina virtual (VM) ou uma instância na nuvem (como AWS EC2) com Docker devidamente configurado.

**Passos para Execução:**

1.  **Clone o Repositório ou Descompacte os Arquivos:** Certifique-se de ter a pasta do projeto (`BibliotecaDistribuida`) com todos os arquivos (`docker-compose.yml`, `api/`, `site/`, `db/`) em seu ambiente.
2.  **Navegue até o Diretório Raiz:** Abra um terminal ou prompt de comando e navegue até o diretório que contém o arquivo `docker-compose.yml`.
    ```bash
    cd caminho/para/BibliotecaDistribuida
    ```
3.  **Construa e Inicie os Contêineres:** Execute o seguinte comando. Ele irá construir as imagens (se ainda não existirem) e iniciar todos os serviços em background (`-d`).
    ```bash
    sudo docker compose up --build -d
    ```
    *Observação: O uso de `sudo` pode ser necessário dependendo da configuração do seu Docker.*

4.  **Verifique os Contêineres:** Você pode verificar se os contêineres estão em execução com:
    ```bash
    sudo docker compose ps
    ```
    Você deverá ver os três serviços (`biblioteca_api`, `biblioteca_site`, `biblioteca_db`) com o status `Up` ou `running`.

5.  **Acesse a Aplicação:**
    *   **Frontend:** Abra seu navegador e acesse `http://localhost:3000`.
    *   **Backend (API):** A API estará acessível em `http://localhost:5000`. Você pode testar os endpoints diretamente.

6.  **Para Parar a Aplicação:**
    ```bash
    sudo docker compose down
    ```
    Este comando para e remove os contêineres, redes e, opcionalmente, volumes (se especificado).

## 6. Exemplos de Uso da API (Testes)

Você pode usar ferramentas como `curl`, Postman ou Insomnia para interagir diretamente com a API RESTful no backend (`http://localhost:5000`).

*   **Listar todos os livros (GET /livros):**
    ```bash
    curl http://localhost:5000/livros
    ```
    *Resposta Esperada (Exemplo):* `{"livros":[{"autor":"Machado de Assis","id":1,"titulo":"Dom Casmurro"}]}` (se houver livros cadastrados)

*   **Adicionar um novo livro (POST /livros):**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d 
    ```
    *Resposta Esperada (Exemplo):* `{"message":"Livro adicionado com sucesso!"}`

*   **Consultar um livro específico (GET /livros/<id>):**
    ```bash
    curl http://localhost:5000/livros/1
    ```
    *Resposta Esperada (Exemplo):* `{"autor":"Machado de Assis","id":1,"titulo":"Dom Casmurro"}`

**Capturas de Tela:**

*Recomendação:* Ao executar a aplicação em seu ambiente, capture telas mostrando:
    1.  O frontend funcionando no navegador (`http://localhost:3000`).
    2.  Exemplos de requisições à API (usando Postman ou similar) e suas respostas.
    3.  O terminal mostrando os contêineres em execução (`docker compose ps`).

## 7. Conclusão

A implementação desta biblioteca virtual distribuída permitiu a aplicação prática de conceitos essenciais de sistemas distribuídos. A utilização de Docker e Docker Compose simplificou a configuração e o gerenciamento do ambiente, enquanto a arquitetura de microserviços com comunicação RESTful demonstrou a separação de responsabilidades e a independência dos componentes. Embora a validação completa tenha sido impedida por limitações do ambiente de desenvolvimento inicial, a estrutura está pronta para ser executada e testada em um ambiente Docker padrão, servindo como uma base sólida para projetos distribuídos mais complexos.
