import uvicorn

from ._settings import settings


def main():
    uvicorn.run("api._app:app", host=settings.API_HOST, port=settings.API_PORT)


if __name__ == "__main__":
    main()
