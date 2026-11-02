from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Cryptid
from app.schemas import CryptidCreate, CryptidResponse, CryptidUpdate

router = APIRouter(prefix="/cryptids", tags=["cryptids"])
session = Depends(get_db)


@router.get("/", response_model=list[CryptidResponse])
def read_cryptids(skip: int = 0, limit: int = 10, db: Session = session):
    """
    Return a list of all cryptids.

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (default 10)
    """
    cryptids = db.query(Cryptid).offset(skip).limit(limit).all()
    return cryptids


@router.get("/{cryptid_id}", response_model=CryptidResponse)
def read_cryptid(cryptid_id: int, db: Session = session):
    """
    Return a single cryptid by ID. Returns 404 if not found.
    """
    cryptid = db.query(Cryptid).filter(Cryptid.id == cryptid_id).first()
    if not cryptid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cryptid not found"
        )
    return cryptid


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CryptidResponse)
def create_cryptid(cryptid: CryptidCreate, db: Session = session):
    """
    Create a new cryptid record.
    """
    db_cryptid = Cryptid(
        name=cryptid.name, description=cryptid.description, image_url=cryptid.image_url
    )
    db.add(db_cryptid)
    db.commit()
    db.refresh(db_cryptid)
    return db_cryptid


@router.put(
    "/{cryptid_id}", response_model=CryptidResponse, status_code=status.HTTP_200_CREATED
)
def update_cryptid(cryptid_id: int, cryptid: CryptidUpdate, db: Session = session):
    """
    Update an existing cryptid by ID. Returns 404 if not found.
    """
    db_cryptid = db.query(Cryptid).filter(Cryptid.id == cryptid_id).first()
    if not db_cryptid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cryptid not found"
        )
    for field, value in cryptid.model_dump().items():
        setattr(db_cryptid, field, value)
    db.commit()
    db.refresh(db_cryptid)
    return db_cryptid


@router.delete("/{cryptid_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cryptid(cryptid_id: int, db: Session = session):
    """
    Delete a cryptid by ID. Returns 404 if not found.
    """
    cryptid = db.query(Cryptid).filter(Cryptid.id == cryptid_id).first()
    if not cryptid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cryptid not found"
        )
    db.delete(cryptid)
    db.commit()
    