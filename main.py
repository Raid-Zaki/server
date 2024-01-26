from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import lifespan
from routes.auth_router import router as auth_router
from routes.media_router import router as media_router
from routes.chat_router import router as chat_router
from responses.core import HealthResponse

from fastapi_pagination import  add_pagination

app = FastAPI(lifespan=lifespan)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=auth_router, prefix="/auth")
app.include_router(router=media_router,prefix="/medias")
app.include_router(router=chat_router,prefix="/chats")
add_pagination(app)
@app.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status="Ok")
