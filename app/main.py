from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import pokemons

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pokedox API",
    description="API para gerenciamento de Pokémons, inspirada na PokéAPI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pokemons.router)


@app.get("/", tags=["Root"], summary="Mensagem de boas-vindas")
def bem_vindo():
    return {"mensagem": "Seja bem-vindo à Pokedox API"}
