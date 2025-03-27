from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://recipedb_sw6x_user:BfqJskerYq2f3Y2F7i2vvrOoNcZ9B2DU@dpg-cviron6r433s73e732b0-a/recipedb_sw6x"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
