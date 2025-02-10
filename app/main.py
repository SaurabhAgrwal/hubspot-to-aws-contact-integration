from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import contacts

app = FastAPI(
    title="HubSpot Contact Integration",
    description="API for syncing contacts from AWS to HubSpot",
    version="1.0.0"
)



# CORS middleware for web client access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(contacts.router, prefix="/api/v1", tags=["contacts"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)