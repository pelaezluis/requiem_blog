from fastapi import FastAPI
from app.routes import api

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Server is running'}

app.include_router(api.router, prefix='/api/v1')