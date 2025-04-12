from fastapi import FastAPI
import uvicorn


app = FastAPI(
    title='This service for manage users',
    debug=False,
    version="0.1"
    
)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
