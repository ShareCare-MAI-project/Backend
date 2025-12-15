from fastapi import FastAPI
from app.ml.router import router as ml_router
from app.core.config import PROJECT_NAME, SERVER_PORT
from app.core.database import setup_db
from app.utils.server_utils import setup
import os
os.makedirs("uploads", exist_ok=True)
app = FastAPI(title=f"{PROJECT_NAME}")
app.include_router(ml_router, prefix="/api/v1")
setup(app)
setup_db()

@app.get("/",
         summary="Статус API",
         description="Проверка работы API",
         response_description=f'Возвращает "{PROJECT_NAME} работает!"'
         )
async def root():
    return {"message": f"{PROJECT_NAME} работает!"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=SERVER_PORT, reload=True)
