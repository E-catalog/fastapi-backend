from fastapi import FastAPI

from backend.routers import individuals, places

def create_app():
    app = FastAPI()

    app.include_router(individuals.router)
    app.include_router(places.router)

    return app


app = create_app()
