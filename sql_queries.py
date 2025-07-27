SEARCH_RECORDS = """
    SELECT v.visit_id, p.patient_name, v.visit_complaint ,v.visit_diagnosis, v.visit_prescription ,v.embedding <=> %s AS distance
    FROM Visits v
    JOIN Patient p ON v.patient_id = p.patient_id
    ORDER BY v.embedding <=> %s
    LIMIT 5;
"""

INSERT_RECORD = """
    INSERT INTO Visits (
        patient_id, doctor_id, hospital_id,
        visit_date, visit_complaint, visit_diagnosis,
        visit_prescription, admission_type, embedding
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING visit_id;
"""

FETCH_EXISTING_RECORD = """
    SELECT visit_complaint, visit_diagnosis
    FROM Visits
    WHERE visit_id = %s;
"""

UPDATE_RECORD = """
    UPDATE Visits
    SET visit_complaint = %s,
        visit_diagnosis = %s,
        embedding = %s
    WHERE visit_id = %s;
"""

DELETE_RECORD = """
    DELETE FROM Visits WHERE visit_id = %s;
"""

CHECK_RECORD_EXISTS = """
    SELECT visit_id FROM Visits WHERE visit_id = %s;
"""

GET_PATIENT_BY_ID = """
    SELECT v.visit_id, p.patient_name, v.visit_diagnosis
    FROM Visits v
    JOIN Patient p ON v.patient_id = p.patient_id
    WHERE v.visit_id = %s;
"""

CHECK_ID_EXISTS = """
    SELECT visit_id FROM Visits WHERE visit_id = %s;
"""

INSERTING_RECORD = """
    INSERT INTO Visits (
        visit_id, patient_id, doctor_id, hospital_id,
        visit_date, visit_complaint, visit_diagnosis,
        visit_prescription, admission_type, embedding
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""
