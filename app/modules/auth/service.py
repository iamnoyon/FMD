from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.user.model import User, Role
from app.modules.otp.model import OTP
from app.utils.permission import Permissions
from app.utils.otp_service import create_otp_record, verify_otp
from app.utils.token_service import create_token


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

        # Mark all previous OTPs as verified
        db.query(OTP).filter(
            OTP.phone == req.phone,
            OTP.verified == False
        ).update(
            {
                "verified": True
            },
            synchronize_session=False
        )

        # Generate new OTP
        new_otp_record, plan_otp = create_otp_record(req.phone)

        db.add(new_otp_record)
        db.commit()
        db.refresh(new_user)
        db.refresh(new_otp_record)

        # For development only
        print("New OTP:", plan_otp)

        return {
            "success": True,
            "status_code": status.HTTP_201_CREATED,
            "message": "User registered successfully. OTP sent to your number.",
            "data": new_user
        }

    except Exception:
        db.rollback()
        raise



def user_login(req, db: Session):
    user = db.query(User).filter(User.phone == req.phone).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )
    
    result = otp_verify(req, db)

    if result:
        user.verified = True
        db.commit()
        # Token
        token = create_token(user.id, user.phone, user.role, user.permissions)
        return token

    return None



def resend_otp(req, db: Session):
    existing_user = db.query(User).filter(User.phone == req.phone).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found with this phone number. Please register first!'
        )

    
    new_otp_record, plan_otp = create_otp_record(req.phone)
    db.add(new_otp_record)
    db.commit()
    db.refresh(new_otp_record)

    print('Registerd User OTP: ', plan_otp)

    return {
        "success": True,
        "status_code": 201,
        "message": "OTP sent to your number"
    }



def get_user_details(current_user, db: Session):
    user_id = int(current_user['id'])
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "data": {
            "id": user.id,
            "name": user.name,
            "phone": user.phone,
            "role": user.role.value,
            "area": user.area,
            "avenue": user.avenue,
            "road": user.road,
            "house": user.house,
            "flat": user.flat,
            "verified": user.verified,
            "permissions": user.permissions
        }
    }



################################ Verify OTP ###################################
def otp_verify(req, db: Session):
    otp_record = (
        db.query(OTP)
        .filter(
            OTP.phone == req.phone,
            OTP.verified.is_(False)
        )
        .order_by(OTP.id.desc())
        .first()
    )

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pending OTP found."
        )

    expire_at = otp_record.expire_at

    # Convert DB datetime to UTC-aware datetime
    if expire_at.tzinfo is None:
        expire_at = expire_at.replace(tzinfo=timezone.utc)
    else:
        expire_at = expire_at.astimezone(timezone.utc)

    current_time = datetime.now(timezone.utc)

    # IMPORTANT: compare expire_at, NOT otp_record.expire_at
    if current_time >= expire_at:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="OTP has expired."
        )

    if not verify_otp(req.otp, otp_record.otp_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP."
        )

    otp_record.verified = True
    db.commit()

    return True