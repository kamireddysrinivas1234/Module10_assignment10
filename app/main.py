
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .logger import configure_logging, logger
from . import operations as ops
from .schemas import CalcRequest, CalcResponse
from .routers.users import router as users_router

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
configure_logging(LOG_LEVEL)

app = FastAPI(title="FastAPI Calculator + Users", version="2.0.0")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(users_router)

@app.get("/health")
def health():
    logger.debug("Health check ping")
    return {"status": "ok"}

@app.post("/api/calc", response_model=CalcResponse)
def api_calc(payload: CalcRequest):
    logger.info("API /api/calc called with %s", payload.dict())
    try:
        if payload.op == "add": result = ops.add(payload.a, payload.b)
        elif payload.op == "sub": result = ops.subtract(payload.a, payload.b)
        elif payload.op == "mul": result = ops.multiply(payload.a, payload.b)
        else: result = ops.divide(payload.a, payload.b)
        logger.info("Computed result: %s", result)
        return CalcResponse(result=float(result))
    except ZeroDivisionError as e:
        logger.exception("Zero division error")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
