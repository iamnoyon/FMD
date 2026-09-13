from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .model import Product
from .schema import CreateProduct, UpdateProduct


def get_product_list(db: Session):
    try:
        products = db.query(Product).filter(Product.status == True).all()
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


def get_products_by_category(category_id: int, db: Session):
    try:
        products = db.query(Product).filter(
            Product.categoryId == category_id,
            Product.status == True
        ).all()
        return {
            "success": True,
            "message": "Products retrieved by category!",
            "data": products
        }
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
