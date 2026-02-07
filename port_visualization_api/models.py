from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    picture = Column(String)

class Port(Base):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String, index=True)
    type = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    details = Column(String)
    # GeoJSON representation can be stored if needed, or constructed on the fly
    geojson = Column(JSON, nullable=True)

class Boundary(Base):
    __tablename__ = "boundaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    geojson_data = Column(JSON)
    
    owner = relationship("User")
