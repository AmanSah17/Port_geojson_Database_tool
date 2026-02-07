from sqlalchemy.orm import Session
from . import models, schemas

def get_ports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Port).offset(skip).limit(limit).all()

def create_port(db: Session, port: schemas.PortCreate):
    db_port = models.Port(**port.dict())
    db.add(db_port)
    db.commit()
    db.refresh(db_port)
    return db_port

def get_boundaries(db: Session, user_id: int):
    return db.query(models.Boundary).filter(models.Boundary.user_id == user_id).all()

def create_boundary(db: Session, boundary: schemas.BoundaryCreate, user_id: int):
    db_boundary = models.Boundary(**boundary.dict(), user_id=user_id)
    db.add(db_boundary)
    db.commit()
    db.refresh(db_boundary)
    return db_boundary

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user_info: dict):
    db_user = models.User(
        email=user_info["email"],
        name=user_info.get("name"),
        picture=user_info.get("picture")
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
