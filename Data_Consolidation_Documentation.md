# Data Consolidation Documentation for Dare Careers Power BI Dashboard

## Project Preamble
Dare Careers provides training in Power BI and AWS Cloud. To monitor student progress, a comprehensive Power BI dashboard will track key metrics:
- Daily Zoom attendance records
- Daily participation
- Weekly quiz and lab grades
- Learner status (graduation and certification)

The original raw data was organized in tracking folders (`Cloud Training` and `PowerBI Training`), each containing sub-folders for specific metrics across a 10-week period.

## Consolidation Target
All consolidated files used for Power BI modeling are saved in the `Module 8 Data\Consolidated Data` directory. The following scripts process the raw data and produce standard CSVs for importing to Power BI.

---

## 1. Zoom Attendance Consolidation (`consolidate_zoom.py`)

### Logic and Rules
- Processes daily attendance `.csv` files stored under the `Zoom Attendance` directory for both tracks across Week 1 to Week 10.
- Calculates total duration for each learner per session. The `Leave Time` is subtracted from the `Join Time` to determine the total minutes spent in class.
- **Attendance Condition enforced:** A learner is marked as **"Attended"** if out of the total duration calculated, the time spent is **greater than 30 minutes**. Otherwise, it's logged as **"Not Attended"**.

### Output File
- `Consolidated Data\Zoom_Attendance.csv`
- Total Master Records generated: `7000 rows`
- Columns added: `Week`, `Training Type`, `Source File`, `Date`, and `Attendance Status`.

---

## 2. Labs and Quizzes Consolidation (`consolidate_labs.py`)

### Logic and Rules
- Processes `labs_and_quizzes.xlsx` files for both tracks.
- Transforms the wide-format structure (with separate columns for Week 1 to Week 10) into a clean, **long-format** structure better suited for Power BI modeling.
- Adds metadata columns to distinguish the Training Type.

### Output File
- `Consolidated Data\Labs_and_Quizzes.csv`
- Total Records generated: `1400 rows`
- Key Columns: `email`, `Training Type`, `Source File`, `Week`, `Score`

---

## 3. Participation Consolidation (`consolidate_participation.py`)

### Logic and Rules
- Consolidates the `participation.xlsx` files from both tracks.
- Appends training type tags and standardizes the structure for calculating the participation rate metrics inside Power BI.

### Output File
- `Consolidated Data\Participation.csv`
- Total Records generated: `100 rows`

---

## 4. Learner Status Consolidation (`consolidate_status.py`)

### Logic and Rules
- Consolidates the `participant_status.xlsx` configuration file from both tracks.
- This dataset tracks the final results: certification and graduation status for the learners, matching the expected output required for measuring completion, certification, and drop-out rates.

### Output File
- `Consolidated Data\Status_of_Learners.csv`
- Total Records generated: `140 rows`

---

## 5. Automated Data Validation (`validate_consolidation.py`)

### Process Checklist 
The data processing pipeline includes an automated validation script which:
- Confirms the resulting generated `Consolidated Data` files exist.
- Parses `Zoom_Attendance.csv` and cross-verifies group row counts per Training Type and Week compared to the initial raw data inputs.
- Verifies unique training types inside the generated Excel conversions.

*Validation check successfully confirmed that 7,000 attendance records perfectly mirrored the un-consolidated raw `.csv` counts.*

## Next Steps for Power BI
1. Connect Power BI to the `Module 8 Data\Consolidated Data` directory.
2. Build data relationships based on unique identifiers (e.g., Email addresses).
3. Utilize `Attendance Status` column for all class presence calculations.
4. Utilize `Score` in the Labs CSV for assessment averaging (per cohort and per learner).
5. Deploy `DAX` formulas to count Certificates, Graduations, and Drop-outs dynamically based on the filters requested in the dashboard requirement documentation.
