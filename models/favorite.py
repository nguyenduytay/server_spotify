from sqlalchemy import Column, ForeignKey, TEXT
from sqlalchemy.orm import relationship
from models.base import Base

class Favorite(Base):
    __tablename__ = 'favorites'

    id = Column(TEXT, primary_key=True)
    song_id = Column(TEXT, ForeignKey("songs.id"))
    user_id = Column(TEXT, ForeignKey("users.id"))

    song = relationship('Song')
    users = relationship('User', back_populates='favorites')
