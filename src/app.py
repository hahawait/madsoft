import betterlogging
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from apps.memes.router import memes_router
from config import Config


def get_app(config: Config):
    betterlogging.basic_colorized_config(level=config.app.LOGGING_LEVEL)

    fastapi_params = dict(
        title=config.app.PROJECT_NAME,
        version=config.app.VERSION,
    )

    if config.app.is_production:
        app = FastAPI(
            **fastapi_params,
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
            debug=True,
        )
    else:
        app = FastAPI(**fastapi_params, debug=True)

    app.include_router(memes_router)

    register_tortoise(
        app,
        db_url=config.db.database_url,
        modules={"models": ["apps.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    return app
