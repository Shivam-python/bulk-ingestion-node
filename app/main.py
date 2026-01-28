# app/main.py
from fastapi import FastAPI
from app.api.routes import router
from app.core.exceptions import global_exception_handler

app = FastAPI(title="Hospital Bulk Processor")
app.include_router(router)
app.add_exception_handler(Exception, global_exception_handler)
