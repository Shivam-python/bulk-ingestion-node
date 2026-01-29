# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings

from app.api.routes import router
from app.api.home import router as home_router
from app.api.health import router as health_router
from app.api.metrics import router as metrics_router
from app.core.global_exceptions import global_exception_handler
from app.middlewares.logging_middleware import LoggingMiddleware
from app.middlewares.metrics_middleware import MetricsMiddleware

app = FastAPI(title="Hospital Bulk Processor")

# adding middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(MetricsMiddleware)
app.add_middleware(LoggingMiddleware)

# adding routers
app.include_router(router)
app.include_router(metrics_router)
app.include_router(home_router)
app.include_router(health_router)

# adding custom exception handlers
app.add_exception_handler(Exception, global_exception_handler)
