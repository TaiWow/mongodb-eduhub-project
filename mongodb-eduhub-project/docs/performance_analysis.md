# Performance Analysis: Indexing & Query Optimization

Based on the console log I captured, here’s what happened during my profiling run for Task 5.2.

---

## 1. Index Cleanup (Pre-index Baseline)

```text
[INFO] Dropped index courses.idx_courses_title  
[INFO] Dropped index courses.idx_courses_category  
[INFO] Dropped index assignments.idx_assignments_dueDate  
[INFO] Dropped index enrollments.idx_enrollments_userId  
[INFO] Dropped index enrollments.idx_enrollments_courseId  
```

* **What I did:** I dropped all five custom indexes on `courses.title`, `courses.category`, `assignments.dueDate`, `enrollments.userId`, and `enrollments.courseId`.
* **Why it matters:** Removing these indexes ensured that my "before" measurements truly reflect unindexed query performance.

---

## 2. “Before” Explain-Driven Profiling

```text
[ERROR] Explain failed: Explain cannot explain itself…  × 3  
```

* **What I saw:** Each call to `explain_execution_time()` failed because I tried to explain an explain command itself—MongoDB rejects that (`IllegalOperation`).
* **Impact:** I couldn’t capture any server-side execution times for the unindexed queries.

---

## 3. Index Creation

```text
[ERROR] Could not create index on users: Index already exists with a different name: uix_users_email  
[OK] Created index courses.idx_courses_title  
[OK] Created index courses.idx_courses_category  
[OK] Created index assignments.idx_assignments_dueDate  
[OK] Created index enrollments.idx_enrollments_userId  
[OK] Created index enrollments.idx_enrollments_courseId  
```

* **Email index conflict:** I attempted to create `idx_users_email`, but the database already had a unique index named `uix_users_email`, so that step failed.
* **Other indexes:** I successfully created the five non-email indexes, putting my database into the intended "after" state.

---

## 4. “After” Explain-Driven Profiling

```text
[ERROR] Explain failed: Explain cannot explain itself…  × 3  
```

* **What I saw:** The same explain-misuse occurred after index creation, so again I recorded no server-side metrics for the optimized queries.

---

## 5. Client-Side Timing (Implicit)

I called `list(coll.find(...))` both before and after indexing, but I didn’t log the `time.perf_counter()` results—so those timings exist internally but aren’t in my console output.

---

## 6. Summary

| Metric                 | Status                         |
| ---------------------- | ------------------------------ |
| **Server Before (ms)** | Missing                        |
| **Client Before (ms)** | Unlogged                       |
| **Index Drops**        | Completed                      |
| **Index Creates**      | Partial (email index conflict) |
| **Server After (ms)**  | Missing                        |
| **Client After (ms)**  | Unlogged                       |
| **% Improvements**     | Not calculable                 |


