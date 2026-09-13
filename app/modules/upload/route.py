from fastapi import APIRouter, Depends, UploadFile, File, Query
from app.utils.token_service import get_current_user
from .schema import UploadResponse, UploadData
from .service import upload_to_cloudinary, delete_from_cloudinary

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/", response_model=UploadResponse, description="Upload a file to Cloudinary")
def upload_file(
    file: UploadFile = File(...),
    folder: str = Query(default="uploads", description="Cloudinary folder name"),
    current_user=Depends(get_current_user),
):
    result = upload_to_cloudinary(file, folder)

    return UploadResponse(
        success=True,
        message="File uploaded successfully!",
        data=UploadData(**result),
    )


@router.delete("/{public_id}", description="Delete a file from Cloudinary")
def delete_file(
    public_id: str,
    resource_type: str = Query(default="image", description="Resource type: image, video, or raw"),
    current_user=Depends(get_current_user),
):
    delete_from_cloudinary(public_id, resource_type)

    return {
        "success": True,
        "message": "File deleted successfully!",
    }
