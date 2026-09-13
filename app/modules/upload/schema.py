from pydantic import BaseModel
from typing import Optional


class UploadData(BaseModel):
    url: str
    public_id: str
    format: Optional[str] = None
    resource_type: Optional[str] = None


class UploadResponse(BaseModel):
    success: bool
    message: str
    data: Optional[UploadData] = None
