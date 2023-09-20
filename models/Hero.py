from sqlmodel import Session, select, Relationship, SQLModel, Field
from fastapi import Depends, HTTPException
from database.config import engine, crear_session
from typing import Optional, List
from random import randint

def atributo_aleatorio():
	return randint(1,5)

class AtributoBase(SQLModel):
	vitalidad : int = Field(default_factory=atributo_aleatorio)
	aguante : int = Field(default_factory=atributo_aleatorio)
	fuerza : int = Field(default_factory=atributo_aleatorio)
	destreza : int = Field(default_factory=atributo_aleatorio)
	agilidad : int = Field(default_factory=atributo_aleatorio)
	magia : int = Field(default_factory=atributo_aleatorio)

class Atributo(AtributoBase, table = True):
    id: Optional[int] = Field(default=None,primary_key=True)
    heroe: Optional['Heroe'] = Relationship(sa_relationship_kwargs={'uselist':False}, back_populates='atributos')

class AtributoRead(AtributoBase):
    id : int

class HeroeBase(SQLModel):
	nombre: str = 'Heroe'
	salud: int = 100
	stamina: int = 50
	mana: int = 25

class Heroe(HeroeBase,table = True):
	id: Optional[int] = Field(default=None,primary_key=True)
	id_atributo: Optional[int] = Field(default=None,foreign_key='atributo.id')
	atributos: Optional['Atributo'] = Relationship(back_populates='heroe')

	@staticmethod
	def Crear(session:Session):
		atributoNuevo = Atributo()
		heroe = Heroe()
		session.add(atributoNuevo)
		session.commit()
  
		heroe.id_atributo = atributoNuevo.id
		session.add(heroe)
		session.commit()
		session.refresh(heroe)
		return heroe

	@staticmethod
	def ObtenerUno(id:int,session:Session):
		heroe = session.get(Heroe,id)
		if not heroe:
			raise HTTPException(detail='No existe heroe',status_code=404)
		return heroe

	@staticmethod
	def ObtenerTodo():
		pass

	
	def AtaqueFisico(self):
		return randint(5,15)
 
	def AtaqueMagico(self) : pass

	def Defender(self) : pass
 
	def Esquivar(self) : pass
 
	def ContraAtaque(self) : pass
 
	def Morir(self) : pass
 

class HeroeRead(HeroeBase):
    id : int

class HeroeConAtributos(HeroeRead):
    atributos : Optional[AtributoRead] = None