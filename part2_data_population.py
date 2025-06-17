#!/usr/bin/env python3
"""
part2_data_population.py

Part 2: Data Population for the EduHub e-learning platform.
- Clears existing documents.
- Generates and inserts:
    * 20 users (5 instructors + 15 students)
    * 8 courses
    * 15 enrollments
    * 25 lessons
    * 10 assignments
    * 12 submissions
- When run as a script: prints ASCII tables via tabulate.
- When imported in a notebook: call main() to get back a dict of pandas DataFrames.
"""

import sys
import random
import datetime

from pymongo import errors
from part1_setup import get_client, DB_NAME

import pandas as pd

# Optional: for prettier terminal tables
try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

# Make this module‐level so notebooks can inspect after calling main()
tables: dict = {}

# Seed randomness for reproducibility
random.seed(42)


def clear_collections(db):
    """Remove all documents from each target collection."""
    for coll in ["users", "courses", "enrollments", "lessons", "assignments", "submissions"]:
        db[coll].delete_many({})


def generate_users(now):
    """Generate 20 users: 5 instructors + 15 students."""
    users = []
    # Instructors
    for i in range(1, 6):
        users.append({
            "userId":     f"u{2000+i}",
            "email":      f"instructor{i}@example.com",
            "firstName":  f"Instructor{i}",
            "lastName":   "Smith",
            "role":       "instructor",
            "dateJoined": now - datetime.timedelta(days=random.randint(30, 365)),
            "profile":    {"bio": f"Expert in subject {i}", "avatar": "", "skills": ["Teaching", "Leadership"]},
            "isActive":   True
        })
    # Students
    for i in range(1, 16):
        users.append({
            "userId":     f"u{1000+i}",
            "email":      f"student{i}@example.com",
            "firstName":  f"Student{i}",
            "lastName":   "Jones",
            "role":       "student",
            "dateJoined": now - datetime.timedelta(days=random.randint(0, 365)),
            "profile":    {"bio": "", "avatar": "", "skills": []},
            "isActive":   random.choice([True, True, True, False])
        })
    return users


def generate_courses(now, instructors):
    """Generate 8 courses, randomly assigned to instructors."""
    categories = [
        "Data Science", "Web Development", "Machine Learning",
        "Cloud Computing", "UI/UX Design", "Cybersecurity",
        "Mobile Development", "Databases"
    ]
    courses = []
    for idx, cat in enumerate(categories, start=1):
        created = now - datetime.timedelta(days=random.randint(0, 365))
        courses.append({
            "courseId":     f"c{3000+idx}",
            "title":        f"{cat} Essentials",
            "description":  f"An introductory course on {cat}.",
            "instructorId": random.choice(instructors)["userId"],
            "category":     cat,
            "level":        random.choice(["beginner", "intermediate", "advanced"]),
            "duration":     round(random.uniform(5.0, 20.0), 1),
            "price":        round(random.uniform(0, 200), 2),
            "tags":         [cat, cat.split()[0]],
            "rating":       0.0,
            "ratingsCount": 0,
            "createdAt":    created,
            "updatedAt":    created,
            "isPublished":  random.choice([True, False])
        })
    return courses


def generate_enrollments(now, students, courses):
    """Generate 15 unique enrollments with progress/completion status."""
    enrollments, seen, idx = [], set(), 1
    while len(enrollments) < 15:
        student = random.choice(students)
        course  = random.choice(courses)
        key     = (student["userId"], course["courseId"])
        if key in seen:
            continue
        seen.add(key)
        enrolled = now - datetime.timedelta(days=random.randint(0, 365))
        prog     = random.randint(0, 100)
        enrollments.append({
            "enrollmentId":    f"e{4000+idx}",
            "userId":          student["userId"],
            "courseId":        course["courseId"],
            "enrolledAt":      enrolled,
            "progress":        prog,
            "completionStatus": "completed" if prog == 100 else "in progress"
        })
        idx += 1
    return enrollments


