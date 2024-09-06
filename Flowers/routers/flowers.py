from fastapi import APIRouter, Depends, status, HTTPException, Path, Query
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Flower
from database import SessionLocal

def normalize_name(name):
    return " ".join(i.capitalize() for i in name.strip().split())


router = APIRouter(prefix="/flowers", tags=["flowers"])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

class FlowerRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    quantity: int = Field(gt=0)

class FlowerUpdateRequest(BaseModel):
    quantity: int = Field(gt=0)


@router.get("/get-flowers", status_code=status.HTTP_200_OK)
def get_flowers(db: db_dependency):
    flowers_model = db.query(Flower).all()
    if flowers_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flower not found!")
    return flowers_model


@router.get("/get-flower/{flower_name}", status_code=status.HTTP_200_OK)
def get_flower_by_name(db: db_dependency, flower_name: str = Path(min_length=2, max_length=100)):
    flower_model = db.query(Flower).filter(Flower.name == normailize_name(flower_name)).first()
    if flower_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flower not found!")
    return flower_model

@router.post("/create-flower", status_code=status.HTTP_201_CREATED)
def create_flower(db: db_dependency, flower_request: FlowerRequest):
    flower_model = db.query(Flower).filter(Flower.name == normalize_name(flower_request.name)).first()
    if flower_model is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Flower already exists!")
    flower_model = flower_request.dict()
    flower_model["name"] = normalize_name(flower_request.name)
    flower_post = Flower(**flower_model)
    db.add(flower_post)
    db.commit()

@router.put("/update-flower/{flower_name}", status_code=status.HTTP_200_OK)
def update_flower(db: db_dependency, flower_update_request: FlowerUpdateRequest, flower_name: str = Path(min_length=2, max_length=100)):
    flower_model = db.query(Flower).filter(Flower.name == normalize_name(flower_name)).first()
    if flower_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flower not found!")
    flower_model.quantity = flower_update_request.quantity
    db.add(flower_model)
    db.commit()

@router.delete("/delete-flower/{flower_name}",status_code=status.HTTP_200_OK)
def delete_flower(db: db_dependency, flower_name: str = Path(min_length=2, max_length=100)):
    flower_model = db.query(Flower).filter(Flower.name == normalize_name(flower_name)).first()
    if flower_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flower not found!")
    db.query(Flower).filter(Flower.name == normalize_name(flower_name)).delete()