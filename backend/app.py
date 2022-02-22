from fastapi import FastAPI

from backend.db.session import database
from backend.routers import individuals, places


def create_app():
    app = FastAPI()

    @app.on_event('startup')
    async def startup():
        await database.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await database.disconnect()

    app.include_router(individuals.router)
    app.include_router(places.router)

    return app


app = create_app()
