import uvicorn

from backend.app import app
from backend.config import config


def main():
    uvicorn.run(app, config.host, config.port)


if __name__ == '__main__':
    main()
