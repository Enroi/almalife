import logging
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from etl.cbr.load_rates import router as load_cbr_router

app = FastAPI(
    swagger_ui_parameters = {
        "filter": True,
        "operationsSorter": "alpha",
        "tagsSorter": "alpha",
        "displayRequestDuration": True,
    },
    description = """
        Модуль запуска преобразования данных, как ETL так и бизнес расчетов.
        """,
    version = "0.1",
    title = "Almalife API",
    summary = "Almalife API server",
    debug = os.getenv("FASTAPI_DEBUG", "false") == "true",
)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(thread)d - %(message)s',
                    )

@app.get(path = "/", response_class = RedirectResponse)
async def root():
    return "/docs"

@app.get("/api/ping")
async def ping_pong():
    return "pong"

app.include_router(load_cbr_router)

if __name__ == '__main__':
    uvicorn.run(app)
