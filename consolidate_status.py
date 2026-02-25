import pandas as pd
import os

def consolidate_status():
    """
    Consolidates 'Status of Learners/participant_status.xlsx' from 'Cloud Training' and 'PowerBI Training'.
    """
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Module 8 Data")
    output_dir_master = os.path.join(base_dir, "Consolidated Data")
    
    target_dirs = ["Cloud Training", "PowerBI Training"]
    all_dfs = []
    
    print(f"Starting Status consolidation from base directory: {base_dir}")
    print("-" * 50)
    
    for training_type in target_dirs:
        # Path to specific excel file
        file_path = os.path.join(base_dir, training_type, "Status of Learners", "participant_status.xlsx")
        
        if os.path.exists(file_path):
            try:
                print(f"Processing: {training_type} -> {file_path}")
                df = pd.read_excel(file_path)
                
                # Add Metadata
                df['Training Type'] = training_type
                df['Source File'] = "participant_status.xlsx"
                
                all_dfs.append(df)
                print(f"  -> Loaded {len(df)} rows.")
            except Exception as e:
                print(f"  Error reading {file_path}: {e}")
        else:
            print(f"Warning: File not found - {file_path}")

    # Process Master File
    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        
        if not os.path.exists(output_dir_master):
            os.makedirs(output_dir_master)
            
        output_file_master = os.path.join(output_dir_master, "Status_of_Learners.csv")
        final_df.to_csv(output_file_master, index=False)
        
        print(f"\nSUCCESS: Consolidated Status file saved to: {output_file_master}")
        print(f"Total Records: {len(final_df)}")
    else:
        print("\nWARNING: No Status data found to consolidate.")

if __name__ == "__main__":
    consolidate_status()
