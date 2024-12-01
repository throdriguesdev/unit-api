from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Asset
from app.schemas import AssetCreate, AssetResponse
from app.crud import get_assets, create_asset, delete_asset
import csv
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)
def normalize_category(category: str) -> str:
    return category.lower()


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de cadastro de ativos de TI!"}


@app.get("/assets/", response_model=list[AssetResponse])
def read_assets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_assets(db, skip=skip, limit=limit)


@app.post("/assets/", response_model=AssetResponse)
def create_new_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    return create_asset(db, asset)

@app.post("/upload/")
async def upload_assets(file: UploadFile, db: Session = Depends(get_db)):
    contents = await file.read()
    decoded = contents.decode("utf-8")
    csv_reader = csv.DictReader(decoded.splitlines())

    for row in csv_reader:
        asset = AssetCreate(
            name=row["name"],
            description=row["description"],
            category=normalize_category(row["category"]),
            status=row["status"]
        )
        create_asset(db, asset) 

    return {"message": "Assets uploaded successfully"}

def update_asset(db: Session, asset_id: int, asset_data: AssetCreate):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")
    for key, value in asset_data.dict().items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@app.put("/assets/{asset_id}", response_model=AssetResponse)
def update_existing_asset(asset_id: int, asset: AssetCreate, db: Session = Depends(get_db)):
    return update_asset(db, asset_id, asset)


@app.delete("/assets/{asset_id}")
def delete_existing_asset(asset_id: int, db: Session = Depends(get_db)):
    return delete_asset(db, asset_id)