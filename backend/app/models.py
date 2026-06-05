"""ORM models for the two core entities: Equipment and Ticket.

These map directly to the Data Access Layer described in the Phase 1 building-block
diagram. The relationship is one-to-many: one piece of Equipment can have many Tickets.
"""
from datetime import datetime, timezone
import enum

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class TicketStatus(str, enum.Enum):
    """Allowed lifecycle states for a maintenance ticket."""

    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"


class Equipment(Base):
    """A single piece of gym equipment that members can report issues against."""

    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="equipment")


class Ticket(Base):
    """A maintenance ticket reported against a piece of equipment."""

    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    equipment: Mapped["Equipment"] = relationship(back_populates="tickets")
