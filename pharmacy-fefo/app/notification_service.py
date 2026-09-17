from datetime import datetime

from sqlalchemy.orm import Session

from .models import Medicine, OutboxMessage


class NotificationService:

    @staticmethod
    def send_reorder_alert(
        db: Session,
        medicine: Medicine,
        current_stock: int
    ):

        message = (
            f"Re-order alert: {medicine.name} "
            f"sellable stock is {current_stock}, "
            f"below threshold {medicine.reorder_threshold}."
        )

        notification = OutboxMessage(
            event_type="REORDER_ALERT",
            medicine_id=medicine.id,
            message=message,
            created_at=datetime.utcnow()
        )

        db.add(notification)

        return notification