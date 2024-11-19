from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, patients
from app.core.logging_config import LogConfig
from contextlib import asynccontextmanager

log_config = LogConfig()

app = FastAPI(
    title="Healthcare Data Platform",
    description="API for managing elderly patient healthcare data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(patients.router)

@asynccontextmanager
async def startup_event():
    """Initialize services on startup."""
    pass  

@asynccontextmanager
async def shutdown_event():
    """Cleanup on shutdown."""
    pass  