-- Simplified OMOP CDM Person table
CREATE TABLE IF NOT EXISTS person (
    person_id SERIAL PRIMARY KEY,
    gender_concept_id INTEGER,
    year_of_birth INTEGER,
    month_of_birth INTEGER,
    day_of_birth INTEGER,
    race_concept_id INTEGER,
    ethnicity_concept_id INTEGER
);

-- Simplified OMOP CDM Observation table
CREATE TABLE IF NOT EXISTS observation (
    observation_id SERIAL PRIMARY KEY,
    person_id INTEGER REFERENCES person(person_id),
    observation_concept_id INTEGER,
    observation_date DATE,
    value_as_number FLOAT,
    value_as_string TEXT
);
