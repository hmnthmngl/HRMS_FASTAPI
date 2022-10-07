import models,models1
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers import users,auth
import uvicorn


models1.Base.metadata.create_all(bind=engine)
app = FastAPI(title='Inventory Management System')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(users.router)
app.include_router(auth.router)

@app.get('/')
def index():
    return 'Welcome to new World'

if __name__== "__main__":
    uvicorn.run(app,port=4001)