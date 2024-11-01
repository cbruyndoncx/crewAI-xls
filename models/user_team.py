from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class UserTeam(Base):
    __tablename__ = 'user_teams'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True)
