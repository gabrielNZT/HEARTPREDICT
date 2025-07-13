import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.model_manager import get_model_manager
from app.routers.prediction import router as prediction_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação: carrega modelo na inicialização e loga no shutdown
    """
    logger.info("Iniciando API com modelo aprimorado...")
    try:
        get_model_manager().load_model()
        logger.info("Modelo aprimorado carregado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao carregar modelo aprimorado: {e}")
        raise

    yield

    logger.info("Finalizando API...")

# Instância da aplicação FastAPI
title = "Enhanced Cardiac Risk Prediction API"
description = ("API aprimorada para previsão de risco cardíaco usando pipeline científico "
               "com LightGBM")
version = "2.0.0"

app = FastAPI(
    title=title,
    description=description,
    version=version,
    lifespan=lifespan
)

# Registrar rotas
app.include_router(prediction_router)

if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8002,
        log_level="info"
    )
