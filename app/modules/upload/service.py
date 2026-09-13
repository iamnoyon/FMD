import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

ALLOWED_TYPES = ["image", "video", "raw"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def _detect_resource_type(content_type: str) -> str:
    if content_type.startswith("image/"):
        return "image"
    if content_type.startswith("video/"):
        return "video"
    return "raw"


def upload_to_cloudinary(file: UploadFile, folder: str = "uploads"):
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not determine file type."
        )

    resource_type = _detect_resource_type(file.content_type)

    if resource_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{resource_type}' is not allowed. Allowed: {', '.join(ALLOWED_TYPES)}"
        )

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds {MAX_FILE_SIZE // (1024 * 1024)}MB limit."
        )

    try:
        result = cloudinary.uploader.upload(
            file.file,
            resource_type=resource_type,
            folder=folder,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

    return {
        "url": result.get("secure_url", result.get("url", "")),
        "public_id": result.get("public_id", ""),
        "format": result.get("format"),
        "resource_type": result.get("resource_type"),
    }


def delete_from_cloudinary(public_id: str, resource_type: str = "image"):
    try:
        result = cloudinary.uploader.destroy(
            public_id,
            resource_type=resource_type,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delete failed: {str(e)}"
        )

    if result.get("result") != "ok":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found or already deleted."
        )

    return result
