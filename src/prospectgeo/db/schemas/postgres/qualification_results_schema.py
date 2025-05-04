def create_qualification_results_schema(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS QualificationResults (
                user_id INT,
                prospect_id INT,
                qualifies BOOLEAN,
                qualification_timestamp TIMESTAMP,
                PRIMARY KEY (user_id, prospect_id)
            );
        """)
        conn.commit()