from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.user.model import User, Role
from app.utils.permission import Permissions


def get_permissions_for_role(role: Role):
    if role in (Role.SUPERADMIN, Role.ADMIN):
        return [p.value for p in Permissions]
    return []


def create_new_user(req, db: Session, current_user):
    existing_user = (
        db.query(User)
        .filter(User.phone == req.phone)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists with this phone."
        )

    try:
        new_user = User(
            name=req.name,
            phone=req.phone,
            role=req.role,
            area=req.area,
            avenue=req.avenue,
            road=req.road,
            house=req.house,
            flat=req.flat,
            verified=True,
            permissions=get_permissions_for_role(req.role),
            createdBy=current_user.get('phone', 'admin'),
            createdAt=datetime.now(timezone.utc)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": "User created successfully.",
        "data": {
            "id": new_user.id,
            "name": new_user.name,
            "phone": new_user.phone,
            "role": new_user.role.value,
            "area": new_user.area,
            "avenue": new_user.avenue,
            "road": new_user.road,
            "house": new_user.house,
            "flat": new_user.flat,
            "verified": new_user.verified,
            "permissions": new_user.permissions,
            "profile_image": new_user.profile_image,
            "createdAt": new_user.createdAt,
            "createdBy": new_user.createdBy
        }
    }


def get_deliveryman_by_area(area: str, db: Session):
    try:
        deliverymen = (
            db.query(User)
            .filter(User.role == Role.DELIVERYMAN, User.area == area)
            .all()
        )

        return {
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": "Deliverymen retrieved successfully.",
            "data": [
                {
                    "id": u.id,
                    "name": u.name,
                    "phone": u.phone,
                    "role": u.role.value,
                    "area": u.area,
                    "avenue": u.avenue,
                    "road": u.road,
                    "house": u.house,
                    "flat": u.flat,
                    "verified": u.verified,
                    "profile_image": u.profile_image
                }
                for u in deliverymen
            ]
        }
    except Exception:
        db.rollback()
        raise