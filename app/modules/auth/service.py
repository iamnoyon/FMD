from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.user.model import User, Role
from app.modules.otp.model import OTP
from app.utils.permission import Permissions
from app.utils.otp_service import (
    hash_otp,
    generate_otp,
    get_otp_expire_time,
)


def user_register(req, db: Session):

    # Check if user already exists
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
        # Create new user
        new_user = User(
            name=req.name,
            phone=req.phone,
            role=Role.CUSTOMER,
            area=req.area,
            avenue=req.avenue,
            road=req.road,
            house=req.house,
            flat=req.flat,
            verified=False,
            permissions=[p.value for p in Permissions],
            createdBy="system",
            createdAt=datetime.now(timezone.utc)
        )
        db.add(new_user)

        # -----------------------------------
        # Mark all previous OTPs as verified
        # -----------------------------------
        db.query(OTP).filter(
            OTP.phone == req.phone,
            OTP.verified == False
        ).update(
            {
                "verified": True
            },
            synchronize_session=False
        )

        # -----------------------------------
        # Generate new OTP
        # -----------------------------------
        otp = generate_otp()
        hashed_otp = hash_otp(otp)
        expire_time = get_otp_expire_time()

        # Create new OTP
        new_otp = OTP(
            phone=req.phone,
            otp_hash=hashed_otp,
            verified=False,
            expire_at=expire_time
        )
        db.add(new_otp)

        # Save user + OTP
        db.commit()
        # Refresh objects
        db.refresh(new_user)
        db.refresh(new_otp)

        # For development only
        print("New OTP:", otp)

        return new_user

    except Exception:
        db.rollback()
        raise