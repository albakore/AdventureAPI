from sqlmodel import create_engine, Session, SQLModel

engine = create_engine('sqlite:///database/adventure.db')

def crear_session():
    with Session(engine) as session:
        yield session

def crear_tablas():
	SQLModel.metadata.create_all(engine)

def borrar_tablas():
	SQLModel.metadata.drop_all(engine)


