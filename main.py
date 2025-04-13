import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.main_router import api_routers
from src.settings import lifespan

app = FastAPI(
    title='This service for manage users',
    debug=False,
    version="0.1",
        contact={
        "name": "Sultan Kurbanov",
        "email": "sultan_kurbanov00@gmail.com",
    },
    lifespan=lifespan
    
)
origins = [
    "http://localhost:3000/",
    "http://localhost:80/",
    "http://localhost:8080/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["*"],

)
app.include_router(router=api_routers)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
