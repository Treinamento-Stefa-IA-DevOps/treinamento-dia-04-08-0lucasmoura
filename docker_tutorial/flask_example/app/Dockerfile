# imagem base
FROM python:3.8-slim

# copia tudo dentro do contexto para o diretorio /app dentro do container
COPY . /app

# seta o /app como diretorio base
WORKDIR /app

# instala as dependencias do python
RUN pip install flask

# requerimento para rodar o flask run
ENV FLASK_APP=flask_app.py

# comando rodado ao iniciar o container
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
