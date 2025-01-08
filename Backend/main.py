from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.api.routes import alerts, auth, dashboards, ingest, logs, metrics, schemas, search, sources, changelog, dashboard
from Backend.api.database import engine, Base

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
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(changelog.router, prefix="/api/v1", tags=["Changelog"])
app.include_router(alerts.router, prefix="/api/v1", tags=["Alerts"])
app.include_router(dashboards.router, prefix="/api/v1", tags=["Dashboards"])
app.include_router(ingest.router, prefix="/api/v1", tags=["Log Ingestion"])
app.include_router(logs.router, prefix="/api/v1", tags=["Logs"])
app.include_router(metrics.router, prefix="/api/v1", tags=["Metrics"])
app.include_router(schemas.router, prefix="/api/v1", tags=["Schemas"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(sources.router, prefix="/api/v1", tags=["Sources"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

