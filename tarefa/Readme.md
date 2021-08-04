## Descrição do exercicio
Um colega de trabalho mudou de emprego e te deixou uma API para terminar, de acordo com ele já esta tudo pronto
só falta testar e subir, e todas as informações adicionais estão nesse manual.

#### Objetivos
* Confirmar que a API esta funcionando
* Testar a API
* Testar o Dockerfile

## API para predição de sobrevivencia do Titanic

#### Introdução

A segunte API serve para predizer se o usuario sobreviveria ao acidente do Titanic ou não.

#### Variaveis do modelo

O modelo foi treinado com as seguintes variaveis 

```json
{
	"Sex": "int",
	"Age": "float",	
	"Lifeboat": "int",	
	"Pclass": "int"	
}
```

* Sexo 0 é masculino sexo 1 é feminino
* Idade em forma fracionaria
* Numero do salva barco vidas que a pessoa pegou
* Classe no navio representado por um inteiro, onde 1 é primeira classe e 3 é classe economica

#### Resposta

A respsota da API deve ser a seguinte:

```json
{
	"survived": "bool",
	"status": "int",	
	"message": "string",	
}
```
* Survived é um booleano (true | false) para dizer se a pessoa sobreviveu ou não
* Status code da resposta HTTP
* Campo para mensagem extra para o usuário
