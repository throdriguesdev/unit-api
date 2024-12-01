from sqlalchemy.orm import Session
from app.models import Asset
from app.schemas import AssetCreate
from fastapi import HTTPException   
def get_assets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Asset).offset(skip).limit(limit).all()
def create_asset(db: Session, asset: AssetCreate):
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def delete_asset(db: Session, asset_id: int):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")
    db.delete(db_asset)
    db.commit()
    return {"message": f"Ativo com ID {asset_id} deletado com sucesso"}