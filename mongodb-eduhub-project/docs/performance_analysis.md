# Performance Analysis: Indexing & Query Optimization

Based on the console log I captured, here’s how my Part 5 tasks (5.1 and 5.2) actually executed:

---

## Task 5.1: Index Creation

* **User email lookup index**

  * Attempted creating `idx_users_email` failed because `uix_users_email` already existed.
  * **Result:** Email lookup index remains as `uix_users_email` (preexisting).

* **Course search indexes**

  ```
  [OK] Created index courses.idx_courses_title  
  [OK] Created index courses.idx_courses_category  
  ```

  Both title and category indexes on `courses` were created successfully.

* **Assignment due date index**

  ```
  [OK] Created index assignments.idx_assignments_dueDate  
  ```

* **Enrollment indexes**

  ```
  [OK] Created index enrollments.idx_enrollments_userId  
  [OK] Created index enrollments.idx_enrollments_courseId  
  ```

All required indexes except the email-lookup index were created as intended.

---

## Task 5.2: Query Optimization

I profiled three representative queries **before** and **after** index creation. However, all my `explain()` calls failed with:

```text
[ERROR] Explain failed: Explain cannot explain itself.  (×6 total)
```

This means I never captured any server-side `executionTimeMillis` data, either pre- or post-indexing for:

1. **Courses by Category**
2. **Enrollments by User**
3. **Assignments Due Soon**

Furthermore, **client-side timings** were measured internally via `time.perf_counter()` but **not logged**, so I have no concrete before/after millisecond values.

---

## Summary Table

| Query                | Index                     | Server Before (ms) | Client Before (ms) | Server After (ms) | Client After (ms) | Server Improvement (%) | Client Improvement (%) |
| -------------------- | ------------------------- | ------------------ | ------------------ | ----------------- | ----------------- | ---------------------- | ---------------------- |
| Courses by Category  | idx\_courses\_category    | *n/a*              | *n/a*              | *n/a*             | *n/a*             | *n/a*                  | *n/a*                  |
| Enrollments by User  | idx\_enrollments\_userId  | *n/a*              | *n/a*              | *n/a*             | *n/a*             | *n/a*                  | *n/a*                  |
| Assignments Due Soon | idx\_assignments\_dueDate | *n/a*              | *n/a*              | *n/a*             | *n/a*             | *n/a*                  | *n/a*                  |

---

### Analysis

* **Index Creation (5.1)**: Success for all except the user-email index, due to a name conflict.
* **Query Profiling (5.2)**: Server-side profiling failed entirely; client timings exist but weren’t output.

This reflects exactly what my console log shows, mapped back to the project brief’s requirements.
