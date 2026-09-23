from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from .model import Categories

def get_category_list(db: Session, page: int = None, limit: int = None):
    try:
        query = db.query(Categories).filter(Categories.status == True)

        if page is not None and limit is not None:
            total = query.count()
            offset = (page - 1) * limit
            categories = query.offset(offset).limit(limit).all()
            return {
                "success": True,
                "message": "Categories are retrived successfully!",
                "data": categories,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "total_pages": (total + limit - 1) // limit
                }
            }

        categories = query.all()
        return {
            "success": True,
            "message": "Categories are retrived successfully!",
            "data": categories
        }

    except Exception:
        db.rollback()
        raise 



def create_new_category(req, db: Session):
    try:
        new_category = Categories(
            name = req.name,
            image = req.image,
            icon = req.icon,
            status = req.status if req.status is not None else True
        )

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

    except Exception:
        db.rollback()
        raise 

    return {
        "success": True,
        "message": 'Product Category is created successfully!',
        "data": new_category
    }


def get_category_by_id(id, db: Session):
    catId = int(id)
    category = db.query(Categories).filter(Categories.id == catId).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )

    return {
        "success": True,
        "message": "Retrive category by id",
        "data": category
    }


def update_category_by_id(id, req, db: Session):
    catId = int(id)
    category = db.query(Categories).filter(Categories.id == catId).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'Category not found'
        )

    if req.name is not None:
        category.name = req.name
    if req.image is not None:
        category.image = req.image
    if req.icon is not None:
        category.icon = req.icon
    if req.status is not None:
        category.status = req.status

    db.commit()
    db.refresh(category)

    return {
        "success": True,
        "message": "Category updated successfully!",
        "data": category
    }


def delete_category_by_id(id, db: Session):
    catId = int(id)

    category = (
        db.query(Categories)
        .filter(Categories.id == catId)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()

    return {
        "success": True,
        "message": "Category deleted successfully"
    }

    
