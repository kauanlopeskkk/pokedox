from sqlalchemy.orm import Session

from app import models, schemas


def get_pokemon(db: Session, pokemon_id: int) -> models.Pokemon | None:
    return db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()


def get_pokemon_by_nome(db: Session, nome: str) -> models.Pokemon | None:
    return db.query(models.Pokemon).filter(models.Pokemon.nome == nome).first()


def list_pokemons(db: Session, skip: int = 0, limit: int = 100) -> list[models.Pokemon]:
    return db.query(models.Pokemon).offset(skip).limit(limit).all()


def create_pokemon(db: Session, pokemon: schemas.PokemonCreate) -> models.Pokemon:
    db_pokemon = models.Pokemon(**pokemon.model_dump())
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon


def update_pokemon(
    db: Session, db_pokemon: models.Pokemon, dados: schemas.PokemonUpdate
) -> models.Pokemon:
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(db_pokemon, campo, valor)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon


def delete_pokemon(db: Session, db_pokemon: models.Pokemon) -> None:
    db.delete(db_pokemon)
    db.commit()
