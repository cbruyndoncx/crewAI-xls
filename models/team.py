from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    users = relationship('User', secondary='user_teams', back_populates='teams')
