# Trabalhando com flask e docker-compose

O flask é uma framework em python para desenvolvimento de APIs web, focado principalmente na construção de microsserviços!

Iremos utilizar o flask junto com o docker-compose para subir sua primeira aplicação funcional *dockerizada*. Siga os passos abaixo para obter sucesso:

## Instalando o compose

O compose é uma ferramenta Docker para definir e rodar multiplos containers com uma facilidade enorme! Recomendo inclusive o uso do compose até para quando você tiver apenas um container, pois ele resume todo aquele comando no seu CLI para um simples arquivo de definição `.yml`.

Para sua instalação você pode usar o pip, caso possua python instalado em sua maquina Linux, ou pegar os binários da fonte:

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Para mais informações, siga para a [página oficial de instalação do compose](https://docs.docker.com/compose/install/).

## Rodando sua primeira aplicação flask

Como esse é um tutorial simples, e o objetivo não é ensinar explicitamente o flask e/ou python, siga as instruções abaixo para rodar seu primeiro app:

Crie uma estrutura de diretório tal qual abaixo:

```tree
- flask_example
    +- app
        +- __init__.py
        +- flask_app.py
        +- Dockerfile
    +- docker-compose.yml
```  

Dentro do arquivo `flask_app.py` adicione:

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'
```

Agora para o seu `Dockerfile`:

```Dockerfile
FROM python:3.8-slim  # imagem base

COPY . /app  # copia tudo dentro do contexto para o diretorio /app dentro do container

WORKDIR /app  # seta o /app como diretorio base

RUN pip install -u flask  # instala as dependencias do python

ENV FLASK_APP=flask_app.py  # requerimento para rodar o flask run

CMD ["flask", "run", "--host=0.0.0.0", "--port:5000"]  # comando rodado ao iniciar o container
```

E seu `docker-compose.yml` fica definido como abaixo:

```yml
version: '3'

services:
  api:
    build:
      context: ./app
      dockerfile: Dockerfile
    ports:
      - 5000:5000  # espelha a porta 5000 da sua maquina para a 5000 do container
```

Para subir esse app, basta rodar o seguinte comando:

```sh
docker-compose up
```

Agore acesse seu navegador na pagina `http://localhost:5000` e você terá seu próprio Hello World para conquistar p mundo!

## Flask com postgres 😨  

Para rodar seu app flask que conversa com um banco de dados, no nosso caso o postgres, precisaremos fazer poucas alterações...

Primeiramente precisamos nos conectar ao database né.. Para isso vamos alerar nosso `flask_app.py`:

```python
from flask import Flask

import os  # vamos pegar nossas credenciais de conexão como variaveis de ambiente!!
import psycopg2  # lib que vai nos conectar ao postgres!

app = Flask(__name__)


@app.route('/')
def hello_world():
    with psycopg2.connect(f"dbname={os.getenv("DB_NAME")} user={"DB_USER"} password:{os.getenv:"DB_PASS"}") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM test;")
        rows = cur.fetchall()  # retorna o resultado como tuplas, onde cada item dentro da tupla [e o valor de uma coluna]
        message = ''
        for row in rows:
            message = message + row[1] # seleciona primeiro elemento da tupla retornada
    return message + " Direto de meu belo database!!"
```

Mas para conectar e pegar valores de dentro do meu banco de dados eu preciso primeiramente popula-lo.. Podemos fazer isso de tres formas:  

- Levantar o container, entrar nele e rodar cada comando sql na mão com o psql
- Fazer a população das tabelas de dentro do script python
- Carregar o comando no momento em que o database for criado utilizando o docker-entrypoint-initdb.d

Para esse tutorial eu escolhi a terceira forma! 😈  
Não porque é a mais dificil, mas porque é a mais correta em minha visão, pois separamos completamento a aplicação do banco de dados e ainda o fazemos de forma automatizada.

Para isso funcionar adicione o seguinte script sql a pasta `./app/db_entrypoint` como `sql_entry.sql`:

```sql
CREATE DATABASE my_db;

-- connect to the newly created database
\c my_db

CREATE TABLE hello_world (
    id SERIAL PRIMARY KEY,
    text VARCHAR(200) NOT NULL
);

INSERT INTO
    hello_world (text)
VALUES
    ('Hello,'), (' World'), ('!');
```

Agora sua estrutura de diretórios deverá estar assim:  

```tree
- flask_example
    +- app
        +- __init__.py
        +- flask_app.py
        +- Dockerfile
        +- db_entrypoint
            +- sql_entry.sql
    +- docker-compose.yml
```  

Para o Dockerfile, basta adicionar a nova dependencia `psycopg2`a linha do pip install dentro do Dockerfile e adicionar o novo `COPY` para o script sql no entrypoint. Simples né?

```Dockerfile
RUN pip install -u flask psycopg2 # instala as dependencias do python

COPY ./db_entrypoint/sql_entry.sql /docker-entrypoint-initdb.d/sql_entry.sql
```

E agora a parte interessante! O docker-compose:

```yml
version: '3'

services:
  api:
    build:
      context: ./app
      dockerfile: Dockerfile
    environment:
      DB_PASS: password123
      DB_USER: userino
    ports:
      - 5000:5000  # espelha a porta 5000 da sua maquina para a 5000 do container
    depends:
      - postgres # faz a api subir depois do db
    networks:
      - backend  # rede para o db e a api "conversarem"

  postgres:
    image: postgres # ele busca a imagem automaticamente do dockerhub
    environment:
      POSTGRES_PASSWORD: password123 # definição do password do banco
      POSTGRES_USER: userino # definição do user do banco
    networks:
      - backend  # rede para o db e a api "conversarem"

networks:
  backend:
    driver: bridge
```

Se tudo estiver correto basta rodar:

```sh
docker-compose up --build
```

***Lembre-se de colocar a flag build para forçar o rebuild das imagens pois agora temos bastante coisa nova!!***

## FIM

Então é isso, jovem padawan, você foi introduzido ao mundo do Docker e por tabela ainda aprendeu um pouco sobre API's. Para finalizar esse tutorial recomendo alguns materiais e cursos para complementar seu conhecimento. Além disso para prosseguirmos para o trabalho principal recomendo fazer o rust_example como próxima atividade!

### Recomendações de leitrua e estudo

<https://hub.docker.com/_/postgres>  
<https://flask.palletsprojects.com/en/1.1.x/>  
<https://docs.docker.com/compose/>  
<https://www.udemy.com/course/curso-docker/>
<https://www.fullstackpython.com/microservices.html>
