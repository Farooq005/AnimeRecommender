from sqlalchemy import create_engine, text
import json

# Connect to Neon
db_url = "postgresql://neondb_owner:npg_ziW1uVZR4jhL@ep-dry-flower-a5cttzfr-pooler.us-east-2.aws.neon.tech/user_anime_stats?sslmode=require"
engine = create_engine(db_url, connect_args={'connect_timeout':10})

schema_url = "https://raw.githubusercontent.com/Farooq005/AnimeRecommender/refs/heads/main/schema.sql"

schema_sql = requests.get(schema_url).text


with engine.connect() as conn:
    # Check if the 'users' table exists
    table_exists = engine.dialect.has_table(conn, "users") 
    if not table_exists:
      conn.execute(text(schema_sql))
      conn.commit()
      print("Schema created!")
    else:
      print("Schema already exists!")
