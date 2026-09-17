from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import OutboxMessage
from .auth import get_current_user


router = APIRouter(
    prefix="/outbox",
    tags=["Notification Service"],
    dependencies=[Depends(get_current_user)]
)


@router.get("")
def get_outbox(
    db: Session = Depends(get_db)
):

    messages = (
        db.query(OutboxMessage)
        .order_by(
            OutboxMessage.created_at.desc()
        )
        .all()
    )

    return {
        "count": len(messages),
        "messages": [
            {
                "id": message.id,
                "event_type": message.event_type,
                "medicine_id": message.medicine_id,
                "message": message.message,
                "created_at": message.created_at
            }
            for message in messages
        ]
    }