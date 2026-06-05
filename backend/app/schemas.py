"""Pydantic schemas defining the API request/response contracts.

Validation here satisfies functional requirement FR-03: reject empty submissions
and excessively long descriptions before they ever reach the database.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .models import TicketStatus

# Description length bounds (FR-03). A min length blocks empty/whitespace-only
# submissions; the max length blocks abusive or accidental oversized input.
DESCRIPTION_MIN_LENGTH = 5
DESCRIPTION_MAX_LENGTH = 500


class EquipmentRead(BaseModel):
    """Equipment as returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    location: str


class TicketCreate(BaseModel):
    """Payload for creating a new maintenance ticket."""

    equipment_id: int
    description: str = Field(
        ..., min_length=DESCRIPTION_MIN_LENGTH, max_length=DESCRIPTION_MAX_LENGTH
    )


class TicketStatusUpdate(BaseModel):
    """Payload for an administrator updating a ticket's status."""

    status: TicketStatus


class TicketRead(BaseModel):
    """Ticket as returned to the client, including its related equipment."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    equipment_id: int
    description: str
    status: TicketStatus
    created_at: datetime
    equipment: EquipmentRead
