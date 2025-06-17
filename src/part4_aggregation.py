
"""
part4_aggregation.py

Part 4: Advanced Queries & Aggregation for the EduHub e-learning platform.

- Task 4.1: Complex Queries
    * find_courses_by_price(min_price, max_price)
    * find_recent_users(months=6)
    * find_courses_by_tags(tags)
    * find_assignments_due_within(days=7)
- Task 4.2: Aggregation Pipelines
    * enrollment_stats(db)             – total enrollments & avg. course rating by category
    * course_enrollment_counts(db)     – total enrollments per course
    * course_completion_rate(db)       – completion rate per course
    * student_performance(db)          – avg. grade per student & top performers
    * instructor_analytics(db)         – students taught, avg. rating, revenue per instructor
    * advanced_trends(db)              – monthly trends, popular categories, avg. progress
- Running as script prints ASCII tables; importing returns pandas DataFrames.
"""

import datetime
from pymongo import MongoClient
import pandas as pd

from part1_setup import get_client, DB_NAME


try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


# --- Task 4.1: Complex Queries ---

def find_courses_by_price(db, min_price, max_price):
    """Find courses priced between min_price and max_price."""
    cursor = db.courses.find({
        "price": {"$gte": min_price, "$lte": max_price}
    })
    return pd.DataFrame(list(cursor))


def find_recent_users(db, months=6):
    """Find users who joined in the last `months` months."""
    now = datetime.datetime.utcnow()
    cutoff = now - datetime.timedelta(days=months * 30)
    cursor = db.users.find({"dateJoined": {"$gte": cutoff}})
    return pd.DataFrame(list(cursor))


def find_courses_by_tags(db, tags):
    """Find courses that have any of the specified tags."""
    cursor = db.courses.find({"tags": {"$in": tags}})
    return pd.DataFrame(list(cursor))


def find_assignments_due_within(db, days=7):
    """Find assignments due within the next `days` days."""
    now = datetime.datetime.utcnow()
    cutoff = now + datetime.timedelta(days=days)
    cursor = db.assignments.find({
        "dueDate": {"$gte": now, "$lte": cutoff}
    })
    return pd.DataFrame(list(cursor))


# --- Task 4.2: Aggregation Pipelines ---

def enrollment_stats(db):
    """
    Category-level stats:
    - totalEnrollments per course category
    - avgCourseRating per category
    """
    pipeline = [
        {"$lookup": {
            "from": "courses",
            "localField": "courseId",
            "foreignField": "courseId",
            "as": "course"
        }},
        {"$unwind": "$course"},
        {"$group": {
            "_id": "$course.category",
            "totalEnrollments": {"$sum": 1},
            "avgCourseRating": {"$avg": "$course.rating"}
        }},
        {"$project": {
            "_id": 0,
            "category": "$_id",
            "totalEnrollments": 1,
            "avgCourseRating": 1
        }}
    ]
    return pd.DataFrame(list(db.enrollments.aggregate(pipeline)))


def course_enrollment_counts(db):
    """
    Course-level counts:
    - totalEnrollments per course
    """
    pipeline = [
        {"$group": {
            "_id": "$courseId",
            "totalEnrollments": {"$sum": 1}
        }},
        {"$project": {
            "_id": 0,
            "courseId": "$_id",
            "totalEnrollments": 1
        }}
    ]
    return pd.DataFrame(list(db.enrollments.aggregate(pipeline)))


def course_completion_rate(db):
    """
    Course-level completion rate:
    - percent of enrollments marked 'completed' per course
    """
    pipeline = [
        {"$group": {
            "_id": "$courseId",
            "completed": {
                "$sum": {
                    "$cond": [{"$eq": ["$completionStatus", "completed"]}, 1, 0]
                }
            },
            "total": {"$sum": 1}
        }},
        {"$project": {
            "_id": 0,
            "courseId": "$_id",
            "completionRate": {
                "$cond": [
                    {"$eq": ["$total", 0]},
                    0,
                    {"$divide": ["$completed", "$total"]}
                ]
            }
        }}
    ]
    return pd.DataFrame(list(db.enrollments.aggregate(pipeline)))


def student_performance(db):
    """
    Per-student performance:
    - avgGrade from submissions
    - topPerformer flag (avgGrade ≥ 75th percentile)
    """
    # Avg grade per student
    grade_pipeline = [
        {"$group": {"_id": "$userId", "avgGrade": {"$avg": "$grade"}}},
        {"$project": {"_id": 0, "userId": "$_id", "avgGrade": 1}}
    ]
    df_grades = pd.DataFrame(list(db.submissions.aggregate(grade_pipeline)))

    # Identify top performers
    threshold = df_grades["avgGrade"].quantile(0.75) if not df_grades.empty else 0
    df_grades["topPerformer"] = df_grades["avgGrade"] >= threshold

    return df_grades


