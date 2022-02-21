from backend.db.models import *  # noqa: F401, WPS347, F403
from backend.db.session import Base, engine


def main():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    main()
