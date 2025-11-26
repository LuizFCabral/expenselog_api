from fastapi import FastAPI

app = FastAPI(tittle='Expense Log API', version='1.0.0')


@app.get('/')
def home():
    return {'message': 'Welcome to the Expense Log API'}
