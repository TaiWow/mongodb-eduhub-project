
"""
part3_crud.py

Part 3: Basic CRUD Operations for the EduHub e-learning platform.
- CREATE: add student, create course, enroll student, add lesson
- READ: list active students; course details + instructor; courses by category;
        students in a course; search courses by title
- UPDATE: update user profile; publish course; update submission grade; add course tags
- DELETE: soft-delete user; remove enrollment; delete lesson
- When run as a script: prints results as ASCII tables via tabulate
- When imported in a notebook: each function returns a pandas DataFrame for rich display
"""

import datetime
import sys

from pymongo import errors
from part1_setup import get_client, DB_NAME
import pandas as pd

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


def print_table(df: pd.DataFrame, title: str):
    """Print a single DataFrame as an ASCII table with a title."""
    print(f"\n=== {title} ({len(df)} row{'s' if len(df)!=1 else ''}) ===")
    if tabulate:
        print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
    else:
        print(df.to_string(index=False))


# === CREATE ===

def create_student(db, userId, email, firstName, lastName, profile=None):
    now = datetime.datetime.utcnow()
    doc = {
        "userId": userId,
        "email": email,
        "firstName": firstName,
        "lastName": lastName,
        "role": "student",
        "dateJoined": now,
        "profile": profile or {"bio": "", "avatar": "", "skills": []},
        "isActive": True
    }
    db.users.insert_one(doc)
    return pd.DataFrame([doc])


def create_course(db, courseId, title, instructorId, category, level, duration, price, tags=None):
    now = datetime.datetime.utcnow()
    doc = {
        "courseId": courseId,
        "title": title,
        "description": "",
        "instructorId": instructorId,
        "category": category,
        "level": level,
        "duration": duration,
        "price": price,
        "tags": tags or [],
        "rating": 0.0,
        "ratingsCount": 0,
        "createdAt": now,
        "updatedAt": now,
        "isPublished": False
    }
    db.courses.insert_one(doc)
    return pd.DataFrame([doc])


def enroll_student(db, enrollmentId, userId, courseId):
    now = datetime.datetime.utcnow()
    doc = {
        "enrollmentId": enrollmentId,
        "userId": userId,
        "courseId": courseId,
        "enrolledAt": now,
        "progress": 0,
        "completionStatus": "in progress"
    }
    db.enrollments.insert_one(doc)
    return pd.DataFrame([doc])


def add_lesson(db, lessonId, courseId, title, content, order):
    now = datetime.datetime.utcnow()
    doc = {
        "lessonId": lessonId,
        "courseId": courseId,
        "title": title,
        "content": content,
        "order": order,
        "createdAt": now,
        "updatedAt": now
    }
    db.lessons.insert_one(doc)
    return pd.DataFrame([doc])


# === READ ===

def get_active_students(db):
    cursor = db.users.find({"role": "student", "isActive": True})
    return pd.DataFrame(list(cursor))


def get_course_details(db, courseId):
    course = db.courses.find_one({"courseId": courseId})
    instr = db.users.find_one({"userId": course["instructorId"]})
    if not course or not instr:
        return pd.DataFrame()
    # flatten into one record
    record = {
        **{k: course[k] for k in ["courseId", "title", "category", "level", "isPublished"]},
        "instructorFirstName": instr["firstName"],
        "instructorLastName": instr["lastName"]
    }
    return pd.DataFrame([record])


def get_courses_by_category(db, category):
    cursor = db.courses.find({"category": category})
    return pd.DataFrame(list(cursor))


def get_students_in_course(db, courseId):
    cursor = db.enrollments.aggregate([
        {"$match": {"courseId": courseId}},
        {"$lookup": {
            "from": "users",
            "localField": "userId",
            "foreignField": "userId",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$project": {
            "_id": 0,
            "enrollmentId": 1,
            "userId": 1,
            "firstName": "$user.firstName",
            "lastName": "$user.lastName",
            "progress": 1,
            "completionStatus": 1
        }}
    ])
    return pd.DataFrame(list(cursor))


def search_courses_by_title(db, keyword):
    regex = {"$regex": keyword, "$options": "i"}
    cursor = db.courses.find({"title": regex})
    return pd.DataFrame(list(cursor))


# === UPDATE ===

