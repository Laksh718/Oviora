import os
import sys
import importlib.util
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure the backend directory is in the import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.logger import logger
from app.api.upload import router as upload_router
from app.api.analyze import router as analyze_router
from app.api.reports import router as reports_router
from app.api.health import router as health_router

# Dynamically import inference since directory starts with a number
module_name = "clinical_risk_engine_inference"
module_path = os.path.join(os.path.dirname(__file__), '..', 'models', '01_clinical_risk_engine', 'inference.py')
spec = importlib.util.spec_from_file_location(module_name, module_path)
inference = importlib.util.module_from_spec(spec)
sys.modules[module_name] = inference
spec.loader.exec_module(inference)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Oviora Backend Services")
    settings.create_directories()
    yield
    logger.info("Stopping Oviora Backend Services")

app = FastAPI(
    title="Oviora Backend API",
    version=settings.VERSION,
    description="Unified API endpoints for Clinical Risk Assessment and Hormone Intelligence Analysis.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lab Intelligence Engine (LIE-v1.0) Routers
app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(reports_router)
app.include_router(health_router)

# Clinical Risk Engine (CRE-v1.0) Endpoint
@app.post("/api/v1/clinical-risk/predict")
def predict_clinical_risk(payload: Dict[str, Any]):
    return inference.predict(payload)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Oviora API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }
