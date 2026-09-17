from datetime import date, datetime
import re

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import get_db
from .models import Medicine, Batch
from .auth import get_current_user


router = APIRouter(
    prefix="/api/import",
    tags=["Import"],
    dependencies=[Depends(get_current_user)]
)


class ImportRequest(BaseModel):
    medicine_id: int
    rows: list[dict]


def parse_quantity(value):
    """
    Accept:
    10
    "10"
    "10 units"
    " 10 units "
    """

    if value is None:
        return None

    if isinstance(value, int):
        return value if value > 0 else None

    if isinstance(value, float):
        return int(value) if value > 0 else None

    text = str(value).strip()

    match = re.fullmatch(
        r"(\d+)\s*(?:units?)?",
        text,
        re.IGNORECASE
    )

    if not match:
        return None

    quantity = int(match.group(1))

    return quantity if quantity > 0 else None


def parse_expiry(value):
    """
    Accept:
    YYYY-MM-DD
    DD/MM/YYYY
    """

    if value is None:
        return None

    if isinstance(value, date):
        return value

    text = str(value).strip()

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y"
    ]

    for fmt in formats:

        try:
            return datetime.strptime(
                text,
                fmt
            ).date()

        except ValueError:
            continue

    return None


@router.post("/batches")
def import_batches(
    data: ImportRequest,
    db: Session = Depends(get_db)
):

    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == data.medicine_id)
        .first()
    )

    if not medicine:
        return {
            "imported": 0,
            "deduped": 0,
            "rejected": len(data.rows),
            "errors": [
                {
                    "row": None,
                    "reason": "Medicine not found"
                }
            ]
        }

    imported = 0
    deduped = 0
    rejected = 0

    errors = []

    # Track duplicates inside this import
    seen = set()

    for index, row in enumerate(data.rows, start=1):

        # --------------------------------
        # READ VALUES
        # --------------------------------

        batch_number = row.get("batch_number")
        quantity = parse_quantity(
            row.get("quantity")
        )
        expiry_date = parse_expiry(
            row.get("expiry_date")
        )

        # --------------------------------
        # REQUIRED FIELD VALIDATION
        # --------------------------------

        if not batch_number:
            rejected += 1

            errors.append({
                "row": index,
                "reason": "Missing batch_number"
            })

            continue

        batch_number = str(
            batch_number
        ).strip()

        if quantity is None:
            rejected += 1

            errors.append({
                "row": index,
                "reason": "Invalid quantity"
            })

            continue

        if expiry_date is None:
            rejected += 1

            errors.append({
                "row": index,
                "reason": "Invalid expiry_date"
            })

            continue

        # --------------------------------
        # DUPLICATE DETECTION
        # --------------------------------

        duplicate_key = (
            data.medicine_id,
            batch_number,
            expiry_date
        )

        if duplicate_key in seen:

            deduped += 1

            continue

        seen.add(duplicate_key)

        # --------------------------------
        # CHECK DATABASE
        # --------------------------------

        existing_batch = (
            db.query(Batch)
            .filter(
                Batch.medicine_id == data.medicine_id,
                Batch.batch_number == batch_number,
                Batch.expiry_date == expiry_date
            )
            .first()
        )

        if existing_batch:

            deduped += 1

            continue

        # --------------------------------
        # CREATE BATCH
        # --------------------------------

        batch = Batch(
            medicine_id=data.medicine_id,
            batch_number=batch_number,
            quantity=quantity,
            expiry_date=expiry_date,
            status="active",
            flagged_for_expiry=0
        )

        db.add(batch)

        imported += 1

    db.commit()

    return {
        "medicine": medicine.name,
        "imported": imported,
        "deduped": deduped,
        "rejected": rejected,
        "errors": errors
    }