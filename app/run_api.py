"""
run_api.py
------------
FastAPI Backend Application

Features:
1. FastAPI initialization
2. API route registration
3. Swagger documentation
4. CORS middleware
5. Health monitoring
6. Local development optimization
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router


# -----------------------------------
# CREATE FASTAPI APPLICATION
# -----------------------------------

app = FastAPI(

    title=(
        "SmartRail Crowd Analytics API"
    ),

    description=(
        "AI-powered railway surveillance "
        "analytics backend system."
    ),

    version="1.0.0",

    docs_url="/docs",

    redoc_url="/redoc"
)


# -----------------------------------
# ENABLE CORS
# -----------------------------------

# CORS allows:
# frontend <-> backend communication

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# -----------------------------------
# REGISTER API ROUTES
# -----------------------------------

app.include_router(
    router
)


# -----------------------------------
# ROOT ENDPOINT
# -----------------------------------

@app.get("/")
def root():
    """
    Root API endpoint.
    """

    return {

        "message": (
            "SmartRail API Running"
        ),

        "status": "ACTIVE"
    }


# -----------------------------------
# APPLICATION STARTUP EVENT
# -----------------------------------

@app.on_event("startup")
async def startup_event():
    """
    Application startup handler.
    """

    print(
        "SmartRail FastAPI Server Started"
    )


# -----------------------------------
# APPLICATION SHUTDOWN EVENT
# -----------------------------------

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown handler.
    """

    print(
        "SmartRail FastAPI Server Stopped"
    )


# -----------------------------------
# RUN UVICORN SERVER
# -----------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "run_api:app",

        host="127.0.0.1",

        port=8000,

        reload=True
    )