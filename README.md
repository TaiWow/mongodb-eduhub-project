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
11. [Results & Visualizations](#results--visualizations)
12. [Repository Structure](#repository-structure)
13. [License & Contact](#license--contact)

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



*Comprehensive portfolio README with clickable links to all key files and visuals.*
EduHub E-Learning Platform Project
Brief Description: EduHub is a MongoDB-backed e-learning platform that allows users to register as students or instructors, create and enroll in courses, submit assignments, and track performance metrics. This repository contains sections covering setup, CRUD operations, advanced queries, indexing & performance optimization, schema validation, and analytical reporting.
Table of Contents
1. Project Setup
2. Part 1: Database Initialization
3. Part 2: CRUD Operations
4. Part 3: Advanced Queries & Reporting
5. Part 4: Schema Validation & Error Handling
6. Part 5: Indexing & Performance Optimization
    * Performance Analysis
7. Part 6: Analytical Dashboards & Export
8. Sample Data JSON
9. Schema Validation JSON
10. License

Project Setup
1. Clone the repository git clone <REPOSITORY_URL>
2. cd eduhub-mongodb-project
3. 
4. Install dependencies pip install -r requirements.txt
5. 
6. Configure environment
    * Ensure MongoDB is running locally on mongodb://localhost:27017 or set MONGO_URI in part1_setup.py.
7. Initialize database python part1_setup.py
8. 

Part 1: Database Initialization
Source: part1_setup.py
* Connects to MongoDB
* Creates eduhub_db and collections
* Sets up sample documents

Part 2: CRUD Operations
Source: part2_crud.py
* Create, Read, Update, Delete functions for users, courses, enrollments, lessons, assignments, and submissions
* Sample usage in Jupyter notebook notebooks/part2_crud_demo.ipynb

Part 3: Advanced Queries & Reporting
Source: part3_queries.py
* Joins across collections using aggregation pipelines
* Reports: enrollment stats, completion rates, instructor analytics
* Demo notebook: notebooks/part3_reporting.ipynb

Part 4: Schema Validation & Error Handling
Source: schema_validation.json
* JSON Schema validators for each collection
* Automatic enforcement of required fields, types, enums, and patterns
* Error handling tests in tests/test_validation.py

Part 5: Indexing & Performance Optimization
Source: part5_performance.py
* Task 5.1: Created indexes on users.email, courses.title, courses.category, assignments.dueDate, enrollments.userId, and enrollments.courseId
* Task 5.2: Profiling before/after indexes, capturing server and client timings
Performance Analysis
Refer to Performance Analysis for detailed results, summary table, and recommendations.

Part 6: Analytical Dashboards & Export
Source: part6_dashboards.py
* Generates aggregated metrics for dashboards (monthly enrollments, popular categories, student performance)
* Exports results to CSV and JSON for visualization
* See notebooks/part6_dashboards.ipynb for interactive charts

Sample Data JSON
data/sample_data.json contains exported sample documents for all collections.

Schema Validation JSON
data/schema_validation.json contains JSON Schema definitions applied to collections.

License
This project is licensed under the MIT License.

& publishing
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

![Entity Relationship Diagram](docs/images/er_diagram.png)

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
5. **Launch Notebook**:
   [notebooks/eduhub\_mongodb\_project.ipynb](notebooks/eduhub_mongodb_project.ipynb)
6. **Run Python script**:

   ```bash
   python src/eduhub_queries.py
   ```


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

## 11. Results & Visualizations

### Active Students

### Performance Comparison

Additional screenshots: [`docs/images/`](docs/images/).

---

## 12. Repository Structure

* [README.md](README.md)
* [notebooks/eduhub\_mongodb\_project.ipynb](notebooks/eduhub_mongodb_project.ipynb)
* [src/eduhub\_queries.py](src/eduhub_queries.py)
* [data/sample\_data.json](data/sample_data.json)
* [data/schema\_validation.json](data/schema_validation.json)
* [docs/performance\_analysis.md](docs/performance_analysis.md)
* [docs/test\_results.md](docs/test_results.md)
* [docs/presentation.pptx](docs/presentation.pptx)
* [docs/images/er\_diagram.png](docs/images/er_diagram.png)
* [docs/images/active\_students.png](docs/images/active_students.png)
* [docs/images/performance\_chart.png](docs/images/performance_chart.png)
* [LICENSE](LICENSE)
* [.gitignore](.gitignore)

---

## 13. License & Contact

Licensed under the **MIT License** — see [LICENSE](LICENSE).

Maintainer: Your Name ([youremail@example.com](mailto:youremail@example.com))

*Comprehensive portfolio README with clickable links to all key files and visuals.*
# EduHub MongoDB Project

&#x20;

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
11. [Results & Visualizations](#results--visualizations)
12. [Repository Structure](#repository-structure)
13. [License & Contact](#license--contact)

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

## 8. Core Features & CRUD Operations



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

