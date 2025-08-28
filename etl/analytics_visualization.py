
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy
import os
import numpy as np

if __name__ == "__main__":
	# Database connection settings
	DB_USER = os.getenv('DB_USER', 'clinical_user')
	DB_PASS = os.getenv('DB_PASS', 'StrongPassword123')
	DB_HOST = os.getenv('DB_HOST', 'localhost')
	DB_PORT = os.getenv('DB_PORT', '5432')
	DB_NAME = os.getenv('DB_NAME', 'clinical_demo')

	DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
	engine = sqlalchemy.create_engine(DATABASE_URL)
	docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')

	# Persons by gender
	gender_df = pd.read_sql("SELECT gender_concept_id, COUNT(*) as count FROM person GROUP BY gender_concept_id", engine)
	plt.figure()
	gender_df.plot.bar(x='gender_concept_id', y='count', legend=False)
	plt.title('Number of Persons by Gender Concept ID')
	plt.xlabel('Gender Concept ID')
	plt.ylabel('Count')
	plt.tight_layout()
	plt.savefig(os.path.join(docs_dir, 'persons_by_gender.png'))

	# Age distribution
	age_df = pd.read_sql("SELECT year_of_birth FROM person", engine)
	age_df['age'] = pd.Timestamp.now().year - age_df['year_of_birth']
	plt.figure()
	age_df['age'].plot.hist(bins=10)
	plt.title('Age Distribution')
	plt.xlabel('Age')
	plt.ylabel('Number of Persons')
	plt.tight_layout()
	plt.savefig(os.path.join(docs_dir, 'age_distribution.png'))

	# Observations per year
	obs_year_df = pd.read_sql("SELECT EXTRACT(YEAR FROM observation_date::date) AS year, COUNT(*) as count FROM observation GROUP BY year ORDER BY year", engine)
	plt.figure()
	obs_year_df.plot.bar(x='year', y='count', legend=False)
	plt.title('Observations per Year')
	plt.xlabel('Year')
	plt.ylabel('Number of Observations')
	plt.tight_layout()
	plt.savefig(os.path.join(docs_dir, 'observations_per_year.png'))

	# Additional date-based visualizations
	# Observations per month
	obs_month_df = pd.read_sql("""
		SELECT DATE_TRUNC('month', observation_date::date) AS month, COUNT(*) as count
		FROM observation
		GROUP BY month
		ORDER BY month
	""", engine)
	plt.figure()
	obs_month_df.set_index('month')['count'].plot(marker='o')
	plt.title('Observations Per Month')
	plt.xlabel('Month')
	plt.ylabel('Number of Observations')
	plt.tight_layout()
	plt.savefig(os.path.join(docs_dir, 'observations_per_month.png'))

	# Cumulative observations over time
	obs_month_df['cumulative'] = obs_month_df['count'].cumsum()
	plt.figure()
	obs_month_df.set_index('month')['cumulative'].plot(marker='o')
	plt.title('Cumulative Observations Over Time')
	plt.xlabel('Month')
	plt.ylabel('Cumulative Observations')
	plt.tight_layout()
	plt.savefig(os.path.join(docs_dir, 'cumulative_observations.png'))

	# Top 3 observation concepts trends over time
	top_concepts = pd.read_sql("""
		SELECT observation_concept_id, COUNT(*) as count
		FROM observation
		GROUP BY observation_concept_id
		ORDER BY count DESC
		LIMIT 3
	""", engine)['observation_concept_id'].tolist()

	if top_concepts:
		obs_trend_df = pd.read_sql(f"""
			SELECT DATE_TRUNC('month', observation_date::date) AS month, observation_concept_id, COUNT(*) as count
			FROM observation
			WHERE observation_concept_id IN ({','.join(map(str, top_concepts))})
			GROUP BY month, observation_concept_id
			ORDER BY month, observation_concept_id
		""", engine)
		plt.figure()
		for concept in top_concepts:
			df = obs_trend_df[obs_trend_df['observation_concept_id'] == concept]
			plt.plot(df['month'], df['count'], marker='o', label=f'Concept {concept}')
		plt.title('Top Observation Concepts Over Time')
		plt.xlabel('Month')
		plt.ylabel('Number of Observations')
		plt.legend()
		plt.tight_layout()
		plt.savefig(os.path.join(docs_dir, 'top_concepts_over_time.png'))

	print("Analytics visualizations saved in docs/.")
