from fastapi import APIRouter, FastAPI
from app.api.endpoints import router 


app = FastAPI(title="Gen AI Email Processing API")  # This creates the FastAPI app instance

#router = APIRouter()

# Include API routes from endpoints.py
app.include_router(router, prefix="/api")  # You can remove prefix if not needed

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}

#app.include_router(router)
