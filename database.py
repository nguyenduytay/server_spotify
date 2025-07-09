from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = 'postgresql://spotify_user:vTSsmxooC3NQOJhgZVJoygioP9wislFZ@dpg-d1mu10nfte5s73d4arfg-a/spotify_db_kuxw'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
 db = SessionLocal()
 try:
     yield db
 finally:
     db.close()
