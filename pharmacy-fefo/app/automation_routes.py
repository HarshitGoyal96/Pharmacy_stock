from datetime import date, timedelta

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import get_db
from .models import Batch


router = APIRouter(
    tags=["Automation"]
)


class ClockRequest(BaseModel):
    date: date


@router.post("/clock")
def run_daily_job(
    data: ClockRequest,
    db: Session = Depends(get_db)
):
    current_date = data.date

    expiry_limit = current_date + timedelta(days=7)

    batches = (
        db.query(Batch)
        .all()
    )

    quarantined_count = 0
    flagged_count = 0

    for batch in batches:

        # Already quarantined batches are ignored
        if batch.status == "quarantined":
            continue

        # -------------------------
        # EXPIRED
        # -------------------------

        if batch.expiry_date < current_date:

            if batch.quantity > 0:
                quarantined_count += 1

            batch.status = "quarantined"

            continue

        # -------------------------
        # EXPIRING WITHIN 7 DAYS
        # -------------------------

        if (
            current_date
            <= batch.expiry_date
            <= expiry_limit
            and batch.quantity > 0
        ):

            if batch.flagged_for_expiry == 0:
                flagged_count += 1

            batch.flagged_for_expiry = 1

    db.commit()

    return {
        "message": "Daily inventory job completed",
        "run_date": current_date,
        "quarantined": quarantined_count,
        "flagged_for_expiry": flagged_count
    }