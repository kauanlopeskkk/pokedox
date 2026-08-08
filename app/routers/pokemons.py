from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import autenticar_usuario
from app.database import get_db

router = APIRouter(prefix="/pokemons", tags=["Pokémons"])


@router.post(
    "",
    response_model=schemas.PokemonOut,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo Pokémon",
)
def criar_pokemon(
    pokemon: schemas.PokemonCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(autenticar_usuario),
):
    if crud.get_pokemon_by_nome(db, pokemon.nome):
        raise HTTPException(status_code=400, detail="Esse Pokémon já existe no banco de dados")
    return crud.create_pokemon(db, pokemon)


@router.get("", response_model=list[schemas.PokemonOut], summary="Lista todos os Pokémons")
def listar_pokemons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario: str = Depends(autenticar_usuario),
):
    return crud.list_pokemons(db, skip=skip, limit=limit)


@router.get("/{pokemon_id}", response_model=schemas.PokemonOut, summary="Busca um Pokémon pelo id")
def buscar_pokemon(
    pokemon_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(autenticar_usuario),
):
    db_pokemon = crud.get_pokemon(db, pokemon_id)
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    return db_pokemon


@router.put("/{pokemon_id}", response_model=schemas.PokemonOut, summary="Atualiza um Pokémon existente")
def atualizar_pokemon(
    pokemon_id: int,
    dados: schemas.PokemonUpdate,
    db: Session = Depends(get_db),
    usuario: str = Depends(autenticar_usuario),
):
    db_pokemon = crud.get_pokemon(db, pokemon_id)
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    return crud.update_pokemon(db, db_pokemon, dados)


@router.delete("/{pokemon_id}", summary="Remove um Pokémon")
def deletar_pokemon(
    pokemon_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(autenticar_usuario),
):
    db_pokemon = crud.get_pokemon(db, pokemon_id)
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    crud.delete_pokemon(db, db_pokemon)
    return {"mensagem": "Pokémon deletado com sucesso"}
