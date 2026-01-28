# app/main.py
from fastapi import FastAPI
from app.api.routes import router
from app.api.home import router as home_router
from app.api.health import router as health_router
from app.core.exceptions import global_exception_handler

app = FastAPI(title="Hospital Bulk Processor")
app.include_router(router)
app.include_router(home_router)
app.include_router(health_router)
app.add_exception_handler(Exception, global_exception_handler)
