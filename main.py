from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import lifespan
from routes.post_router import router as post_router
from routes.auth_router import router as auth_router
from routes.media_router import router as media_router
from models.core import HealthResponse



app = FastAPI(lifespan=lifespan)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=post_router, prefix="/posts")
app.include_router(router=auth_router, prefix="/auth")
app.include_router(router=media_router,prefix="/medias")
@app.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status="Ok")
