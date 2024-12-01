from pydantic import BaseModel
from enum import Enum


class AssetCategory(str, Enum):
    hardware = "hardware"
    software = "software"
    network = "network"
    other = "other"


class AssetStatus(str, Enum):
    in_use = "in_use"
    inactive = "inactive"
    maintenance = "maintenance"
    retired = "retired"


class AssetCreate(BaseModel):
    name: str
    description: str
    category: AssetCategory  
    status: AssetStatus 
class AssetResponse(BaseModel):
    id: int
    name: str
    description: str
    category: AssetCategory
    status: AssetStatus

    class Config:
        orm_mode = True  