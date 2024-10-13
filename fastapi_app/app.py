from fastapi import FastAPI
from elasticsearch import Elasticsearch
import time
from typing import List
from faker import Faker
import databases
import sqlalchemy

app = FastAPI()

es = Elasticsearch(hosts=["http://elasticsearch:9200"])

in_memory_storage = []
fake = Faker()

DATABASE_URL = "postgresql://fastapi_user:fastapi_password@postgres:5432/fastapi_db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

texts = sqlalchemy.Table(
    "texts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("content", sqlalchemy.String, nullable=False),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/populate/")
async def populate_data(count: int = 1000):
    """
    Populate Elasticsearch, PostgreSQL, and in-memory storage with random strings.
    """
    global in_memory_storage
    in_memory_storage = []
    
    start_time = time.time()

    for _ in range(count):
        random_string = fake.text(max_nb_chars=200)
        
        in_memory_storage.append(random_string)

        es.index(index="test-index", body={"content": random_string})

        query = texts.insert().values(content=random_string)
        await database.execute(query)
    
    elapsed_time = time.time() - start_time
    return {"message": f"Populated {count} records", "elapsed_time": elapsed_time}

@app.get("/search/in_memory/{query}")
async def search_in_memory(query: str):
    """
    Search the in-memory list for matching strings using case-insensitive partial matching.
    """
    start_time = time.time()
    
    results = [item for item in in_memory_storage if query.lower() in item.lower()]
    
    elapsed_time = time.time() - start_time
    return {"results": results, "count": len(results), "elapsed_time": elapsed_time}

@app.get("/search/elasticsearch/{query}")
async def search_elasticsearch(query: str):
    """
    Search Elasticsearch for matching strings using a more flexible query.
    """
    start_time = time.time()
    result = es.search(index="test-index", body={
        "query": {
            "match_phrase_prefix": {
                "content": query
            }
        }
    })
    elapsed_time = time.time() - start_time
    return {"results": result['hits']['hits'], "count": len(result['hits']['hits']), "elapsed_time": elapsed_time}

@app.get("/search/postgres/{query}")
async def search_postgres(query: str):
    """
    Search PostgreSQL for matching strings using case-insensitive partial matching.
    """
    start_time = time.time()
    
    query = texts.select().where(texts.c.content.ilike(f"%{query}%"))
    rows = await database.fetch_all(query)
    
    results = [{"content": row["content"]} for row in rows]
    
    elapsed_time = time.time() - start_time
    return {"results": results, "count": len(results), "elapsed_time": elapsed_time}
