from fastapi import APIRouter, FastAPI
from app.api.endpoints import router 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Gen AI Email Processing API")  # This creates the FastAPI app instance

# Allowed origins (Update this for production)
origins = [
    "http://localhost:4200",  # Angular frontend (Local)
    "https://vivek0912-genaiemailclassification.hf.space",  # Hugging Face frontend
]

#router = APIRouter()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Replace "*" with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes from endpoints.py
app.include_router(router, prefix="/api")  # You can remove prefix if not needed

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}

#app.include_router(router)
