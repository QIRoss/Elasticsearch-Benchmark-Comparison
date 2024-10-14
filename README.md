# Elasticsearch Benchmark Comparison

Studies based in day 37-38 of 100 Days System Design for DevOps and Cloud Engineers.

https://deoshankar.medium.com/100-days-system-design-for-devops-and-cloud-engineers-18af7a80bc6f

Days 31–40: Scalability and Performance Optimization

Day 37–38: Optimize a large-scale Elasticsearch cluster for search performance.

## Project Overview

In this project we compare the performance of three different data storage and search approaches—in-memory storage, PostgreSQL, and Elasticsearch—using a FastAPI application. The project demonstrates how to populate and search through a dataset using each method, highlighting their strengths and weaknesses in terms of speed, scalability, and search complexity. By running benchmarks with both small and large datasets, we analyze how each approach performs under different conditions, with Elasticsearch showing significant advantages for full-text search on large datasets after the initial query, while in-memory storage remains optimal for small-scale operations.

This project focus in populating a dataset and then provide three FastAPI endpoints capable of processing it.

Theoretical Performance Order:
* 1- In-memory (Fastest for small datasets, low complexity).
* 2- PostgreSQL (Fast for structured data and indexed queries, medium for large datasets).
* 3- Elasticsearch (Slowest for small datasets but best for large, complex, full-text searches).

If you populate a large dataset like 30000 you will see Elasticsearch become the fastest after first execution.

## How to Run:

Start docker-compose
```
docker-compose up --build
```
Populate the database for a small dataset like 1000:
```
curl -X POST "http://localhost:8000/populate/?count=1000"
```
You can also do a large dataset (takes some minutes to run):
```
curl -X POST "http://localhost:8000/populate/?count=30000"
```

Endpoints to benchmark:

In-memory endpoint:
```
curl "http://localhost:8000/search/in_memory/foo"
```
Elasticsearch endpoint:
```
curl "http://localhost:8000/search/elasticsearch/foo"
```
Postgres endpoint:
```
curl "http://localhost:8000/search/postgres/foo"
```

## Author
This project was implemented by [Lucas de Queiroz dos Reis][2]. It is based on the [100 Days System Design for DevOps and Cloud Engineers][1].

[1]: https://deoshankar.medium.com/100-days-system-design-for-devops-and-cloud-engineers-18af7a80bc6f "Medium - Deo Shankar 100 Days"
[2]: https://www.linkedin.com/in/lucas-de-queiroz/ "LinkedIn - Lucas de Queiroz"
