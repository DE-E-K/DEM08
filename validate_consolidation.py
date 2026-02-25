import pandas as pd
import os

def validate_consolidation():
    """
    Validates the existence and content of consolidated files in 'Module 8 Data/Consolidated Data'.
    Performs raw data count comparison for Zoom Attendance.
    """
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Module 8 Data")
    consol_dir = os.path.join(base_dir, "Consolidated Data")
    
    print("=" * 60)
    print("STARTING AUTOMATED VALIDATION")
    print("=" * 60)

    # 1. Validate Zoom Attendance (Detailed Check)
    zoom_file = os.path.join(consol_dir, "Zoom_Attendance.csv")
    print(f"\nChecking: {os.path.basename(zoom_file)}")
    
    if os.path.exists(zoom_file):
        try:
            df = pd.read_csv(zoom_file)
            print(f"  -> File exists. Rows: {len(df)}")
            print(f"  -> Columns: {list(df.columns)}")
            
            # Grouping check
            print("  -> Summary by Training Type & Week:")
            print(df.groupby(['Training Type', 'Week']).size().to_string())
            
            # Compare with Raw
            print("\n  [Deep Verification] Comparing with Raw Files...")
            raw_count = 0
            targets = ["Cloud Training", "PowerBI Training"]
            
            for target in targets:
                path = os.path.join(base_dir, target, "Zoom Attendance")
                for root, dirs, files in os.walk(path):
                    if "Week" in os.path.basename(root):
                        for file in files:
                            if file.endswith(".csv"):
                                try:
                                    temp_df = pd.read_csv(os.path.join(root, file))
                                    raw_count += len(temp_df)
                                except:
                                    pass
            
            print(f"  -> Total Raw Rows: {raw_count}")
            print(f"  -> Total Consolidated Rows: {len(df)}")
            
            if raw_count == len(df):
                print("MATCH: Data integrity confirmed.")
            else:
                print(f"MISMATCH: Difference of {abs(raw_count - len(df))} rows.")
                
        except Exception as e:
            print(f"Error reading file: {e}")
    else:
        print("File NOT found.")

    # 2. Validate Other Files (Existence & Basic Check)
    other_files = [
        "Labs_and_Quizzes.csv",
        "Participation.csv",
        "Status_of_Learners.csv"
    ]
    
    for filename in other_files:
        file_path = os.path.join(consol_dir, filename)
        print(f"\nChecking: {filename}")
        
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                print(f"\nFile exists. Rows: {len(df)}")
                print(f"\nUnique Training Types: {df['Training Type'].unique().tolist() if 'Training Type' in df.columns else 'Column Missing'}")
                print("Check passed.")
            except Exception as e:
                print(f"\nError reading file: {e}")
        else:
            print("\nFile NOT found. (Run the respective script to generate it)")

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")


if __name__ == "__main__":
    validate_consolidation()
