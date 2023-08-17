from fastapi import FastAPI
from .routes import api # esta es la que se usa para llamar las apis, está en routes/api.py
# import app.routes.user as Useroutes
from app.database.database import create_tables

#create_tables()



app = FastAPI()


#app.include_router(api.router, prefix='/api/v1')
app.include_router(api.api_router, prefix='/api')
