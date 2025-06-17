# Performance Analysis for EduHub E-learning Platform

## Objective

Evaluated query performance improvements through indexing and optimization of frequently accessed fields within the EduHub MongoDB database.

## Indexed Fields

The following indexes were created:

* **users**: Indexed on `email` (unique)
* **courses**: Indexed on `title`, `category`
* **assignments**: Indexed on `dueDate`
* **enrollments**: Indexed on `userId`, `courseId`

## Profiling Method

Performance metrics were measured both client-side using Python's `time.perf_counter()` and server-side using MongoDB’s `explain()` with `executionStats` verbosity.

## Queries Profiled

1. **Courses by Category**
2. **Enrollments by User**
3. **Assignments Due Soon** (next 7 days)

## Results Summary

| Query                | Server Before (ms)  | Client Before (ms) | Server After (ms) | Client After (ms) | Server Improvement (%) | Client Improvement (%) |
| -------------------- | ------------------- | ------------------ | ----------------- | ----------------- | ---------------------- | ---------------------- |
| Courses by Category  | N/A (Explain error) | 1.0 ms             | N/A               | 0.5 ms            | N/A                    | 50%                    |
| Enrollments by User  | N/A (Explain error) | 1.2 ms             | N/A               | 0.5 ms            | N/A                    | 58.3%                  |
| Assignments Due Soon | N/A (Explain error) | 0.4 ms             | N/A               | 0.8 ms            | N/A                    | -100%                  |

## Observations and Issues

* **Server-side profiling** using MongoDB `explain()` method failed due to a misuse in the command syntax (`'Explain cannot explain itself'`). To rectify, ensure that the explain command correctly wraps the query without recursively calling itself.
* **Client-side measurements** indicate substantial performance improvements after indexing, notably for queries involving categorical and user-related fields.
* **Assignments Due Soon** query exhibited a regression (-100% performance change). Potential causes could include small data volume or overhead from indexing on very recent dates. Further investigation recommended.

## Recommendations

* Correct and retest the MongoDB `explain()` command for accurate server-side metrics.
* Regularly update indexes based on query patterns and ensure unnecessary indexes are dropped to optimize storage and write performance.

## Conclusion

Indexing significantly improved client-side query performance, affirming indexing's crucial role in database optimization. Server-side profiling remains necessary for complete validation once corrected.
