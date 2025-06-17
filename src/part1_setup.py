
"""
part1_setup.py

Part 1: Database Setup & Data Modeling for the EduHub e-learning platform.
- Creates collections with JSON Schema validation (including rating fields).
- Defines sample documents and exposes them as pandas DataFrames.
- Can be run in terminal (prints ASCII tables) or imported in a notebook (returns DataFrames).
"""

import sys
import datetime

from pymongo import MongoClient, errors
import pandas as pd

# Optional: for prettier terminal tables
try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

# Configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "eduhub_db"


def get_client(uri: str = MONGO_URI) -> MongoClient:
    """Establish and return a MongoClient, exiting on failure."""
    try:
        client = MongoClient(uri)
        client.server_info()  # verify connection
        return client
    except errors.PyMongoError as e:
        print(f"[ERROR] Could not connect to MongoDB: {e}")
        sys.exit(1)


def setup_database(client: MongoClient = None):
    """
    Drop existing collections (if any) and recreate them with JSON Schema validation.
    """
    client = client or get_client()
    db = client[DB_NAME]

    schemas = {
        "users": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["userId", "email", "firstName", "lastName", "role", "dateJoined", "isActive"],
                "properties": {
                    "userId":    {"bsonType": "string"},
                    "email":     {"bsonType": "string", "pattern": r"^.+@.+\..+$"},
                    "firstName": {"bsonType": "string"},
                    "lastName":  {"bsonType": "string"},
                    "role":      {"enum": ["student", "instructor"]},
                    "dateJoined":{"bsonType": "date"},
                    "profile": {
                        "bsonType": "object",
                        "properties": {
                            "bio":    {"bsonType": "string"},
                            "avatar": {"bsonType": "string"},
                            "skills": {
                                "bsonType": "array",
                                "items":   {"bsonType": "string"}
                            }
                        }
                    },
                    "isActive":  {"bsonType": "bool"}
                }
            }
        },
        "courses": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["courseId", "title", "instructorId", "level", "createdAt", "isPublished"],
                "properties": {
                    "courseId":     {"bsonType": "string"},
                    "title":        {"bsonType": "string"},
                    "description":  {"bsonType": "string"},
                    "instructorId": {"bsonType": "string"},
                    "category":     {"bsonType": "string"},
                    "level":        {"enum": ["beginner", "intermediate", "advanced"]},
                    "duration":     {"bsonType": "number"},
                    "price":        {"bsonType": "number"},
                    "tags": {
                        "bsonType": "array",
                        "items":   {"bsonType": "string"}
                    },
                    "rating":       {"bsonType": ["double", "int"], "minimum": 0, "maximum": 5},
                    "ratingsCount": {"bsonType": "int",    "minimum": 0},
                    "createdAt":    {"bsonType": "date"},
                    "updatedAt":    {"bsonType": "date"},
                    "isPublished":  {"bsonType": "bool"}
                }
            }
        },
        "enrollments": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["enrollmentId", "userId", "courseId", "enrolledAt", "progress", "completionStatus"],
                "properties": {
                    "enrollmentId":    {"bsonType": "string"},
                    "userId":          {"bsonType": "string"},
                    "courseId":        {"bsonType": "string"},
                    "enrolledAt":      {"bsonType": "date"},
                    "progress":        {"bsonType": "number"},
                    "completionStatus":{"enum": ["in progress", "completed"]}
                }
            }
        },
        "lessons": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["lessonId", "courseId", "title", "order", "createdAt"],
                "properties": {
                    "lessonId":  {"bsonType": "string"},
                    "courseId":  {"bsonType": "string"},
                    "title":     {"bsonType": "string"},
                    "content":   {"bsonType": "string"},
                    "order":     {"bsonType": "number"},
                    "createdAt": {"bsonType": "date"},
                    "updatedAt": {"bsonType": "date"}
                }
            }
        },
        "assignments": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["assignmentId", "courseId", "title", "dueDate", "createdAt"],
                "properties": {
                    "assignmentId":{"bsonType": "string"},
                    "courseId":    {"bsonType": "string"},
                    "title":       {"bsonType": "string"},
                    "description": {"bsonType": "string"},
                    "dueDate":     {"bsonType": "date"},
                    "createdAt":   {"bsonType": "date"},
                    "updatedAt":   {"bsonType": "date"}
                }
            }
        },
        "submissions": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["submissionId", "assignmentId", "userId", "submittedAt"],
                "properties": {
                    "submissionId":{"bsonType": "string"},
                    "assignmentId":{"bsonType": "string"},
                    "userId":      {"bsonType": "string"},
                    "submittedAt": {"bsonType": "date"},
                    "grade":       {"bsonType": "number"},
                    "feedback":    {"bsonType": "string"}
                }
            }
        }
    }

    # Drop & recreate each collection with its validator
    for name, schema in schemas.items():
        if name in db.list_collection_names():
            db.drop_collection(name)
        db.create_collection(
            name,
            validator={"$jsonSchema": schema["$jsonSchema"]},
            validationLevel="strict",
            validationAction="error"
        )
    print("[OK] Collections created with JSON Schema validation.")


