from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Dobrodar', version='2025.11.1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Импортируем роутеры
from app.auth.auth_routes import router as auth_router
from app.items.items_routes import router as items_router
from app.profile.profile_routes import router as profile_router
from app.funds.funds_routes import router as funds_router
from app.needs.needs_routes import router as needs_router

# Подключаем маршруты
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(profile_router, prefix="/profile", tags=["profile"])
app.include_router(funds_router, prefix="/funds", tags=["funds"])
app.include_router(needs_router, prefix="/requests", tags=["needs"])

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в Dobrodar "}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)