def generate_lessons(now, courses):
    """Generate 25 lessons, distributed roughly evenly across courses."""
    lessons, lesson_id = [], 1
    per_course = 25 // len(courses)
    extra      = 25 - per_course * len(courses)
    for idx, course in enumerate(courses):
        count = per_course + (1 if idx < extra else 0)
        for order in range(1, count + 1):
            created = now - datetime.timedelta(days=random.randint(0, 365))
            lessons.append({
                "lessonId":  f"l{4000+lesson_id}",
                "courseId":  course["courseId"],
                "title":     f"{course['title']} - Lesson {order}",
                "content":   f"Content for lesson {order} of {course['title']}.",
                "order":     order,
                "createdAt": created,
                "updatedAt": created
            })
            lesson_id += 1
    return lessons


def generate_assignments(now, courses):
    """Generate 10 assignments randomly assigned to courses."""
    assignments = []
    for i in range(1, 11):
        course  = random.choice(courses)
        created = now - datetime.timedelta(days=random.randint(0, 365))
        due     = created + datetime.timedelta(days=random.randint(7, 30))
        assignments.append({
            "assignmentId": f"a{5000+i}",
            "courseId":     course["courseId"],
            "title":        f"{course['title']} - Assignment {i}",
            "description":  f"Complete the task for assignment {i}.",
            "dueDate":      due,
            "createdAt":    created,
            "updatedAt":    created
        })
    return assignments


def generate_submissions(now, assignments, students):
    """Generate 12 submissions with grades and feedback."""
    submissions = []
    for i in range(1, 13):
        assignment = random.choice(assignments)
        student    = random.choice(students)
        created    = assignment["createdAt"]
        delta      = (assignment["dueDate"] - created).days or 1
        submitted  = created + datetime.timedelta(days=random.randint(0, delta))
        grade_val  = random.randint(0, 100)
        feedback   = "Good job!" if grade_val >= 50 else "Needs improvement."
        submissions.append({
            "submissionId": f"s{6000+i}",
            "assignmentId": assignment["assignmentId"],
            "userId":       student["userId"],
            "submittedAt":  submitted,
            "grade":        grade_val,
            "feedback":     feedback
        })
    return submissions


def print_tables(tables: dict):
    """Print each DataFrame as an ASCII table when run in a terminal."""
    for name, df in tables.items():
        print(f"\n=== {name.upper()} ({len(df)} rows) ===")
        if tabulate:
            print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
        else:
            print(df.to_string(index=False))


def main():
    """
    Generates, inserts sample data, and returns a dict of pandas DataFrames.
    """
    global tables

    client = get_client()
    db     = client[DB_NAME]
    now    = datetime.datetime.utcnow()

    # Clear old data
    clear_collections(db)

    # Generate
    users       = generate_users(now)
    instructors = [u for u in users if u["role"] == "instructor"]
    students    = [u for u in users if u["role"] == "student"]
    courses     = generate_courses(now, instructors)
    enrollments = generate_enrollments(now, students, courses)
    lessons     = generate_lessons(now, courses)
    assignments = generate_assignments(now, courses)
    submissions = generate_submissions(now, assignments, students)

    # Insert into MongoDB
    try:
        db.users.insert_many(users)
        db.courses.insert_many(courses)
        db.enrollments.insert_many(enrollments)
        db.lessons.insert_many(lessons)
        db.assignments.insert_many(assignments)
        db.submissions.insert_many(submissions)
        print("[OK] Sample data inserted.")
    except errors.PyMongoError as e:
        print(f"[ERROR] Inserting data failed: {e}")
        sys.exit(1)

    # Build DataFrames
    tables = {
        "users":       pd.DataFrame(users),
        "courses":     pd.DataFrame(courses),
        "enrollments": pd.DataFrame(enrollments),
        "lessons":     pd.DataFrame(lessons),
        "assignments": pd.DataFrame(assignments),
        "submissions": pd.DataFrame(submissions),
    }

    # Print tables if script
    if __name__ == "__main__":
        print_tables(tables)

    return tables


if __name__ == "__main__":
    main()
