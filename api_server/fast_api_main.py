import logging
import os
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
import yaml
import etl.transformer as T

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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(thread)d - %(message)s',
    )

@app.get(path = "/", response_class = RedirectResponse)
async def root():
    return "/docs"

@app.get("/api/ping")
async def ping_pong():
    return "pong"

@app.post(
    "/api/transform",
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "required": ["file"],
                        "properties": {
                            "file": {
                                "type": "string",
                                "format": "binary",
                                "description": (
                                    "YAML-файл в кодировке UTF-8 "
                                    "(.yaml или .yml)"
                                ),
                            }
                        },
                    },
                    "encoding": {
                        "file": {
                            "contentType": "application/x-yaml; charset=utf-8"
                        }
                    },
                }
            },
        }
    },
    )
async def transform(file: UploadFile):
    allowed_extensions = (".yaml", ".yml")
    filename: str = file.filename # type: ignore
    logging.info(f"Received file {filename}")
    if not filename.endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Ожидается .yaml или .yml")
    raw_bytes = await file.read()
    try:
        yaml_text = raw_bytes.decode('UTF-8')
        result: str = T.transform(yaml_text)
        return result
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Некорректный YAML: {e}")


if __name__ == '__main__':
    uvicorn.run(app)
