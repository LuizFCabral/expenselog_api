from fastapi import FastAPI

from expenselog_api.routers import auth, users

app = FastAPI(tittle='Expense Log API', version='1.0.0')

app.include_router(auth.router) 
app.include_router(users.router) 

@app.get('/')
def home():
    return {'message': 'Welcome to the Expense Log API'}
