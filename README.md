# Clinical Data Engineering Demo

This project demonstrates scalable, production-grade data engineering skills using Python and PostgreSQL, aligned with the Senior Manager, Data Engineering job requirements.

## Structure
- `etl/` — ETL scripts for ingesting, transforming, and loading data
- `data/` — Sample clinical data files
- `docs/` — Documentation and references

## Features
- Ingests and transforms sample clinical data
- Loads data into a PostgreSQL database using a simplified OMOP CDM schema
- Includes data validation and quality checks

## Requirements
- Python 3.8+
- PostgreSQL (local or cloud instance)
- Python packages: pandas, SQLAlchemy, psycopg2

## Setup
1. Install PostgreSQL and create a database (e.g., `clinical_demo`).
2. Install Python dependencies:
   ```bash
   pip install pandas sqlalchemy psycopg2-binary
   ```
3. Update database connection settings in `etl/etl_load.py`.
4. Run the ETL script:
   ```bash
   python etl/etl_load.py
   ```

## How this aligns with the job description
- Demonstrates scalable data pipeline design (ETL)
- Uses OMOP CDM concepts for healthcare data
- Implements data validation and quality checks
- Prepares data for analytics and research
- Uses production-grade tools (PostgreSQL, Python)

---

For more details, see the scripts and documentation in each folder.
