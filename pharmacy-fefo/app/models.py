from datetime import date, datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False,
        index=True
    )

    generic_name = Column(
        String(150),
        nullable=True
    )

    manufacturer = Column(
        String(150),
        nullable=True
    )

    reorder_threshold = Column(
        Integer,
        nullable=False,
        default=10
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    batches = relationship(
        "Batch",
        back_populates="medicine",
        cascade="all, delete-orphan"
    )

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)

    medicine_id = Column(
        Integer,
        ForeignKey("medicines.id"),
        nullable=False,
        index=True
    )

    batch_number = Column(
        String(100),
        nullable=False,
        index=True
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    expiry_date = Column(
        Date,
        nullable=False,
        index=True
    )

    status = Column(
        String(20),
        nullable=False,
        default="active"
    )

    flagged_for_expiry = Column(
        Integer,
        nullable=False,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    medicine = relationship(
        "Medicine",
        back_populates="batches"
    )
class OutboxMessage(Base):
    __tablename__ = "outbox"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    event_type = Column(
        String(50),
        nullable=False
    )

    medicine_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    message = Column(
        String(500),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )