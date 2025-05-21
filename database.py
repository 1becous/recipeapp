from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = "postgresql://uf7pno9o6dabuo:p776a0e9d2354688d222fee466f3fa1d72d92b99206bdc00d092210569aad15c0@c7lolh640htr57.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/dcc94e96af5e61"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
