import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.api.routes import logs, alerts, auth
from Backend.api.database import engine, Base

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Log Management API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(logs.router, prefix="/api/v1", tags=["Logs"])
app.include_router(alerts.router, prefix="/api/v1", tags=["Alerts"])
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

