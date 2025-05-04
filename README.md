
# Location-Based Prospect Qualification System

This project implements a location-based prospect qualification system that evaluates whether prospects meet users’ location preferences. It reads input data from CSV and JSON files, processes it using a custom matching logic, and stores the results in a PostgreSQL database.

---

## 🛠 Technologies Used

- Python 3.9+
- [Poetry](https://python-poetry.org/)
- PostgreSQL
- Docker
- pytest

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nadavedri/ProspectGeo.git
cd ProspectGeo
```

### 2. Install Dependencies with Poetry
install Petry with pipx
```bash
pipx install poetry
```
install dependencies
```bash
poetry install
```

### 3. Set Up PostgreSQL with dockerfile or docker-compose


**dockerfile**

```bash
docker build -t postgres-container:latest .
docker run --env-file .env --name prospectgeo-postgres -p 5432:5432 postgres-container:latest
```

---

## ▶️ Running the Application

Make sure your input files are placed in the `data/` directory in `src/prospectgeo`:

- `prospects.csv`
- `country-to-regions-mapping.json`
- `users-locations-settings.json`

run local:

```bash
poetry run prospectgeo
```

Run remote:

```bash
ddocker-compose up -d
```


---

## 🧠 Matching Logic

A prospect qualifies if:

- Their `company_country` or `company_state` (if in the US) is:
  - Directly listed in the user's `location_include`, or
  - Mapped to a region listed in `location_include`,
- And it is **not** listed in the user's `location_exclude`.

---

## 🧪 Run Tests

To ensure everything works as expected:
```bash
poetry run pytest
```

## Development
- Linting: `poetry run ruff check`
- Formatting: `poetry run ruff format`


