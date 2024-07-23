from app import get_app
from config import get_config

config = get_config()
app = get_app(config=config)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=config.app.FASTAPI_HOST, port=config.app.FASTAPI_PORT, reload=True)
