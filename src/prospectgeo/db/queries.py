def insert_qualification_results():
    return """
        INSERT INTO QualificationResults (user_id, prospect_id, qualifies, qualification_timestamp)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id, prospect_id)
        DO UPDATE SET
            qualifies = EXCLUDED.qualifies,
            qualification_timestamp = EXCLUDED.qualification_timestamp;
    """
