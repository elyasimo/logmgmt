import logging.config
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from Backend.api.routes import logs, customers, products, users, groups
from Backend.api.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
import random
from datetime import datetime

# Configure logging
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    }
})

logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the routers
app.include_router(logs.router, prefix="/api/v1", dependencies=[Depends(get_db)])
app.include_router(customers.router, prefix="/api/v1", dependencies=[Depends(get_db)])
app.include_router(products.router, prefix="/api/v1", dependencies=[Depends(get_db)])
app.include_router(users.router, prefix="/api/v1", dependencies=[Depends(get_db)])
app.include_router(groups.router, prefix="/api/v1", dependencies=[Depends(get_db)])

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Log Management API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

