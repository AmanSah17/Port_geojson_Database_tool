import os
from dotenv import load_dotenv

# Explicitly load .env from the same directory as main.py
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database, auth, crud, cache
from .database import engine
import json
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Port Visualization API", description="API for Crimson Energy Experts Port Visualization", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Wildcard not allowed with allow_credentials=True
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Seed data if empty
    db = database.SessionLocal()
    if db.query(models.Port).count() == 0:
        seed_file_path = os.path.join(os.path.dirname(__file__), "seed_ports.json")
        # Check if file exists in current dir
        if not os.path.exists(seed_file_path):
             seed_file_path = "seed_ports.json"
        
        if os.path.exists(seed_file_path):
            with open(seed_file_path, "r") as f:
                ports_data = json.load(f)
                for port_data in ports_data:
                    # Convert lat/lon keys if necessary or map them
                    # The seed data has "lat", "lon", "name", "country", "type", "details"
                    # Our schema expects matching keys, which they do.
                    port_in = schemas.PortCreate(**port_data)
                    crud.create_port(db, port_in)
            print("Database seeded with ports.")
    db.close()

@app.post("/auth/google")
async def login_google(token: str = Body(..., embed=True), db: Session = Depends(database.get_db)):
    import sys
    import traceback
    try:
        # Verify token with Google
        try:
            user_info = await auth.verify_google_token(token)
        except Exception as e:
             raise HTTPException(status_code=400, detail=f"Invalid token: {str(e)}")

        if not user_info.get("email_verified"):
             raise HTTPException(status_code=400, detail="Email not verified")

        # Check if user exists, else create
        user = crud.get_user_by_email(db, user_info["email"])
        if not user:
            user = crud.create_user(db, user_info)
        
        # Create JWT
        access_token = auth.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer", "user": {"name": user.name, "picture": user.picture}}
    except HTTPException:
        raise
    except Exception as e:
        print(f"CRITICAL AUTH ERROR: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Internal Auth Error: {str(e)}")

@app.get("/ports", response_model=list[schemas.Port])
def read_ports(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    # Try cache first
    cached = cache.get_cached_ports()
    if cached and skip == 0:
        return cached

    ports = crud.get_ports(db, skip=skip, limit=limit)
    
    # Cache all ports if we fetched the default page
    if skip == 0 and limit >= 100:
         # Serialize Pydantic models to dicts for caching
         ports_dict = [port.__dict__ for port in ports]
         # Remove internal SQLAlchemy state
         for p in ports_dict:
             p.pop('_sa_instance_state', None)
         cache.set_cached_ports(ports_dict)
         
    return ports

@app.get("/boundaries", response_model=list[schemas.Boundary])
def read_boundaries(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.get_boundaries(db, current_user.id)

@app.post("/boundaries", response_model=schemas.Boundary)
def create_boundary(boundary: schemas.BoundaryCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_boundary(db, boundary, current_user.id)

@app.get("/")
def read_root():
    return {"message": "Crimson Energy Experts Port Visualization API is running."}
