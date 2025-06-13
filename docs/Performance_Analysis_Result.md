
# Performance Analysis Report

As part of the performance optimization phase of this PyMongo-based application, an in-depth query performance analysis was conducted using MongoDB’s `.explain()` method. The goal was to identify inefficient query patterns and implement indexing strategies to improve execution time and reduce resource consumption.

---

## Objective

- Analyze critical queries using `.explain()` to assess execution plans.
- Detect performance bottlenecks such as full collection scans (COLLSCAN).
- Apply appropriate indexes to enhance query performance.
- Measure the impact of optimizations using Python’s `time` module.

---

## Identified Issues

Initially, several frequently executed queries were relying on **COLLSCAN**, causing high latency and inefficient resource usage. These queries included:

- Fetching users by `email`
- Retrieving assignments by `due_date`
- Searching courses by `title` and `category`

These access patterns did not leverage any existing indexes, resulting in full scans of entire collections—acceptable only in small datasets but problematic at scale.

---

## Optimization Steps and Solutions

### 1. Users Collection

- **Issue**: Querying users by `email` triggered a `COLLSCAN`.
- **Solution**: Created a **unique index** on the `email` field.
- **Result**: Query plan changed from `COLLSCAN` to `IXSCAN`, significantly improving performance.

```python
db.users.create_index("email", unique=True)
```

---

### 2. Assignments Collection

- **Issue**: Filtering assignments by `due_date` performed a full scan.
- **Solution**: Created a **single-field index** on the `due_date` field.
- **Result**: MongoDB began using `IXSCAN`, improving query speed.

```python
db.assignments.create_index("due_date")
```

---

### 3. Courses Collection

- **Issue**: Queries filtering by both `title` and `category` were inefficient.
- **Solution**: Introduced a **compound index** on `title` and `category`.
- **Result**: Optimized traversal with a single index scan.

```python
db.courses.create_index([("title", 1), ("category", 1)])
```

---

## Benchmarking Results

The `time` module in Python was used to compare query execution time **before and after** index application.

| Query Type              | Before Indexing (ms) | After Indexing (ms) |
|------------------------|----------------------|---------------------|
| User lookup by email   | > 200                | < 10                |
| Assignment by due date | > 150                | < 10                |
| Course search          | > 250                | < 15                |

These results show a **90–95% reduction** in query time across key operations.

---

## Methodology

1. Used `.explain()` to analyze query execution plans:
   ```python
   db.users.find({"email": "test@example.com"}).explain()
   ```

2. Created indexes based on analysis findings.

3. Re-ran queries and verified `IXSCAN` usage in the new execution plans.

4. Measured performance using:
   ```python
   import time
   start = time.time()
   db.users.find_one({"email": "test@example.com"})
   print("Execution time:", time.time() - start)
   ```

---

## Conclusion

This performance tuning process highlighted the importance of:

- Aligning index design with query patterns.
- Using `.explain()` for real-time insight into MongoDB behavior.
- Continuously benchmarking queries to ensure scalability.

By proactively addressing query inefficiencies, the application is now significantly faster and better prepared for larger datasets.

---

## Recommendations

- Regularly monitor slow queries using MongoDB logs or Atlas tools.
- Review query plans after major schema or feature changes.
- Reassess index usage as data volume and usage patterns evolve.

---

*Prepared by: Feyisayo Ajiboye*  
*Role: Data Engineer*  
*Date: June 2025*
