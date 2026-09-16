from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .model import Product
from .schema import CreateProduct, UpdateProduct
from app.modules.categories.model import Categories


def get_product_list(db: Session, page: int = None, limit: int = None):
    try:
        query = db.query(Product).filter(Product.status == True)

        if page is not None and limit is not None:
            total = query.count()
            offset = (page - 1) * limit
            products = query.offset(offset).limit(limit).all()
            return {
                "success": True,
                "message": "Products retrieved successfully!",
                "data": products,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "total_pages": (total + limit - 1) // limit
                }
            }

        products = query.all()
        return {
            "success": True,
            "message": "Products retrieved successfully!",
            "data": products
        }
    except Exception:
        db.rollback()
        raise


def create_new_product(req: CreateProduct, created_by: int, db: Session):
    try:
        new_product = Product(
            categoryId=req.categoryId,
            name=req.name,
            description=req.description,
            weight=req.weight,
            weight_type=req.weight_type.value,
            quantity=req.quantity,
            price=req.price,
            image=req.image,
            createdBy=created_by,
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": "Product is created successfully!",
        "data": new_product
    }


def get_product_by_id(id: int, db: Session):
    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return {
        "success": True,
        "message": "Product retrieved by id",
        "data": product
    }


def get_products_by_category(category_id: str, db: Session):
    try:
        query = db.query(Product).filter(Product.status == True)

        category_icon = None

        if str(category_id).upper() != "ALL":
            try:
                cat_id = int(category_id)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid category id. Use an integer or 'ALL'."
                )
            query = query.filter(Product.categoryId == cat_id)

            cat = db.query(Categories.icon).filter(Categories.id == cat_id).first()
            category_icon = cat.icon if cat else None

        products = query.all()

        data = []
        for p in products:
            data.append({
                "id": p.id,
                "categoryId": p.categoryId,
                "name": p.name,
                "description": p.description,
                "weight": p.weight,
                "weight_type": p.weight_type,
                "quantity": p.quantity,
                "price": p.price,
                "image": p.image,
                "status": p.status,
                "createdAt": p.createdAt,
                "createdBy": p.createdBy,
                "updatedAt": p.updatedAt,
                "updatedBy": p.updatedBy,
            })

        return {
            "success": True,
            "message": "Products retrieved by category!",
            "data": data,
            "total": len(data),
            "categoryIcon": category_icon,
        }
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise


def update_product(id: int, req: UpdateProduct, updated_by: int, db: Session):
    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    try:
        if req.categoryId is not None:
            product.categoryId = req.categoryId
        if req.name is not None:
            product.name = req.name
        if req.description is not None:
            product.description = req.description
        if req.weight is not None:
            product.weight = req.weight
        if req.weight_type is not None:
            product.weight_type = req.weight_type.value
        if req.quantity is not None:
            product.quantity = req.quantity
        if req.price is not None:
            product.price = req.price
        if req.image is not None:
            product.image = req.image
        if req.status is not None:
            product.status = req.status

        product.updatedBy = updated_by

        db.commit()
        db.refresh(product)

    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": "Product updated successfully!",
        "data": product
    }


def delete_product(id: int, db: Session):
    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    try:
        db.delete(product)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": "Product deleted successfully!",
    }
