"""FastAPI application: the Application Layer from the Phase 1 building-block diagram.

Exposes the REST endpoints that the React frontend consumes. Each route maps to a
functional requirement (FR-xx) defined in the project documentation.
"""
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

# Create tables on startup (sufficient for an SQLite MVP; no migration tool needed).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Local Gym Equipment Issue Reporter",
    description="Report and track maintenance issues for gym equipment.",
    version="1.0.0",
)

# Allow the React dev server and any deployed frontend to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Simple liveness probe used by Docker/host health checks."""
    return {"status": "ok"}


@app.get("/equipment", response_model=list[schemas.EquipmentRead], tags=["equipment"])
def list_equipment(db: Session = Depends(get_db)) -> list[models.Equipment]:
    """FR-01: return the list of available gym equipment."""
    return list(db.scalars(select(models.Equipment).order_by(models.Equipment.name)))


@app.get("/tickets", response_model=list[schemas.TicketRead], tags=["tickets"])
def list_tickets(db: Session = Depends(get_db)) -> list[models.Ticket]:
    """FR-04: return all tickets (newest first) for the administrator dashboard."""
    return list(db.scalars(select(models.Ticket).order_by(models.Ticket.created_at.desc())))


@app.post(
    "/tickets",
    response_model=schemas.TicketRead,
    status_code=status.HTTP_201_CREATED,
    tags=["tickets"],
)
def create_ticket(
    payload: schemas.TicketCreate, db: Session = Depends(get_db)
) -> models.Ticket:
    """FR-02/FR-03: create a validated maintenance ticket for a known equipment item."""
    equipment = db.get(models.Equipment, payload.equipment_id)
    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )

    ticket = models.Ticket(
        equipment_id=payload.equipment_id, description=payload.description.strip()
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@app.patch(
    "/tickets/{ticket_id}", response_model=schemas.TicketRead, tags=["tickets"]
)
def update_ticket_status(
    ticket_id: int,
    payload: schemas.TicketStatusUpdate,
    db: Session = Depends(get_db),
) -> models.Ticket:
    """FR-05: administrator updates a ticket's status (Open / In Progress / Resolved)."""
    ticket = db.get(models.Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
        )

    ticket.status = payload.status
    db.commit()
    db.refresh(ticket)
    return ticket
