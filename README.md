# 📍 Location-Based Prospect Qualification System

This project implements a location-based prospect qualification system that evaluates whether prospects meet users' location preferences. It reads input data from CSV and JSON files, processes it using custom matching logic, and stores the results in a PostgreSQL database.

---

## 🛠 Technologies Used

* Python 3.9+
* [Poetry](https://python-poetry.org/)
* PostgreSQL
* Docker & Docker Compose
* pytest

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nadavedri/ProspectGeo.git
cd ProspectGeo
```

### 2. Install Dependencies with Poetry

Make sure you have Poetry installed (via [pipx](https://pypa.github.io/pipx/)):

```bash
pipx install poetry
```

Install project dependencies:

```bash
poetry install
```

### 3. Configure and Launch PostgreSQL with Docker Compose

1. Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

2. Launch the PostgreSQL and app containers:

```bash
docker-compose up -d
```

> ⏳ **Note**: The application waits 10 seconds for the database to become ready.

---

## ▶️ Running the Application Locally

Ensure your input files are placed in the `src/prospectgeo/data/` directory:

* `prospects.csv`
* `country-to-regions-mapping.json`
* `users-locations-settings.json`

Update the `POSTGRES_HOST` value in your `.env` file to `localhost`:

```bash
poetry run prospectgeo
```

---

## 🧠 Matching Logic

A prospect qualifies if:

* Their `company_country` or (if in the US) `company_state` is:

  * Directly listed in the user's `location_include`, **or**
  * Mapped to a region listed in `location_include`
* And **not** present in the user's `location_exclude`

---

## 🧪 Running Tests

To verify that everything works correctly:

```bash
poetry run pytest
```

---

## 🧹 Development Tools

* **Linting**:

  ```bash
  poetry run ruff check
  ```

* **Formatting**:

  ```bash
  poetry run ruff format
  ```

