import pandas as pd
import os

def consolidate_attendance():
    """
    Consolidates Zoom attendance CSV files from 'Cloud Training' and 'PowerBI Training'
    directories.
    
    Logic:
    1. Iterate through each training folder.
    2. Collect all Week files for that training.
    3. Save individual consolidated file and report week count.
    4. Collect all data for master consolidation.
    """
    
    # 1. Define Paths
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Module 8 Data")
    output_dir_master = os.path.join(base_dir, "Consolidated Data")
    
    target_dirs = ["Cloud Training", "PowerBI Training"]
    all_dfs = [] # For master file
    
    print(f"Starting Zoom consolidation from base directory: {base_dir}")
    print("-" * 50)
    
    # 2. Iterate through target directories
    for training_type in target_dirs:
        training_path = os.path.join(base_dir, training_type, "Zoom Attendance")
        training_dfs = [] # For individual training file
        
        if not os.path.exists(training_path):
            print(f"Warning: Directory not found - {training_path}")
            continue
            
        print(f"Processing: {training_type}...")
        
        # 3. Walk through the directory structure
        for root, dirs, files in os.walk(training_path):
            folder_name = os.path.basename(root)
            
            if folder_name.lower().startswith("week"):
                week_val = folder_name # e.g., "Week 3"
                
                for file in files:
                    if file.endswith(".csv"):
                        file_path = os.path.join(root, file)
                        
                        try:
                            # 4. Read and Transform
                            df = pd.read_csv(file_path)
                            
                            # Add Metadata Columns
                            df['Week'] = week_val
                            df['Training Type'] = training_type
                            df['Source File'] = file
                            
                            # Extract date from filename (e.g., '05-Aug-2024.csv' -> '2024-08-05')
                            date_str = os.path.splitext(file)[0]
                            try:
                                df['Date'] = pd.to_datetime(date_str).dt.date
                            except Exception:
                                df['Date'] = date_str
                                
                            # Convert Join/Leave Time to datetime (robustly parsing mixed formats)
                            for col in ['Join Time', 'Leave Time']:
                                df[col] = pd.to_datetime(df[col], errors='coerce')

                            # Calculate duration in minutes (Leave - Join)
                            duration_series = (df['Leave Time'] - df['Join Time']).dt.total_seconds() / 60
                            
                            # Logic: If duration > 30 min -> Attended
                            df['Attendance Status'] = duration_series.apply(lambda x: 'Attended' if x > 30 else 'Not Attended')
                            
                        except Exception as e:
                            print(f"    Error reading/transforming {file}: {e}")
                            df['Attendance Status'] = 'Unknown'
                            
                        training_dfs.append(df)

        # 5. Process Individual Training Data
        if training_dfs:
            training_final_df = pd.concat(training_dfs, ignore_index=True)
            
            # Calculate Week Count
            unique_weeks = training_final_df['Week'].nunique()
            weeks_list = sorted(training_final_df['Week'].unique())
            
            # Save Individual File to its Zoom Attendance folder
            output_file_training = os.path.join(training_path, f"{training_type.replace(' ', '_')}_Attendance.csv")
            training_final_df.to_csv(output_file_training, index=False)
            
            print(f"  -> Saved {training_type} data to: {output_file_training}")
            print(f"  -> Combined {unique_weeks} weeks: {', '.join(weeks_list)}")
            print(f"  -> Total Rows: {len(training_final_df)}")
            
            # Add to master list
            all_dfs.append(training_final_df)
        else:
            print(f"  -> No data found for {training_type}")
        
        print("-" * 50)

    # 6. Process Master File
    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        
        if not os.path.exists(output_dir_master):
            os.makedirs(output_dir_master)
            
        output_file_master = os.path.join(output_dir_master, "Zoom_Attendance.csv")
        final_df.to_csv(output_file_master, index=False)
        
        print(f"\nSUCCESS: Consolidated master file saved to: {output_file_master}")
        print(f"Total Master Records: {len(final_df)}")
    else:
        print("\nWARNING: No data found to consolidate.")

if __name__ == "__main__":
    consolidate_attendance()
