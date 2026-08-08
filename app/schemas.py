from pydantic import BaseModel, ConfigDict, Field


class PokemonBase(BaseModel):
    nome: str = Field(..., examples=["Pikachu"])
    tipo: str = Field(..., examples=["Elétrico"])
    nivel: float = Field(..., ge=0, examples=[5])
    captura: float = Field(..., ge=0, le=1, examples=[0.45])


class PokemonCreate(PokemonBase):
    pass


class PokemonUpdate(BaseModel):
    nome: str | None = None
    tipo: str | None = None
    nivel: float | None = Field(default=None, ge=0)
    captura: float | None = Field(default=None, ge=0, le=1)


class PokemonOut(PokemonBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
