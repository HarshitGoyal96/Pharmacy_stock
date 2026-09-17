from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

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

