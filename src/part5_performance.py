
"""
part5_performance.py

Part 5: Indexing & Performance Optimization for the EduHub e-learning platform.

Task 5.1: Index Creation
- users.email
- courses.title, courses.category
- assignments.dueDate
- enrollments.userId, enrollments.courseId

Task 5.2: Query Optimization
- Profile three representative queries with MongoDB explain() before/after indexing
- Measure client-side elapsed time using time.perf_counter()
- Document both server- and client-side improvements
"""

import datetime
import time
from pymongo import errors
from part1_setup import get_client, DB_NAME
import pandas as pd


try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

# Define the queries to profile
PROFILE_TASKS = [
    {
        "name": "Courses by Category",
        "collection": "courses",
        "filter": {"category": "Data Science"},
        "index_name": "idx_courses_category"
    },
    {
        "name": "Enrollments by User",
        "collection": "enrollments",
        "filter": {"userId": "u1001"},
        "index_name": "idx_enrollments_userId"
    },
    {
        "name": "Assignments Due Soon",
        "collection": "assignments",
        "filter": None,  # to be set dynamically
        "index_name": "idx_assignments_dueDate"
    }
]


def drop_indexes(db):
    """Drop all custom indexes created by this script, if they exist."""
    idxs = [
        ("users", "idx_users_email"),
        ("courses", "idx_courses_title"),
        ("courses", "idx_courses_category"),
        ("assignments", "idx_assignments_dueDate"),
        ("enrollments", "idx_enrollments_userId"),
        ("enrollments", "idx_enrollments_courseId")
    ]
    for coll_name, idx_name in idxs:
        coll = db[coll_name]
        if idx_name in coll.index_information():
            try:
                coll.drop_index(idx_name)
                print(f"[INFO] Dropped index {coll_name}.{idx_name}")
            except errors.OperationFailure as e:
                print(f"[WARN] Could not drop index {coll_name}.{idx_name}: {e}")


def create_indexes(db):
    """Create the required indexes for performance optimization."""
    idx_specs = [
        ("users", [("email", 1)], {"unique": True,  "name": "idx_users_email"}),
        ("courses", [("title", 1)], {"name": "idx_courses_title"}),
        ("courses", [("category", 1)], {"name": "idx_courses_category"}),
        ("assignments", [("dueDate", 1)], {"name": "idx_assignments_dueDate"}),
        ("enrollments", [("userId", 1)], {"name": "idx_enrollments_userId"}),
        ("enrollments", [("courseId", 1)], {"name": "idx_enrollments_courseId"})
    ]
    for coll_name, fields, opts in idx_specs:
        coll = db[coll_name]
        try:
            coll.create_index(fields, **opts)
            print(f"[OK] Created index {coll_name}.{opts['name']}")
        except errors.PyMongoError as e:
            print(f"[ERROR] Could not create index on {coll_name}: {e}")


def explain_execution_time(coll, fltr):
    """
    Use the database command to explain the find(filter) with executionStats verbosity.
    Returns server executionTimeMillis.
    """
    try:
        # Build the explain command
        cmd = {
            "explain": {"find": coll.name, "filter": fltr}
        }
        exp = coll.database.command("explain", cmd, verbosity="executionStats")
        return exp.get("executionStats", {}).get("executionTimeMillis", None)
    except errors.PyMongoError as e:
        print(f"[ERROR] Explain failed: {e}")
        return None


def profile_queries(db):
    """
    Profile each task both server-side (explain) and client-side (perf_counter)
    before and after index creation. Returns a summary DataFrame.
    """
    summary = []
    # Prepare dynamic filter for assignments due soon
    now = datetime.datetime.now(datetime.timezone.utc)
    week_later = now + datetime.timedelta(days=7)
    for task in PROFILE_TASKS:
        if task["name"] == "Assignments Due Soon":
            task["filter"] = {"dueDate": {"$gte": now, "$lte": week_later}}

    # 1) Drop any existing indexes to measure 'before' performance
    drop_indexes(db)

    # 2) Measure BEFORE-index times
    for task in PROFILE_TASKS:
        coll = db[task["collection"]]
        fltr = task["filter"]

        # Client-side timing
        start = time.perf_counter()
        list(coll.find(fltr))
        client_before = (time.perf_counter() - start) * 1000  # ms

        # Server-side explain timing
        server_before = explain_execution_time(coll, fltr)

        summary.append({
            "Query":               task["name"],
            "Index":               task["index_name"],
            "Server Before (ms)":  server_before,
            "Client Before (ms)":  round(client_before, 1),
            "Server After (ms)":   None,
            "Client After (ms)":   None
        })

    # 3) Create all indexes as per Task 5.1
    create_indexes(db)

    # 4) Measure AFTER-index times
    for row in summary:
        task = next(t for t in PROFILE_TASKS if t["index_name"] == row["Index"])
        coll = db[task["collection"]]
        fltr = task["filter"]

        # Client-side timing
        start = time.perf_counter()
        list(coll.find(fltr))
        client_after = (time.perf_counter() - start) * 1000  # ms

        # Server-side explain timing
        server_after = explain_execution_time(coll, fltr)

        row["Server After (ms)"] = server_after
        row["Client After (ms)"] = round(client_after, 1)

    # 5) Build DataFrame and calculate improvements
    df = pd.DataFrame(summary)
    df["Server Improvement (%)"] = df.apply(
        lambda r: None
                  if r["Server Before (ms)"] is None or r["Server After (ms)"] is None
                  else round((r["Server Before (ms)"] - r["Server After (ms)"])
                             / r["Server Before (ms)"] * 100, 1),
        axis=1
    )
    df["Client Improvement (%)"] = df.apply(
        lambda r: None
                  if r["Client Before (ms)"] is None or r["Client After (ms)"] is None
                  else round((r["Client Before (ms)"] - r["Client After (ms)"])
                             / r["Client Before (ms)"] * 100, 1),
        axis=1
    )

    return df


def print_summary(df: pd.DataFrame):
    """Print the summary DataFrame as an ASCII table."""
    print("\n=== Indexing & Query Performance Summary ===")
    if tabulate:
        print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
    else:
        print(df.to_string(index=False))


def main():
    client = get_client()
    db = client[DB_NAME]

    summary_df = profile_queries(db)

    if __name__ == "__main__":
        print_summary(summary_df)

    return summary_df


if __name__ == "__main__":
    main()
