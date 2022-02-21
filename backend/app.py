from fastapi import FastAPI

def create_app():
    pass


#app = create_app()
app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World!'}
