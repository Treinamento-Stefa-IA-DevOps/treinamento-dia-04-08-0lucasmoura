import pickle
from fastapi import FastAPI

app = FastAPI()
@app.post('/model')
## Coloque seu codigo na função abaixo
def titanic(Sex:int):
    with open('model/Titanic.pkl', 'rb') as fid: 
        titanic = pickle.load(fid)

@app.get('/model')
def get():
    return {'hello':'test'}
