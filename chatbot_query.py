import pandas as pd
import psycopg2
from pgvector.psycopg2 import register_vector # so that we can pass vector objects directly in queries.
from pgvector import Vector
from transformers import AutoTokenizer, AutoModel
import torch
from sql_queries import SEARCH_RECORDS
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

conn = psycopg2.connect(
    dbname="covid_db",
    user="postgres",
    password="vedant2005",  
    host="localhost",
    port="5432"
)
cur = conn.cursor()
register_vector(cur)

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().tolist()

cur.execute("SELECT visit_id, visit_diagnosis FROM Visits WHERE embedding IS NULL")
rows = cur.fetchall()

for visit_id, diagnosis in rows:
    if diagnosis:  
        emb = Vector(get_embedding(diagnosis))
        cur.execute("UPDATE Visits SET embedding = %s WHERE visit_id = %s", (emb, visit_id))

conn.commit()


query_text = input("Enter your query: ")


query_embedding = Vector(get_embedding(query_text))

cur.execute(
    SEARCH_RECORDS,
    (query_embedding, query_embedding)
)

rows = cur.fetchall()
print("\nTop matching records:")
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Condition: {row[2]}, Similarity Score: {1 - row[3]:.4f}")

cur.close()
conn.close()