import faiss
import sqlite3
import os
import json
import io
import base64

def query_sqlite(db_path, query):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

faiss_index_id = "faiss_index:v1::test_bank_2"

db_path = os.getenv("SQLITE_STORE_DIR") + "/faiss_store.db"
query = f"select * from kvstore where key = '{faiss_index_id}';"

results = query_sqlite(db_path, query)

print(results[0][0])

value = json.loads(results[0][1])

bytes = io.BytesIO(base64.b64decode(value["faiss_index"]))

index = faiss.IndexFlatL2(384)