def get_sample_docs() -> dict:
    """
    Return one example document per collection as pandas DataFrames.
    In a notebook, simply displaying these DataFrames will render HTML tables.
    """
    now = datetime.datetime.utcnow()
    samples = {
        "users": {
            "userId": "u1001",
            "email": "alice@example.com",
            "firstName": "Alice",
            "lastName": "Anderson",
            "role": "student",
            "dateJoined": now,
            "profile": {"bio": "Data enthusiast", "avatar": "", "skills": ["Python", "MongoDB"]},
            "isActive": True
        },
        "courses": {
            "courseId": "c2001",
            "title": "Intro to Data Engineering",
            "description": "Learn the basics of MongoDB and data pipelines.",
            "instructorId": "u2001",
            "category": "Data Engineering",
            "level": "beginner",
            "duration": 8.5,
            "price": 99.99,
            "tags": ["MongoDB", "ETL"],
            "rating": 0.0,
            "ratingsCount": 0,
            "createdAt": now,
            "updatedAt": now,
            "isPublished": False
        },
        "enrollments": {
            "enrollmentId": "e3001",
            "userId": "u1001",
            "courseId": "c2001",
            "enrolledAt": now,
            "progress": 0,
            "completionStatus": "in progress"
        },
        "lessons": {
            "lessonId": "l4001",
            "courseId": "c2001",
            "title": "Getting Started with MongoDB",
            "content": "Installation and first CRUD ops.",
            "order": 1,
            "createdAt": now,
            "updatedAt": now
        },
        "assignments": {
            "assignmentId": "a5001",
            "courseId": "c2001",
            "title": "Setup Your Database",
            "description": "Install and connect to MongoDB.",
            "dueDate": now + datetime.timedelta(days=7),
            "createdAt": now,
            "updatedAt": now
        },
        "submissions": {
            "submissionId": "s6001",
            "assignmentId": "a5001",
            "userId": "u1001",
            "submittedAt": now + datetime.timedelta(days=1),
            "grade": 0,
            "feedback": ""
        }
    }

    # Convert to DataFrames
    return {name: pd.DataFrame([doc]) for name, doc in samples.items()}


def print_tables(sample_dfs: dict):
    """Print each DataFrame as an ASCII table when running in a terminal."""
    if tabulate:
        for name, df in sample_dfs.items():
            print(f"\n=== {name.upper()} SAMPLE ===")
            print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))
    else:
        for name, df in sample_dfs.items():
            print(f"\n=== {name.upper()} SAMPLE ===")
            print(df.to_string(index=False))


def main():
    client = get_client()
    setup_database(client)
    samples = get_sample_docs()
    print_tables(samples)
    print("\n[Done] Part 1 setup complete.")


if __name__ == "__main__":
    main()