def update_user_profile(db, userId, profile_updates):
    db.users.update_one(
        {"userId": userId},
        {"$set": {f"profile.{k}": v for k, v in profile_updates.items()}}
    )
    doc = db.users.find_one({"userId": userId})
    return pd.DataFrame([doc]) if doc else pd.DataFrame()


def publish_course(db, courseId):
    now = datetime.datetime.utcnow()
    db.courses.update_one(
        {"courseId": courseId},
        {"$set": {"isPublished": True, "updatedAt": now}}
    )
    doc = db.courses.find_one({"courseId": courseId})
    return pd.DataFrame([doc]) if doc else pd.DataFrame()


def update_submission_grade(db, submissionId, grade):
    db.submissions.update_one(
        {"submissionId": submissionId},
        {"$set": {"grade": grade}}
    )
    doc = db.submissions.find_one({"submissionId": submissionId})
    return pd.DataFrame([doc]) if doc else pd.DataFrame()


def add_course_tags(db, courseId, tags):
    db.courses.update_one(
        {"courseId": courseId},
        {"$addToSet": {"tags": {"$each": tags}}}
    )
    doc = db.courses.find_one({"courseId": courseId})
    return pd.DataFrame([doc]) if doc else pd.DataFrame()


# === DELETE ===

def soft_delete_user(db, userId):
    db.users.update_one(
        {"userId": userId},
        {"$set": {"isActive": False}}
    )
    doc = db.users.find_one({"userId": userId})
    return pd.DataFrame([doc]) if doc else pd.DataFrame()


def remove_enrollment(db, enrollmentId):
    db.enrollments.delete_one({"enrollmentId": enrollmentId})
    # return any leftover rows (should be empty)
    cursor = db.enrollments.find({"enrollmentId": enrollmentId})
    return pd.DataFrame(list(cursor))


def delete_lesson(db, lessonId):
    db.lessons.delete_one({"lessonId": lessonId})
    cursor = db.lessons.find({"lessonId": lessonId})
    return pd.DataFrame(list(cursor))


# === DEMONSTRATION MAIN ===

def main():
    client = get_client()
    db = client[DB_NAME]

    # -- CREATE --
    new_student = create_student(db, "u9999", "newstudent@example.com", "New", "Student")
    new_course  = create_course(db, "c9999", "Test Course", "u2001", "Testing", "beginner", 3.0, 0.0, ["test"])
    new_enroll  = enroll_student(db, "e9999", "u9999", "c9999")
    new_lesson  = add_lesson(db, "l9999", "c9999", "Intro Lesson", "Welcome!", 1)

    # -- READ --
    active_students      = get_active_students(db)
    course_details       = get_course_details(db, "c9999")
    courses_in_testing   = get_courses_by_category(db, "Testing")
    students_in_test     = get_students_in_course(db, "c9999")
    search_results       = search_courses_by_title(db, "Test")

    # -- UPDATE --
    updated_profile      = update_user_profile(db, "u9999", {"bio": "Enthusiastic learner", "skills": ["Testing", "Debugging"]})
    published_course     = publish_course(db, "c9999")
    updated_submission   = update_submission_grade(db, "s6001", 88)  # s6001 from part2
    updated_course_tags  = add_course_tags(db, "c9999", ["newtag", "test"])

    # -- DELETE --
    soft_deleted_user    = soft_delete_user(db, "u9999")
    post_delete_enroll   = remove_enrollment(db, "e9999")
    deleted_lesson_check = delete_lesson(db, "l9999")

    # Gather for printing
    results = {
        "Created Student": new_student,
        "Created Course": new_course,
        "Created Enrollment": new_enroll,
        "Created Lesson": new_lesson,
        "Active Students": active_students,
        "Course Details": course_details,
        "Courses in 'Testing'": courses_in_testing,
        "Students in 'c9999'": students_in_test,
        "Search 'Test'": search_results,
        "Updated Profile": updated_profile,
        "Published Course": published_course,
        "Updated Submission s6001": updated_submission,
        "Added Course Tags": updated_course_tags,
        "Soft-deleted User": soft_deleted_user,
        "Post-delete Enrollment e9999": post_delete_enroll,
        "Deleted Lesson l9999": deleted_lesson_check
    }

    for title, df in results.items():
        print_table(df, title)


if __name__ == "__main__":
    main()
