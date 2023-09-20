from sqlmodel import Session, select, Relationship, SQLModel, Field
from fastapi import Depends, HTTPException
from database.config import engine, crear_session
from typing import Optional, List
from random import randint

class DueloBase(SQLModel):
	id : Optional[int] = Field(default=None,primary_key=True)
	id_heroe_uno : Optional[int] = Field(default=None,foreign_key='heroe.id')
	id_heroe_dos : Optional[int] = Field(default=None,foreign_key='heroe.id')
	id_heroe_ganador : Optional[int] = Field(default=None,foreign_key='heroe.id')
	id_heroe_perdedor : Optional[int] = Field(default=None,foreign_key='heroe.id')

class Duelo(DueloBase,table = True):
	registro : List['DueloRegistro'] = Relationship(back_populates='duelo')

	@staticmethod
	def IniciarDuelo(idHeroe1, idHeroe2, session : Session):
		duelo = Duelo(id_heroe_uno=idHeroe1,id_heroe_dos=idHeroe2)
		session.add(duelo)
		session.commit()

		registro1 = DueloRegistro(
      						id_duelo=duelo.id ,
                           	descripcion='Le pego a fulano')
		session.add(registro1)
		registro2 = DueloRegistro(
      						id_duelo=duelo.id ,
                           	descripcion='Este la pego a mengano')
		session.add(registro2)
		registro3 = DueloRegistro(
      						id_duelo=duelo.id ,
                           	descripcion='Se hicieron pija')
		session.add(registro3)
		registro4 = DueloRegistro(
      						id_duelo=duelo.id ,
                           	descripcion='Se murio uno')
		session.add(registro4)
		duelo.id_heroe_ganador = idHeroe2
		duelo.id_heroe_perdedor = idHeroe1
		session.commit()
		session.refresh(duelo)
		return duelo


class DueloRegistroBase(SQLModel):
	id : Optional[int] = Field(default=None,primary_key=True)
	id_duelo : Optional[int] = Field(default=None,foreign_key='duelo.id')
	turno : Optional[int] = Field(default=None)
	descripcion : str = ''

class DueloRegistro(DueloRegistroBase,table = True):
	duelo : Optional['Duelo'] = Relationship(back_populates='registro')

class DueloRegistroRead(SQLModel):
    descripcion : str = ''

class DueloEstadisticas(DueloBase):
	registro : List[DueloRegistroRead] = []