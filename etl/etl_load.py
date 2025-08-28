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

# --- Terminology Mapping Example ---
# Load mapping table (source_code to standard_concept_id)
mapping_path = os.path.join(data_dir, 'code_mapping_sample.csv')
if os.path.exists(mapping_path):
    mapping_df = pd.read_csv(mapping_path)
    # Example: map observation_concept_id if it's a source code (simulate real mapping)
    obs_map = dict(zip(mapping_df['source_code'], mapping_df['standard_concept_id']))
    # If observation_concept_id is not numeric, map it
    def map_concept_id(val):
        try:
            return int(val)
        except:
            return int(obs_map[val]) if val in obs_map else None
    observation_df['observation_concept_id'] = observation_df['observation_concept_id'].apply(map_concept_id)

# --- Automated Data Quality Checks ---
errors = []
# Check for missing person_id
if not person_df['person_id'].notnull().all():
    errors.append("Missing person_id in person data")
if not observation_df['person_id'].notnull().all():
    errors.append("Missing person_id in observation data")
# Check for duplicate person_id
if person_df['person_id'].duplicated().any():
    errors.append("Duplicate person_id found in person data")
# Check for out-of-range year_of_birth (future years)
from datetime import datetime
current_year = datetime.now().year
if (person_df['year_of_birth'] > current_year).any():
    errors.append("year_of_birth in the future found in person data")
# Check for referential integrity: all observation person_ids exist in person
if not observation_df['person_id'].isin(person_df['person_id']).all():
    errors.append("Observation references person_id not in person table")
# Check for unmapped observation_concept_id
if observation_df['observation_concept_id'].isnull().any():
    errors.append("Unmapped observation_concept_id found in observation data")

if errors:
    print("Data Quality Issues Found:")
    for err in errors:
        print(f"- {err}")
    raise ValueError("Data quality checks failed. See errors above.")

# Load data into database
person_df.to_sql('person', engine, if_exists='append', index=False)
observation_df.to_sql('observation', engine, if_exists='append', index=False)

print("ETL process completed successfully.")
