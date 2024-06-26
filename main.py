from fastapi import FastAPI
from .api import atletas
from fastapi_pagination import add_pagination

app = FastAPI()

app.include_router(atletas.router, prefix="/api")

add_pagination(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
