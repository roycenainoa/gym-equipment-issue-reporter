# Local Gym Equipment Issue Reporter

A web application that lets gym members report broken or faulty equipment and lets
facility managers track and resolve those reports. Built for the DLMCSPSE01 portfolio.

- **Frontend:** React + Tailwind CSS (Vite)
- **Backend:** Python + FastAPI
- **Database:** SQLite (via SQLAlchemy ORM)
- **Containerization:** Docker + docker-compose

---

## Quick start (Docker — recommended)

Requires Docker. From the project root:

```bash
docker compose up --build
```

Then open:

- **App (frontend):** http://localhost:8081
- **API docs (Swagger):** http://localhost:8000/docs

The database is seeded automatically with realistic equipment and sample tickets on
first start.

---

## Running locally without Docker

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Python 3.12 or 3.13
pip install -r requirements.txt
python -m app.seed            # load realistic demo data
uvicorn app.main:app --reload # http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                   # http://localhost:5173
```

The frontend reads the backend URL from `VITE_API_URL` (defaults to
`http://localhost:8000`).

---

## Running the tests

```bash
cd backend
source .venv/bin/activate
python -m pytest
```

---

## Project structure

```
gym-equipment-reporter/
├── backend/          FastAPI application, ORM models, tests
│   ├── app/          database, models, schemas, routes, seed data
│   └── tests/        pytest API tests
├── frontend/         React + Tailwind single-page app
│   └── src/          components, API client
└── docker-compose.yml
```

## Usage

- **Report an Issue** tab — members pick a machine and describe the problem.
- **Admin Dashboard** tab — managers see every ticket and change its status
  (Open → In Progress → Resolved).