def instructor_analytics(db):
    """
    Instructor-level analytics:
    - numStudents (distinct) taught
    - avgCourseRating across their courses
    - totalRevenue from enrollments in their courses
    """
    pipeline = [
        {"$lookup": {
            "from": "courses",
            "localField": "courseId",
            "foreignField": "courseId",
            "as": "course"
        }},
        {"$unwind": "$course"},
        {"$group": {
            "_id": "$course.instructorId",
            "studentsSet": {"$addToSet": "$userId"},
            "avgCourseRating": {"$avg": "$course.rating"},
            "totalRevenue": {"$sum": "$course.price"}
        }},
        {"$project": {
            "_id": 0,
            "instructorId": "$_id",
            "numStudents": {"$size": "$studentsSet"},
            "avgCourseRating": 1,
            "totalRevenue": 1
        }}
    ]
    return pd.DataFrame(list(db.enrollments.aggregate(pipeline)))


def advanced_trends(db):
    """
    Advanced analytics:
    - monthlyEnrollments: per-month counts over past year
    - popularCategories: most-enrolled categories
    - avgProgress: average progress per course
    """
    now = datetime.datetime.utcnow()
    year_ago = now - datetime.timedelta(days=365)

    # Monthly enrollments
    m_pipeline = [
        {"$match": {"enrolledAt": {"$gte": year_ago}}},
        {"$group": {
            "_id": {"year": {"$year": "$enrolledAt"}, "month": {"$month": "$enrolledAt"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.year": 1, "_id.month": 1}},
        {"$project": {
            "_id": 0,
            "year": "$_id.year",
            "month": "$_id.month",
            "enrollments": "$count"
        }}
    ]
    df_monthly = pd.DataFrame(list(db.enrollments.aggregate(m_pipeline)))

    # Popular categories
    c_pipeline = [
        {"$lookup": {
            "from": "courses",
            "localField": "courseId",
            "foreignField": "courseId",
            "as": "course"
        }},
        {"$unwind": "$course"},
        {"$group": {
            "_id": "$course.category",
            "enrollments": {"$sum": 1}
        }},
        {"$sort": {"enrollments": -1}},
        {"$project": {"_id": 0, "category": "$_id", "enrollments": 1}}
    ]
    df_popular = pd.DataFrame(list(db.enrollments.aggregate(c_pipeline)))

    # Average progress per course
    p_pipeline = [
        {"$group": {
            "_id": "$courseId",
            "avgProgress": {"$avg": "$progress"}
        }},
        {"$lookup": {
            "from": "courses",
            "localField": "_id",
            "foreignField": "courseId",
            "as": "course"
        }},
        {"$unwind": "$course"},
        {"$project": {
            "_id": 0,
            "courseId": "$_id",
            "title": "$course.title",
            "avgProgress": 1
        }}
    ]
    df_progress = pd.DataFrame(list(db.enrollments.aggregate(p_pipeline)))

    return {
        "monthlyEnrollments": df_monthly,
        "popularCategories": df_popular,
        "avgProgress": df_progress
    }


def print_tables(tables: dict):
    """Print each DataFrame as an ASCII table when run as a script."""
    for name, df in tables.items():
        print(f"\n=== {name.replace('_', ' ').title()} ===")
        if tabulate:
            print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
        else:
            print(df.to_string(index=False))


def main():
    client = get_client()
    db = client[DB_NAME]

    # Task 4.1 queries
    q1 = find_courses_by_price(db, 50, 200)
    q2 = find_recent_users(db, 6)
    q3 = find_courses_by_tags(db, ["MongoDB", "ETL"])
    q4 = find_assignments_due_within(db, 7)

    # Task 4.2 aggregations
    a1 = enrollment_stats(db)
    a2 = course_enrollment_counts(db)
    a3 = course_completion_rate(db)
    a4 = student_performance(db)
    a5 = instructor_analytics(db)
    trends = advanced_trends(db)

    # Collect all results
    tables = {
        "courses_by_price": q1,
        "recent_users": q2,
        "courses_by_tags": q3,
        "assignments_due_soon": q4,
        "enrollment_stats_by_category": a1,
        "enrollment_counts_per_course": a2,
        "completion_rate_by_course": a3,
        "student_performance": a4,
        "instructor_analytics": a5,
        **trends
    }

    print_tables(tables)
    return tables


if __name__ == "__main__":
    main()
