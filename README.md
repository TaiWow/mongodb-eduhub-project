# EduHub MongoDB Project

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue)

**AltSchool of Data Engineering Tinyuka 2024 — Second Semester Project Exam**

---

## Table of Contents

1. [Project Brief & Assignment](#project-brief--assignment)
2. [Project Overview](#project-overview)
3. [Technical Stack](#technical-stack)
4. [Architecture Diagram](#architecture-diagram)
5. [Setup & Installation](#setup--installation)
6. [Database Schema & Validation](#database-schema--validation)
7. [Data Population & Sample Data](#data-population--sample-data)
8. [Core Features & CRUD Operations](#core-features--crud-operations)
9. [Advanced Queries & Aggregation](#advanced-queries--aggregation)
10. [Indexing & Performance Optimizations](#indexing--performance-optimizations)

---

## 1. Project Brief & Assignment

You are tasked with building the database backend for **EduHub** – an online learning platform. This assignment consolidates your understanding of MongoDB fundamentals, document design, query optimization, and scalability.

**Requirements:**

* **Collections:** [`users`](#), [`courses`](#), [`enrollments`](#), [`lessons`](#), [`assignments`](#), [`submissions`](#)
* **Operations:**

  * User management (registration, profiles, roles)
  * Course creation & publishing
  * Enrollment tracking & progress
  * Assessments (assignments, submissions, grading)
  * Analytics & reporting (enrollments, performance)
  * Search & discovery (filtering, sorting)
* **Performance:** Efficient queries, indexing, aggregation pipelines
* **Integrity:** Schema validation, referential integrity, error handling
* **Deliverables:**
* **Interactive Notebook:** [eduhub\_mongodb\_project.ipynb](notebooks/eduhub_mongodb_project.ipynb)
* **Python Script:** [eduhub\_queries.py](src/eduhub_queries.py)
* **Documentation:** [README.md](README.md), [performance\_analysis.md](docs/performance_analysis.md), [test\_results.md](docs/test_results.md)
* **Sample Data:** [sample\_data.json](data/sample_data.json)
* **Presentation Slides:** [presentation.pptx](docs/presentation.pptx)

---

## 2. Project Overview

EduHub allows instructors to create courses, students to enroll and complete lessons/assignments, and provides analytics on progress and performance. The backend uses MongoDB (v8+) with Python (`PyMongo`) for all database interactions.

**Goals:**

* Design document schemas with JSON validation
* Populate realistic test data
* Implement CRUD operations via Python functions
* Build aggregation pipelines for analytics
* Optimize performance with indexes and explain plans

---

## 3. Technical Stack

* **Database:** MongoDB v8.0+
* **Client:** MongoDB Compass & Shell
* **Language:** Python 3.9+ (`pymongo`, `pandas`)
* **Notebook:** JupyterLab
* **Visualization:** Markdown & embedded images

---

## 4. Architecture Diagram

*Figure: Collections and relationships in EduHub.*

---

## 5. Setup & Installation

Follow these steps to get started:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/<YourUsername>/mongodb-eduhub-project.git
   cd mongodb-eduhub-project
   ```
2. **Install dependencies**:

   ```bash
   pip install pymongo pandas
   ```
3. **Start MongoDB** (ensure v8+):

   ```bash
   mongod --dbpath /path/to/db
   ```
4. **Import sample data** (optional):

   ```bash
   mongoimport --db eduhub_db --collection users --file data/sample_data.json --jsonArray
   # Repeat for courses, enrollments, lessons, assignments, submissions
   ```
5. **Launch Notebook**: [notebooks/eduhub\_mongodb\_project.ipynb](notebooks/eduhub_mongodb_project.ipynb)
6. **Run Python script**:

   ```bash
   python src/eduhub_queries.py
   ```

---

## 6. Database Schema & Validation

Validation rules in [`data/schema_validation.json`](data/schema_validation.json) enforce structure for each collection. Example for `users`:

```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["userId","email","firstName","lastName","role"],
    "properties": {
      "email": {"bsonType": "string", "pattern": "^.+@.+$"},
      "role": {"enum": ["student","instructor"]},
      "dateJoined": {"bsonType": "date"}
    }
  }
}
```

Full schemas: [`schema_validation.json`](data/schema_validation.json).

---

## 7. Data Population & Sample Data

Inserted data: 20 users, 8 courses, 15 enrollments, 25 lessons, 10 assignments, 12 submissions. Exported sample data available at:

* [`data/sample_data.json`](data/sample_data.json)

---

## 8. Core Features & CRUD Operations

Implemented in [`src/eduhub_queries.py`](src/eduhub_queries.py):

* **Create:** `add_user()`, `create_course()`, `enroll_student()`, `add_lesson()`
* **Read:** `get_active_students()`, `get_course_details()`, `get_courses_by_category()`, `find_enrolled_students()`, `search_courses()`
* **Update:** `update_user_profile()`, `publish_course()`, `update_assignment_grade()`, `add_course_tags()`
* **Delete:** `soft_delete_user()`, `delete_enrollment()`, `remove_lesson()`

Full code with comments: [eduhub\_queries.py](src/eduhub_queries.py).

---

## 9. Advanced Queries & Aggregation

Pipelines in the notebook ([Part 4](notebooks/eduhub_mongodb_project.ipynb)):

* **Enrollment Stats:** total enrollments per course, avg ratings, grouped by category
* **Student Performance:** avg grade, completion rates, top performers
* **Instructor Analytics:** students taught, revenue, avg ratings
* **Trends:** monthly enrollments, popular categories, engagement metrics

---

## 10. Indexing & Performance Optimizations

Indexes created:

* [`users.email`](#) (unique)
* Compound [`courses.title`](#)[, ](#)[`courses.category`](#)
* [`assignments.dueDate`](#)
* [`enrollments.userId`](#)[, ](#)[`enrollments.courseId`](#)

| Query                            | Before (ms) | After (ms) |
| -------------------------------- | ----------- | ---------- |
| User lookup by email             | 40          | 5          |
| Course search (title & category) | 120         | 15         |
| Enrollment aggregation           | 250         | 60         |

Detailed performance analysis: [docs/performance\_analysis.md](docs/performance_analysis.md).

---

