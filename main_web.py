"""
Gerador Profissional de Posts para Instagram - WEB APP
FastAPI Backend
Desenvolvido por Integrius Automações - 2025
"""

import os
import sys
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio
from pathlib import Path

from openai_service import OpenAIService

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar FastAPI
app = FastAPI(
    title="Instagram Post Generator",
    description="Gerador Profissional de Posts para Instagram com Flux.1 e GPT-4",
    version="2.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar diretórios necessários se não existirem
Path("generated_images").mkdir(exist_ok=True)
Path("static").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/generated_images", StaticFiles(directory="generated_images"), name="generated_images")

# Inicializar serviço OpenAI
openai_service = None

@app.on_event("startup")
async def startup_event():
    """Inicializa serviços ao iniciar"""
    global openai_service

    openai_key = os.getenv("OPENAI_API_KEY")
    replicate_key = os.getenv("REPLICATE_API_TOKEN")

    if not openai_key or openai_key == "sua_chave_openai_aqui":
        print("⚠️  AVISO: OPENAI_API_KEY não configurada!")

    if not replicate_key or replicate_key == "sua_chave_replicate_aqui":
        print("⚠️  AVISO: REPLICATE_API_TOKEN não configurada!")

    try:
        openai_service = OpenAIService(
            api_key=openai_key,
            replicate_key=replicate_key,
            provider="replicate"
        )
        print("✅ Serviços OpenAI e Replicate inicializados!")
    except Exception as e:
        print(f"❌ Erro ao inicializar serviços: {e}")

# Modelos Pydantic
class PostNormalRequest(BaseModel):
    tipo_post: str  # feed, reel, stories
    nicho: str
    tema: str
    tom: str  # profissional, inspiracional, educativo, entusiasta, premium
    cta: str  # comentar, curtir, compartilhar, seguir, salvar, link_bio

class BomDiaRequest(BaseModel):
    categoria: str  # sucesso, forca, positividade, foco, amor_proprio, metas, esperanca, paz
    subtema: Optional[str] = ""

class PostDiversoRequest(BaseModel):
    motivo: str  # aniversario, nascimento, casamento, formatura_escola, colacao_grau, formatura_universidade, boa_viagem, bom_retorno
    genero: str  # masculino, feminino, neutro
    idade: int
    personalidade: str  # serio, extrovertido, normal
    mensagem_extra: Optional[str] = ""

class PostResponse(BaseModel):
    success: bool
    imagem_url: Optional[str] = None
    legenda: Optional[str] = None
    hashtags: Optional[list] = None
    erro: Optional[str] = None

# Rotas
@app.get("/")
async def root():
    """Serve a página principal"""
    return FileResponse("templates/index.html")

@app.get("/health")
async def health_check():
    """Health check para Railway"""
    return {
        "status": "healthy",
        "openai_configured": openai_service is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/gerar-post-normal", response_model=PostResponse)
async def gerar_post_normal(request: PostNormalRequest, background_tasks: BackgroundTasks):
    """Gera post normal para Instagram"""

    if not openai_service:
        raise HTTPException(status_code=500, detail="Serviços não inicializados. Verifique as chaves de API.")

    try:
        # Gerar imagem
        imagem_path = openai_service.gerar_imagem_marketing(
            tipo_post=request.tipo_post,
            nicho=request.nicho,
            tema=request.tema,
            tom=request.tom,
            formato="normal"
        )

        # Gerar legenda
        legenda = openai_service.gerar_legenda_marketing(
            tipo_post=request.tipo_post,
            nicho=request.nicho,
            tema=request.tema,
            tom=request.tom,
            cta=request.cta
        )

        # Gerar hashtags
        hashtags = openai_service.gerar_hashtags_marketing(
            nicho=request.nicho,
            tipo_post=request.tipo_post
        )

        # URL da imagem
        imagem_filename = os.path.basename(imagem_path)
        imagem_url = f"/generated_images/{imagem_filename}"

        return PostResponse(
            success=True,
            imagem_url=imagem_url,
            legenda=legenda,
            hashtags=hashtags
        )

    except Exception as e:
        return PostResponse(
            success=False,
            erro=str(e)
        )

@app.post("/api/gerar-bom-dia", response_model=PostResponse)
async def gerar_bom_dia(request: BomDiaRequest, background_tasks: BackgroundTasks):
    """Gera post de Bom Dia Motivacional"""

    if not openai_service:
        raise HTTPException(status_code=500, detail="Serviços não inicializados. Verifique as chaves de API.")

    try:
        # Gerar imagem
        imagem_path = openai_service.gerar_imagem_bomdia(
            categoria=request.categoria,
            subtema=request.subtema
        )

        # Gerar mensagem
        mensagem = openai_service.gerar_mensagem_bomdia(
            categoria=request.categoria,
            subtema=request.subtema
        )

        # Gerar hashtags
        hashtags = openai_service.gerar_hashtags_bomdia(
            categoria=request.categoria
        )

        # URL da imagem
        imagem_filename = os.path.basename(imagem_path)
        imagem_url = f"/generated_images/{imagem_filename}"

        return PostResponse(
            success=True,
            imagem_url=imagem_url,
            legenda=mensagem,
            hashtags=hashtags
        )

    except Exception as e:
        return PostResponse(
            success=False,
            erro=str(e)
        )

@app.post("/api/gerar-post-diverso", response_model=PostResponse)
async def gerar_post_diverso(request: PostDiversoRequest, background_tasks: BackgroundTasks):
    """Gera card comemorativo para WhatsApp"""

    if not openai_service:
        raise HTTPException(status_code=500, detail="Serviços não inicializados. Verifique as chaves de API.")

    try:
        # Gerar card comemorativo
        imagem_path = openai_service.gerar_card_comemorativo(
            motivo=request.motivo,
            genero=request.genero,
            idade=request.idade,
            personalidade=request.personalidade,
            mensagem_extra=request.mensagem_extra
        )

        # Gerar mensagem de acompanhamento
        mensagem = openai_service.gerar_mensagem_comemorativa(
            motivo=request.motivo,
            genero=request.genero,
            idade=request.idade,
            personalidade=request.personalidade,
            mensagem_extra=request.mensagem_extra
        )

        # URL da imagem
        imagem_filename = os.path.basename(imagem_path)
        imagem_url = f"/generated_images/{imagem_filename}"

        return PostResponse(
            success=True,
            imagem_url=imagem_url,
            legenda=mensagem,
            hashtags=[]  # Cards comemorativos não usam hashtags
        )

    except Exception as e:
        return PostResponse(
            success=False,
            erro=str(e)
        )

@app.get("/api/status")
async def status():
    """Status dos serviços"""
    return {
        "openai_configurado": openai_service is not None,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0"
    }

if __name__ == "__main__":
    import uvicorn

    # Porta para Railway (usa variável de ambiente PORT)
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(
        "main_web:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
