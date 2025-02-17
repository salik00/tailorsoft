from fastapi import FastAPI
from router import auth,user,order,search
import models
from database import engine
from config import settings 

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(order.router)
app.include_router(search.router)