from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.core.db import get_db
from sqlalchemy.orm import Session
from app.utils.token_service import get_current_user
from .schema import CreateProduct, UpdateProduct

from .service import (
    get_product_list,
    create_new_product,
    get_product_by_id,
    get_products_by_category,
    update_product,
    delete_product,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/list")
def product_list(
    page: Optional[int] = Query(None, ge=1),
    limit: Optional[int] = Query(None, ge=1),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_product_list(db, page=page, limit=limit)


@router.post("/create")
def store_product(req: CreateProduct, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_new_product(req, current_user["id"], db)


@router.get("/{id}")
def product_by_id(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_product_by_id(id, db)


@router.get("/category/{category_id}")
def products_by_category(category_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_products_by_category(category_id, db)


@router.put("/{id}")
def product_update(id: int, req: UpdateProduct, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return update_product(id, req, current_user["id"], db)


@router.delete("/{id}")
def product_delete(id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_product(id, db)
