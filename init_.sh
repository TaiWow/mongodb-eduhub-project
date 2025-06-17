#!/usr/bin/env bash

# Abort on any error or use of undefined variable
set -euo pipefail

PROJECT_ROOT="mongodb-eduhub-project"

# Create directory structure
mkdir -p "${PROJECT_ROOT}/notebooks" \
         "${PROJECT_ROOT}/src" \
         "${PROJECT_ROOT}/data" \
         "${PROJECT_ROOT}/docs"

# Create empty files
touch "${PROJECT_ROOT}/README.md"
touch "${PROJECT_ROOT}/notebooks/eduhub_mongodb_project.ipynb"
touch "${PROJECT_ROOT}/src/eduhub_queries.py"
touch "${PROJECT_ROOT}/data/sample_data.json"
touch "${PROJECT_ROOT}/data/schema_validation.json"
touch "${PROJECT_ROOT}/docs/performance_analysis.md"
touch "${PROJECT_ROOT}/docs/presentation.pptx"
