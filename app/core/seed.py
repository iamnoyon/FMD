from datetime import datetime
from app.core.db import localSession
from app.modules.user.model import User
from app.utils.permission import Permissions
from app.modules.user.model import Role, AreaEnum


def seed_superadmin():
    db = localSession()
    exsiting_user = db.query(User).filter(User.phone == '00000000000').first()

    if not exsiting_user:
        user = User(
            name = 'Super Admin',
            phone = '00000000000',
            role = Role.SUPERADMIN,
            area = AreaEnum.MIRPURDOSH,
            avenue = 'A',
            road = '10',
            house = '1200',
            flat = 'B5',
            verified = True,
            permissions = [p.value for p in Permissions],
            createdAt = datetime.utcnow(),
            createdBy = 'system',
        )

        db.add(user)
        db.commit()
    db.close()