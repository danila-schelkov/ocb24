import uvicorn


def main():
    uvicorn.run("api._app:app")


if __name__ == "__main__":
    main()
