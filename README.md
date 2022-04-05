# Autenticação JWT com Python

Projeto baseado inicialmente na vídeo aula [Clean Architecture Python Extra 1 - Autenticação JWT](https://www.youtube.com/watch?v=ZwBB4LEPLBU&list=PLAgbpJQADBGJmTxeRZKWvdJAoJj8_x3si&index=14), mas utilizando o FastAPI para desenvolvimento da API, além de consulta a informações do usuário armazenadas em banco.

A aplicação pode ser iniciada com docker executando os seguintes comandos:

```bash
$ docker build -t auth:jwt .
```

```bash
$ docker run -d -p 8080:8080 --rm auth:jwt
```

A aplicação possui 3 rotas presentes no arquivo `src.routes.route.py` e a documentação pode ser acessada no `http://localhost:8080/redoc`.

As credenciais do usuário cadastrado no banco encontram-se no arquivo `.env` e para o consumo da rota `/secret-information` é necessário fornecer o token obtido na rota `/auth` e o uuid presente no banco para o usuário solicitante.
