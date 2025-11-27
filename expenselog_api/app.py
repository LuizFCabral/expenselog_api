import asyncio
import sys

from fastapi import FastAPI

from expenselog_api.routers import accounts, auth, users

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(tittle='Expense Log API', version='1.0.0')

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(accounts.router)


@app.get('/')
def home():
    return {'message': 'Welcome to the Expense Log API'}
