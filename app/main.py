from fastapi import FastAPI
#from app.routes import api
import routes.user as Useroutes

app = FastAPI()


#app.include_router(api.router, prefix='/api/v1')
app.include_router(Useroutes.router, prefix='/api')