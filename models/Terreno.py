from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class MazmorraBase(SQLModel):
    nivel: int = 0
    enemigos : int = 0
    tesoro : int = 0
    experiencia : int = 0

class Mazmorra(MazmorraBase, table = True):
    id: Optional[int] = Field(default=None,primary_key=True)
    terreno: Optional['Terreno'] = Relationship(sa_relationship_kwargs={'uselist':False}, back_populates='mazmorra') 



class TerrenoBase(SQLModel):
    dificultad : int = 0
    
class Terreno(TerrenoBase, table = True):
    x : int = Field(primary_key=True)
    y : int = Field(primary_key=True)
    id_mazmorra : Optional[int] = Field(default=None, foreign_key='mazmorra.id')
    mazmorra : Optional[Mazmorra] = Relationship(back_populates='terreno')


class TerrenoRead(SQLModel):
	x: int
	y: int
	id_mazmorra : Optional[int] = None

class TerrenoConMazmorra(TerrenoRead):
    mazmorra : Optional[Mazmorra] = None
    