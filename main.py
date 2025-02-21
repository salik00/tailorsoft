from fastapi import FastAPI
from router import auth,user,order,search,filter
import models
from database import engine
import uvicorn
# from config import settings 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    # allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def main():
    return {"message": "hello world!!!"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(order.router)
app.include_router(search.router)
app.include_router(filter.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)