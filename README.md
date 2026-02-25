># DEM08: Tracking Student Progress and Performance: Dare Careers

## Project Overview
This project provides a set of Python scripts to consolidate tracking data from Moodle and Zoom for "Cloud Training" and "PowerBI Training". The goal is to aggregate scattered Excel and CSV files into a unified format for easier analysis to be used in the final report Ms Power BI.

## Environment Setup
It is recommended to use a virtual environment to manage dependencies.

### Windows
```bash
# Create virtual environment if python is not working replace it by py
python -m venv .venv 

# Activate virtual environment
.venv\Scripts\activate
```

### macOS/Linux
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

## Prerequisites
Ensure a Python environment is set up with the following libraries installed:
*   `pandas`
*   `openpyxl`

You can install them via pip:
```bash
pip install pandas openpyxl
```

## Folder Structure
*   **`Module 8 Data/`**: Input directory containing the raw data folders (`Cloud Training`, `PowerBI Training`).
*   **`Module 8 Data/Consolidated Data/`**: Output directory where the consolidated CSV files will be saved.

## Scripts Description

### 1. [consolidate_labs.py](consolidate_labs.py)
*   **Input**: `Labs & Quizes/labs & quizzes.xlsx`
*   **Output**: `Consolidated Data/Labs_and_Quizzes.csv`
*   **Function**: Reads the Excel files, adds 'Training Type' and 'Source File' columns, and combines them.

### 2. [consolidate_participation.py](consolidate_participation.py)
*   **Input**: `Participation/participation.xlsx`
*   **Output**: `Consolidated Data/Participation.csv`
*   **Function**: Consolidates participation tracking data across training types.

### 3. [consolidate_status.py](consolidate_status.py)
*   **Input**: `Status of Learners/participant_status.xlsx`
*   **Output**: `Consolidated Data/Status_of_Learners.csv`
*   **Function**: Consolidates the status of learners (Active, Drop, etc.).

### 4. [consolidate_zoom.py](consolidate_zoom.py)
*   **Input**: `Zoom Attendance/Week X/*.csv`
*   **Output**:
    *   `Consolidated Data/Zoom_Attendance.csv` (Master file)
    *   `Zoom Attendance/Cloud_Training_Attendance.csv` (Intermediate consolidated file)
    *   `Zoom Attendance/PowerBI_Training_Attendance.csv` (Intermediate consolidated file)
*   **Function**: Recursively searches for CSV files in "Week" folders, extracts the week number, adds metadata, and consolidates all records.

### 5. `validate_consolidation.py`
*   **Function**: Checks if the consolidated files exist and performs data integrity checks (e.g., row count comparison between raw and consolidated Zoom data).

## How to Run
You can run the scripts individually from the root directory:

```bash
py consolidate_labs.py
py consolidate_participation.py
py consolidate_status.py
py consolidate_zoom.py
```

To verify the results:
```bash
py validate_consolidation.py
```

## Documentation
For detailed information on the consolidation logic and Power BI integration steps, refer to the [Data Consolidation Documentation](Data_Consolidation_Documentation.md)
