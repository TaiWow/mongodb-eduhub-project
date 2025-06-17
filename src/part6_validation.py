#!/usr/bin/env python3
"""
part6_validation.py

Part 6: Data Validation & Error Handling for the EduHub e-learning platform.

Task 6.1: Schema Validation  
- Enforced via JSON Schema validators on each collection (see part1_setup.py):
  * Required fields
  * Data type checks
  * Enum restrictions
  * Email format via regex

Task 6.2: Error Handling  
- Demonstrate catching:
  * DuplicateKeyError on unique fields
  * WriteError for missing required fields
  * WriteError for invalid data types
  * WriteError for invalid enum values
  * WriteError for invalid email format
"""

import datetime
from pymongo import errors
from src.part1_setup import get_client, setup_database, DB_NAME
import pandas as pd


def setup_unique_indexes(db):
    """Add unique indexes to enforce duplicate-key constraints."""
    idxs = [
        ("users", [("userId", 1)], {"unique": True, "name": "uix_users_userId"}),
        ("users", [("email", 1)], {"unique": True, "name": "uix_users_email"}),
    ]
    for coll_name, fields, opts in idxs:
        try:
            db[coll_name].create_index(fields, **opts)
        except errors.PyMongoError:
            pass  # ignore if already exists


def test_duplicate_key(db):
    """Insert the same user twice to trigger DuplicateKeyError."""
    user = {
        "userId": "udup",
        "email": "dup@example.com",
        "firstName": "Dup",
        "lastName": "User",
        "role": "student",
        "dateJoined": datetime.datetime.utcnow(),
        "profile": {"bio": "", "avatar": "", "skills": []},
        "isActive": True
    }
    try:
        db.users.insert_one(user)
        db.users.insert_one(user)
        return "Error: duplicate insertion allowed"
    except errors.DuplicateKeyError as e:
        return f"DuplicateKeyError caught: {e.details.get('errmsg','')}"
    except Exception as e:
        return f"Unexpected error ({type(e).__name__}): {e}"


def test_missing_required(db):
    """Omit required field 'email' to trigger WriteError."""
    user = {
        "userId": "umiss",
        # email missing
        "firstName": "Missing",
        "lastName": "Email",
        "role": "student",
        "dateJoined": datetime.datetime.utcnow(),
        "profile": {"bio": "", "avatar": "", "skills": []},
        "isActive": True
    }
    try:
        db.users.insert_one(user)
        return "Error: missing required field allowed"
    except errors.WriteError as e:
        return f"WriteError caught (missing field): {e.details.get('errmsg','')}"
    except Exception as e:
        return f"Unexpected error ({type(e).__name__}): {e}"


def test_invalid_type(db):
    """Provide dateJoined as string to trigger WriteError for type mismatch."""
    user = {
        "userId": "utype",
        "email": "type@example.com",
        "firstName": "Type",
        "lastName": "Error",
        "role": "student",
        "dateJoined": "not-a-date",
        "profile": {"bio": "", "avatar": "", "skills": []},
        "isActive": True
    }
    try:
        db.users.insert_one(user)
        return "Error: invalid type allowed"
    except errors.WriteError as e:
        return f"WriteError caught (invalid type): {e.details.get('errmsg','')}"
    except Exception as e:
        return f"Unexpected error ({type(e).__name__}): {e}"


def test_invalid_enum(db):
    """Give role='admin' (not in ['student','instructor']) to trigger WriteError."""
    user = {
        "userId": "uenum",
        "email": "enum@example.com",
        "firstName": "Enum",
        "lastName": "Error",
        "role": "admin",  # invalid enum
        "dateJoined": datetime.datetime.utcnow(),
        "profile": {"bio": "", "avatar": "", "skills": []},
        "isActive": True
    }
    try:
        db.users.insert_one(user)
        return "Error: invalid enum allowed"
    except errors.WriteError as e:
        return f"WriteError caught (invalid enum): {e.details.get('errmsg','')}"
    except Exception as e:
        return f"Unexpected error ({type(e).__name__}): {e}"


def test_invalid_email_format(db):
    """Provide email without '@' to trigger WriteError via regex."""
    user = {
        "userId": "uemail",
        "email": "not-an-email",
        "firstName": "Email",
        "lastName": "Error",
        "role": "student",
        "dateJoined": datetime.datetime.utcnow(),
        "profile": {"bio": "", "avatar": "", "skills": []},
        "isActive": True
    }
    try:
        db.users.insert_one(user)
        return "Error: invalid email format allowed"
    except errors.WriteError as e:
        return f"WriteError caught (invalid email): {e.details.get('errmsg','')}"
    except Exception as e:
        return f"Unexpected error ({type(e).__name__}): {e}"


def main():
    """
    Recreate collections with JSON Schema, add unique indexes,
    then run each validation test and return results.
    """
    client = get_client()
    setup_database(client)        # reapply JSON Schema validators
    db = client[DB_NAME]
    setup_unique_indexes(db)      # enforce duplicate-key constraints

    tests = {
        "Duplicate Key": test_duplicate_key(db),
        "Missing Required Field": test_missing_required(db),
        "Invalid Data Type": test_invalid_type(db),
        "Invalid Enum Value": test_invalid_enum(db),
        "Invalid Email Format": test_invalid_email_format(db)
    }

    # If run as script, print nicely
    if __name__ == "__main__":
        df = pd.DataFrame(
            list(tests.items()),
            columns=["Test", "Result"]
        )
        print("\nValidation & Error Handling Tests\n")
        print(df.to_string(index=False))
    return tests


if __name__ == "__main__":
    main()
