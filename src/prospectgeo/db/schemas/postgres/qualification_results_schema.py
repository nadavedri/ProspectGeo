def create_qualification_results_schema(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS QualificationResults (
                user_id TEXT,
                prospect_id TEXT,
                qualifies BOOLEAN,
                qualification_timestamp TIMESTAMP,
                PRIMARY KEY (user_id, prospect_id)
            );
        """)
        conn.commit()
