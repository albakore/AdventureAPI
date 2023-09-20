from fastapi import FastAPI, Depends, HTTPException
from database.config import crear_tablas, borrar_tablas,engine, crear_session
from models.Hero import Heroe,HeroeConAtributos,HeroeRead
from models.Combate import Duelo, DueloRegistro, DueloEstadisticas
from models.Terreno import Terreno,TerrenoRead,TerrenoConMazmorra,Mazmorra,MazmorraBase
from sqlmodel import Session, select
app = FastAPI()

@app.on_event("startup")
def on_startup():
    crear_tablas()

@app.on_event("shutdown")
def on_shutdown():
    borrar_tablas()

@app.get('/{id}',response_model=HeroeConAtributos)
def getHero(id:int, session : Session = Depends(crear_session)):
	return Heroe.ObtenerUno(id,session)


@app.post('/add',response_model=HeroeRead)
def addHero(session : Session = Depends(crear_session)):
    return Heroe.Crear(session)

@app.post('/',response_model=DueloEstadisticas)
def makeDuelo(id1: int, id2:int ,session : Session = Depends(crear_session)):
    return Duelo.IniciarDuelo(id1,id2,session)

# --- Terrenos ---

@app.post('/addTerrain',tags=['Terreno'],response_model=TerrenoConMazmorra)
def addTerrain(terreno: TerrenoRead, session : Session = Depends(crear_session)):
    nuevoTerreno = Terreno(**terreno.dict())
    session.add(nuevoTerreno)
    session.commit()
    session.refresh(nuevoTerreno)
    return nuevoTerreno
    
@app.get('/getTerrain/',tags=['Terreno'],response_model=TerrenoConMazmorra)
def getTerrain(x: int, y:int, session : Session = Depends(crear_session)):
    try: 
        sentencia = select(Terreno).where(Terreno.x == int(x)).where(Terreno.y ==  int(y))
        print(sentencia)
        terreno = session.exec(sentencia).one()
        return terreno
    except:
        raise HTTPException(status_code=404, detail='No se encontro el terreno')
    
@app.put('/putTerrain/',tags=['Terreno'],response_model=TerrenoConMazmorra)
def putTerrain(terreno: TerrenoRead, session : Session = Depends(crear_session)):
    try: 
        sentencia = select(Terreno).where(Terreno.x == int(terreno.x)).where(Terreno.y ==  int(terreno.y))
        terrenoEncontrado = session.exec(sentencia).one()
        if terrenoEncontrado : 
            terrenoEncontrado.id_mazmorra = terreno.id_mazmorra
            session.add(terrenoEncontrado)
            session.commit()
            session.refresh(terrenoEncontrado)
            return terrenoEncontrado
        else:
            raise HTTPException(status_code=404, detail='No se encontro el terreno')
    except:
        raise HTTPException(status_code=404, detail='No se encontro el terreno')

# --- Mazmorras ---

@app.post('/addMazmorra',tags=['Terreno'],response_model=MazmorraBase)
def addMazmorra(mazmorra: Mazmorra, session : Session = Depends(crear_session)):
    nuevoMazmorra = Mazmorra(**mazmorra.dict())
    session.add(nuevoMazmorra)
    session.commit()
    session.refresh(nuevoMazmorra)
    return nuevoMazmorra
    
@app.get('/getMazmorra/',tags=['Terreno'],response_model=MazmorraBase)
def getMazmorra(id : int = False, session : Session = Depends(crear_session)):
    try: 
        sentencia = select(Mazmorra).where(Mazmorra.id == int(id))
        mazmorra = session.exec(sentencia).one()
        return mazmorra
    except:
        raise HTTPException(status_code=404, detail='No se encontro una mazmorra en el terreno o no existe la ubicacion')




