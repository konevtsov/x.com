import logging

import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from configuration.config import settings
from routes import api_router
from create_fastapi_app import create_app


logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
)

main_app = create_app(
    title=settings.run.title,
    create_custom_static_urls=True,
)

main_app.include_router(api_router)
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
    allow_credentials=settings.cors.allow_credentials,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
