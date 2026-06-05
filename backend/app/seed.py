"""Seed the database with realistic gym equipment and sample tickets.

Run with:  python -m app.seed
This provides the "sensible (test) data, no dummy text" required by the assignment
so the application is immediately usable and its value is tangible on first launch.
"""
from .database import Base, SessionLocal, engine
from .models import Equipment, Ticket, TicketStatus

EQUIPMENT = [
    {"name": "Treadmill #1", "category": "Cardio", "location": "Cardio Zone - Row A"},
    {"name": "Treadmill #2", "category": "Cardio", "location": "Cardio Zone - Row A"},
    {"name": "Concept2 Rowing Machine", "category": "Cardio", "location": "Cardio Zone - Row B"},
    {"name": "Assault Air Bike", "category": "Cardio", "location": "Functional Area"},
    {"name": "Leg Press Machine", "category": "Strength", "location": "Strength Floor - North"},
    {"name": "Lat Pulldown Machine", "category": "Strength", "location": "Strength Floor - North"},
    {"name": "Smith Machine", "category": "Strength", "location": "Strength Floor - South"},
    {"name": "Adjustable Bench #3", "category": "Free Weights", "location": "Free Weights Area"},
    {"name": "Olympic Barbell Set", "category": "Free Weights", "location": "Free Weights Area"},
    {"name": "Cable Crossover Machine", "category": "Strength", "location": "Strength Floor - South"},
]

# Sample tickets reference equipment by list index (resolved to real IDs after insert).
SAMPLE_TICKETS = [
    {"equipment_index": 0, "description": "Belt slips intermittently when running above 10 km/h.", "status": TicketStatus.OPEN},
    {"equipment_index": 4, "description": "Weight pin is bent and gets stuck on the 80 kg plate.", "status": TicketStatus.IN_PROGRESS},
    {"equipment_index": 2, "description": "Display screen flickers and resets mid-session.", "status": TicketStatus.OPEN},
    {"equipment_index": 6, "description": "Safety catch on the left side does not lock properly.", "status": TicketStatus.RESOLVED},
    {"equipment_index": 9, "description": "Lower cable is frayed near the pulley and should be replaced.", "status": TicketStatus.OPEN},
]


def seed() -> None:
    """Reset the schema and load the realistic demo dataset."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        equipment_rows = [Equipment(**item) for item in EQUIPMENT]
        db.add_all(equipment_rows)
        db.flush()  # assign primary keys without committing yet

        for t in SAMPLE_TICKETS:
            db.add(
                Ticket(
                    equipment_id=equipment_rows[t["equipment_index"]].id,
                    description=t["description"],
                    status=t["status"],
                )
            )
        db.commit()
        print(f"Seeded {len(equipment_rows)} equipment items and {len(SAMPLE_TICKETS)} tickets.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
