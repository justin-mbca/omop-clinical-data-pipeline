import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import os

# Update these settings for your PostgreSQL instance
DB_USER = os.getenv('DB_USER', 'clinical_user')
DB_PASS = os.getenv('DB_PASS', 'StrongPassword123')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'clinical_demo')

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


# Load OMOP CDM schema using absolute path
schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs', 'omop_cdm_schema.sql')
with open(schema_path, 'r', encoding='utf-8') as f:
    schema_sql = f.read()

with engine.connect() as conn:
    for stmt in schema_sql.strip().split(';'):
        if stmt.strip():
            conn.execute(sqlalchemy.text(stmt))


# Load sample data using absolute paths
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
person_df = pd.read_csv(os.path.join(data_dir, 'person_sample.csv'))
observation_df = pd.read_csv(os.path.join(data_dir, 'observation_sample.csv'))

# Data validation example: check for missing person_id
assert person_df['person_id'].notnull().all(), "Missing person_id in person data"
assert observation_df['person_id'].notnull().all(), "Missing person_id in observation data"

# Load data into database
person_df.to_sql('person', engine, if_exists='append', index=False)
observation_df.to_sql('observation', engine, if_exists='append', index=False)

print("ETL process completed successfully.")
