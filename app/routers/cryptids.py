from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Cryptid
from app.schemas import CryptidCreate, CryptidResponse, CryptidUpdate
from app.database import get_db

router = APIRouter(prefix="/cryptids", tags=["cryptids"])

@router.get("/", response_model=list[CryptidResponse])
def read_cryptids(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cryptids = db.query(Cryptid).offset(skip).limit(limit).all()
    return cryptids

@router.get("/{cryptid_id}", response_model=CryptidResponse)
def read_cryptid(cryptid_id: int, db: Session = Depends(get_db)):
    cryptid = db.query(Cryptid).filter(Cryptid.id == cryptid_id).first()
    if not cryptid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cryptid not found")
    return cryptid

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CryptidResponse)
def create_cryptid(cryptid: CryptidCreate, db: Session = Depends(get_db)):
    db_cryptid = Cryptid(name=cryptid.name, description=cryptid.description, image_url=cryptid.image_url)
    db.add(db_cryptid)
    db.commit()
    db.refresh(db_cryptid)
    return db_cryptid

@router.put("/{cryptid_id}", response_model=CryptidResponse, status_code=status.HTTP_200_OK)
def update_cryptid(cryptid_id: int, cryptid: CryptidUpdate, db:Session=Depends(get_db)):
    db.query(Cryptid).filter(Cryptid.id == cryptid_id).update(cryptid.model_dump())
    db.commit()
    db_cryptid = db.query(Cryptid).filter(Cryptid.id == cryptid_id).first()
    return db_cryptid
    
@router.delete("/{cryptid_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cryptid(cryptid_id: int, db: Session = Depends(get_db)):
    cryptid = db.query(Cryptid).filter(Cryptid.id == cryptid_id).first()
    if not cryptid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cryptid not found")
    db.delete(cryptid)
    db.commit()