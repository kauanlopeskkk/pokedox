from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi.middleware.cors import CORSMiddleware



DATABASE_URL = "sqlite:///./Pokemon.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEU_USUARIO = "kauan"
MEU_SENHA = "admin"

security = HTTPBasic()

class PokemonDB(Base):
    __tablename__ = "Pokemons"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    tipo = Column(String, index=True)
    nivel = Column(Float, index=True)
    captura = Column(Float, index=True)

Base.metadata.create_all(bind=engine)
 



class Pokemon(BaseModel):
    nome: str
    tipo: str
    nivel: float
    captura: float

def f_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, MEU_USUARIO)
    correct_password = secrets.compare_digest(credentials.password, MEU_SENHA)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    return credentials.username

@app.get("/")
def Bem_vindo():
   return("Mensagem: Seja bem-vindo ao mundo dos Pokémon API ")

@app.post("/Pokemons")
def adicionar_pokemon(pokemon:Pokemon, db: Session = Depends(f_db), user: str = Depends(autenticar_usuario)):
    db_pokemon = db.query(PokemonDB).filter(PokemonDB.nome == pokemon.nome).first()
    if db_pokemon:
        raise HTTPException(
            status_code= 400,
            detail= "Esse Pokémon já existe no banco de dados"

        )
    novo_pokemon = PokemonDB(
        nome =pokemon.nome,
        tipo = pokemon.tipo,
        nivel = pokemon.nivel,
        captura = pokemon.captura
        )
    db.add(novo_pokemon)
    db.commit()
    db.refresh(novo_pokemon)
    return{
          "mensagem": "Pokémon adicionado com sucesso ao banco de dados",
        "pokemon":{
            "id": novo_pokemon.id,
            "nome": novo_pokemon.nome,
            "tipo": novo_pokemon.tipo,
            "nivel": novo_pokemon.nivel,
            "captura": novo_pokemon.captura
        }}
@app.get("/Pokemons")
def listar_pokemon(
    db:Session = Depends(f_db), user: str = Depends(autenticar_usuario)):
    pokemons = db.query(PokemonDB).all()
    if not pokemons:
        raise HTTPException(status_code=404, detail="Nenhum Pokémon cadastrado no banco de dados")
    return pokemons

@app.put("/atualizar_nivel/{id_pokemon}")
def atualizar_nivel(
    id_pokemon: int, pokemon: Pokemon, db: Session = Depends(f_db), user: str = Depends(autenticar_usuario)):
    pokemon_db = db.query(PokemonDB).filter(PokemonDB.id == id_pokemon).first()
    if not pokemon_db:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    pokemon_db.nivel = pokemon.nivel
    db.commit()
    db.refresh(pokemon_db)
    return pokemon_db

@app.delete("/deletar_pokemon/{id_pokemon}")
def deletar_pokemon(
    id_pokemon: int, db: Session = Depends(f_db), user: str = Depends(autenticar_usuario)):
    pokemon_db = db.query(PokemonDB).filter(PokemonDB.id == id_pokemon).first()
    if not pokemon_db:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    db.delete(pokemon_db)
    db.commit()
    return {"mensagem": "Pokémon deletado com sucesso"}

