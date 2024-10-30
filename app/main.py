from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Cryptid
from app.database import get_db
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CryptidModel(BaseModel):
    name:str
    description:str
    image_url:str

@app.get("/cryptids/")
def read_cryptids(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cryptids = db.query(Cryptid).offset(skip).limit(limit).all()
    return cryptids

@app.get("/cryptids/{cryptid_id}")
def read_cryptid(cryptid_id: int, db: Session = Depends(get_db)):
    cryptid = db.query(Cryptid).filter(Cryptid.id == cryptid_id).first()
    return cryptid

@app.post("/cryptids/", status_code=status.HTTP_201_CREATED, response_model=CryptidModel)
def create_cryptid(cryptid: CryptidModel, db: Session = Depends(get_db)):
    db_cryptid = Cryptid(name=cryptid.name, description=cryptid.description, image_url=cryptid.image_url)
    db.add(db_cryptid)
    db.commit()
    db.refresh(db_cryptid)
    return db_cryptid

@app.put("/cryptids/{cryptid_id}", status_code=status.HTTP_201_CREATED)
def update_cryptid(cryptid_id: int, cryptid: CryptidModel, db:Session=Depends(get_db)):
    db.query(Cryptid).filter(Cryptid.id == cryptid_id).update(cryptid.model_dump())
    db.commit()
    db_cryptid = db.query(Cryptid).filter(Cryptid.id == cryptid_id).first()
    return db_cryptid
    
@app.delete("/cryptids/{cryptid_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cryptid(cryptid_id: int, db: Session = Depends(get_db)):
    cryptid = db.query(Cryptid).filter(Cryptid.id == cryptid_id).first()
    if cryptid is None:
        raise HTTPException(status_code=404, detail="Cryptid not found")
    db.delete(cryptid)
    db.commit()
    return {"message": "Cryptid deleted successfully"}