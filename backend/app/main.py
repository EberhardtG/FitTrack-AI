from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base, engine
from app.routers.auth import router as auth_router
from app.routers.weight import router as weight_router
from app.routers.workout_log import router as workout_logs_router
from app.routers.workout_assistant import router as workout_assistant_router
from app.security.config import settings
from app.routers.rag import router as rag_router
from app.routers.rag_admin import router as rag_router


print("Loaded secret:", settings.SECRET_KEY)
print("Loaded algorithm:", settings.ALGORITHM)
print("Loaded access token expiry minutes:", settings.ACCESS_TOKEN_EXPIRE_MINUTES)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FitTrack AI",
    version="1.0.0"
)

# Health check
@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "message": "FITtrack API is running"}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)


# Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(weight_router, tags=["Weights"])
app.include_router(workout_logs_router, tags=["Workout Logs"])
app.include_router(workout_assistant_router, tags=["Workout Assistant"])
app.include_router(rag_router, tags=["RAG"])
app.include_router(rag_router)
# Local dev entrypoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
