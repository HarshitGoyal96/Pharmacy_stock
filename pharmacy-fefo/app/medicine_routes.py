from datetime import date

from fastapi import APIRouter, Depends, HTTPException,Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import get_db
from .models import Medicine, Batch


router = APIRouter(
    prefix="/api/medicines",
    tags=["Medicines"]
)


# -------------------------
# Request schemas
# -------------------------

class MedicineCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    generic_name: str | None = None
    manufacturer: str | None = None


class BatchCreate(BaseModel):
    batch_number: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    expiry_date: date


# -------------------------
# Add medicine
# -------------------------

@router.post("/")
def create_medicine(
    data: MedicineCreate,
    db: Session = Depends(get_db)
):

    medicine = Medicine(
        name=data.name,
        generic_name=data.generic_name,
        manufacturer=data.manufacturer
    )

    db.add(medicine)
    db.commit()
    db.refresh(medicine)

    return {
        "message": "Medicine created successfully",
        "medicine": {
            "id": medicine.id,
            "name": medicine.name,
            "generic_name": medicine.generic_name,
            "manufacturer": medicine.manufacturer
        }
    }


# -------------------------
# Add batch
# -------------------------

@router.post("/{medicine_id}/batches")
def create_batch(
    medicine_id: int,
    data: BatchCreate,
    db: Session = Depends(get_db)
):

    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == medicine_id)
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    batch = Batch(
        medicine_id=medicine_id,
        batch_number=data.batch_number,
        quantity=data.quantity,
        expiry_date=data.expiry_date
    )

    db.add(batch)
    db.commit()
    db.refresh(batch)

    return {
        "message": "Batch added successfully",
        "batch": {
            "id": batch.id,
            "medicine_id": batch.medicine_id,
            "batch_number": batch.batch_number,
            "quantity": batch.quantity,
            "expiry_date": batch.expiry_date
        }
    }


# -------------------------
# Get all batches
# -------------------------

@router.get("/{medicine_id}/batches")
def get_batches(
    medicine_id: int,
    db: Session = Depends(get_db)
):

    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == medicine_id)
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    batches = (
        db.query(Batch)
        .filter(Batch.medicine_id == medicine_id)
        .order_by(Batch.expiry_date.asc())
        .all()
    )

    return {
        "medicine": medicine.name,
        "batches": [
            {
                "id": batch.id,
                "batch_number": batch.batch_number,
                "quantity": batch.quantity,
                "expiry_date": batch.expiry_date,
                "expired": batch.expiry_date < date.today()
            }
            for batch in batches
        ]
    }


# -------------------------
# Get sellable stock
# -------------------------

@router.get("/{medicine_id}/stock")
def get_sellable_stock(
    medicine_id: int,
    db: Session = Depends(get_db)
):

    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == medicine_id)
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    today = date.today()

    valid_batches = (
        db.query(Batch)
        .filter(
            Batch.medicine_id == medicine_id,
            Batch.quantity > 0,
            Batch.expiry_date >= today
        )
        .all()
    )

    sellable_stock = sum(
        batch.quantity
        for batch in valid_batches
    )

    return {
        "medicine_id": medicine.id,
        "medicine": medicine.name,
        "sellable_stock": sellable_stock,
        "as_of": today,
        "valid_batches": len(valid_batches)
    }
# -------------------------
# FEFO Dispensing
# -------------------------

class DispenseRequest(BaseModel):
    quantity: int = Field(gt=0)


@router.post("/{medicine_id}/dispense")
def dispense_medicine(
    medicine_id: int,
    data: DispenseRequest,
    db: Session = Depends(get_db)
):

    # Check that medicine exists
    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == medicine_id)
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    today = date.today()

    # Get ONLY valid, non-expired batches.
    # Earliest expiry comes first.
    valid_batches = (
        db.query(Batch)
        .filter(
            Batch.medicine_id == medicine_id,
            Batch.quantity > 0,
            Batch.expiry_date >= today
        )
        .order_by(Batch.expiry_date.asc(), Batch.id.asc())
        .all()
    )

    available_stock = sum(
        batch.quantity
        for batch in valid_batches
    )

    # Do not partially dispense if there is
    # not enough valid stock.
    if data.quantity > available_stock:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Insufficient sellable stock",
                "requested": data.quantity,
                "available": available_stock
            }
        )

    remaining = data.quantity
    dispensed_from = []

    # Consume earliest-expiring valid batches first.
    for batch in valid_batches:

        if remaining == 0:
            break

        quantity_taken = min(
            batch.quantity,
            remaining
        )

        batch.quantity -= quantity_taken
        remaining -= quantity_taken

        dispensed_from.append({
            "batch_id": batch.id,
            "batch_number": batch.batch_number,
            "expiry_date": batch.expiry_date,
            "quantity_dispensed": quantity_taken,
            "remaining_in_batch": batch.quantity
        })

    # Commit all changes together.
    db.commit()

    return {
        "message": "Medicine dispensed successfully",
        "medicine": medicine.name,
        "quantity_dispensed": data.quantity,
        "dispensed_from": dispensed_from
    }

@router.get("/")
def get_medicines(
    search: str | None = Query(
        default=None,
        description="Search medicine by name"
    ),
    page: int = Query(
        default=1,
        ge=1
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100
    ),
    sort_by: str = Query(
        default="name"
    ),
    order: str = Query(
        default="asc"
    ),
    db: Session = Depends(get_db)
):

    today = date.today()

    # -------------------------
    # Search
    # -------------------------

    query = (
        db.query(
            Medicine,
            func.coalesce(
                func.sum(
                    Batch.quantity
                ).filter(
                    Batch.quantity > 0,
                    Batch.expiry_date >= today
                ),
                0
            ).label("sellable_stock")
        )
        .outerjoin(
            Batch,
            Medicine.id == Batch.medicine_id
        )
        .group_by(Medicine.id)
    )

    if search:
        query = query.filter(
            Medicine.name.ilike(f"%{search}%")
        )

    # -------------------------
    # Sorting
    # -------------------------

    if sort_by == "stock":
        sort_column = func.coalesce(
            func.sum(
                Batch.quantity
            ).filter(
                Batch.quantity > 0,
                Batch.expiry_date >= today
            ),
            0
        )
    else:
        sort_column = Medicine.name

    if order.lower() == "desc":
        query = query.order_by(
            sort_column.desc()
        )
    else:
        query = query.order_by(
            sort_column.asc()
        )

    # -------------------------
    # Total count
    # -------------------------

    total = query.count()

    # -------------------------
    # Pagination
    # -------------------------

    offset = (page - 1) * page_size

    medicines = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total_pages = (
        (total + page_size - 1)
        // page_size
    )

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "medicines": [
            {
                "id": medicine.id,
                "name": medicine.name,
                "generic_name": medicine.generic_name,
                "manufacturer": medicine.manufacturer,
                "sellable_stock": int(sellable_stock or 0)
            }
            for medicine, sellable_stock in medicines
        ]
    }