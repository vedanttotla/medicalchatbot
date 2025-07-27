from fastapi import FastAPI, HTTPException, Path, Depends, Body
from pydantic import BaseModel
from typing import List, Optional
from psycopg2 import pool
from pgvector.psycopg2 import register_vector
from pgvector import Vector
from transformers import AutoTokenizer, AutoModel
from fastapi.middleware.cors import CORSMiddleware
import torch

from sql_queries import (
    SEARCH_RECORDS, FETCH_EXISTING_RECORD, UPDATE_RECORD,
    DELETE_RECORD, CHECK_RECORD_EXISTS, GET_PATIENT_BY_ID,
    CHECK_ID_EXISTS, INSERTING_RECORD
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "dbname": "covid_db",
    "user": "postgres",
    "password": "vedant2005",
    "host": "localhost",
    "port": "5432"
}
db_pool = pool.SimpleConnectionPool(1, 10, **DB_CONFIG)

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(text: str) -> List[float]:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().tolist()

def get_cursor():
    conn = db_pool.getconn()
    try:
        cur = conn.cursor()
        register_vector(cur)
        yield cur
    finally:
        cur.close()
        db_pool.putconn(conn)

class QueryInput(BaseModel):
    query: str

class CovidRecord(BaseModel):
    id: int
    name: str
    complaint: str
    diagnosis: str
    prescription: str
    similarity_score: float

class NewRecord(BaseModel):
    name: str
    medical_condition: str

class UpdateRecord(BaseModel):
    name: Optional[str] = None
    medical_condition: Optional[str] = None

@app.post("/search-query", response_model=List[CovidRecord])
def search_query(input: QueryInput, cur=Depends(get_cursor)):
    emb = Vector(get_embedding(input.query))
    cur.execute(SEARCH_RECORDS, (emb, emb))
    return [
        CovidRecord(
            id=r[0],
            name=r[1],
            complaint=r[2],
            diagnosis=r[3],
            prescription=r[4],
            similarity_score=round(1 - r[5], 4)
        )
        for r in cur.fetchall()
    ]

@app.post("/create-record/{record_id}")
def create_record(record_id: int, record: NewRecord, cur=Depends(get_cursor)):
    try:
        cur.execute(CHECK_ID_EXISTS, (record_id,))
        if cur.fetchone():
            raise HTTPException(status_code=409, detail="Record with this ID already exists")
        emb = Vector(get_embedding(record.medical_condition))
        cur.execute(INSERTING_RECORD, (record_id, record.name, record.medical_condition, emb))
        cur.connection.commit()
        return {"message": "Record created", "id": record_id}
    except Exception as e:
        cur.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating record: {str(e)}")

@app.put("/update-record/{record_id}")
def update_record(record_id: int = Path(..., gt=0), record: UpdateRecord = Body(...), cur=Depends(get_cursor)):
    cur.execute(FETCH_EXISTING_RECORD, (record_id,))
    existing = cur.fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Record not found")
    name = record.name or existing[0]
    condition = record.medical_condition or existing[1]
    emb = Vector(get_embedding(condition))
    cur.execute(UPDATE_RECORD, (name, condition, emb, record_id))
    cur.connection.commit()
    return {"message": "Record updated", "id": record_id}

@app.delete("/delete-record/{record_id}")
def delete_record(record_id: int = Path(..., gt=0), cur=Depends(get_cursor)):
    cur.execute(CHECK_RECORD_EXISTS, (record_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Record not found")
    cur.execute(DELETE_RECORD, (record_id,))
    cur.connection.commit()
    return {"message": "Record deleted", "id": record_id}

@app.get("/get-record/{record_id}", response_model=CovidRecord)
def get_record(record_id: int = Path(..., gt=0), cur=Depends(get_cursor)):
    cur.execute(GET_PATIENT_BY_ID, (record_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Record not found")
    return CovidRecord(
        id=row[0],
        name=row[1],
        complaint="", 
        diagnosis=row[2],
        prescription="",  
        similarity_score=1.0
    )
