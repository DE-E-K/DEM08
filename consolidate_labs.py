import pandas as pd
import os

def consolidate_labs():
    """
    Consolidates 'Labs & Quizes/labs & quizzes.xlsx' from 'Cloud Training' and 'PowerBI Training'.
    """
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Module 8 Data")
    output_dir_master = os.path.join(base_dir, "Consolidated Data")
    
    target_dirs = ["Cloud Training", "PowerBI Training"]
    all_dfs = []
    
    print(f"Starting Labs consolidation from base directory: {base_dir}")
    print("-" * 50)
    
    for training_type in target_dirs:
        # Path to specific excel file
        file_name = "labs_and_quizzes.xlsx"
        # Note: Folder is "Labs & Quizes"
        file_path = os.path.join(base_dir, training_type, "Labs & Quizes", file_name)
        
        if os.path.exists(file_path):
            try:
                print(f"Processing: {training_type} -> {file_path}")
                df = pd.read_excel(file_path)
                
                # Add Metadata
                df['Training Type'] = training_type
                df['Source File'] = "labs and quizzes.xlsx"

                # Transform to Long Format
                # Identify columns that start with "Week"
                week_columns = [col for col in df.columns if col.startswith("Week")]
                
                # Melt the dataframe
                df_long = df.melt(
                    id_vars=['email', 'Training Type', 'Source File'], 
                    value_vars=week_columns,
                    var_name='Week', 
                    value_name='Score'
                )
                
                all_dfs.append(df_long)
                print(f"Loaded {len(df_long)} rows (Long Format).")
            except Exception as e:
                print(f"rror reading {file_path}: {e}")
        else:
            print(f"Warning: File not found - {file_path}")

    # Process Master File
    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        
        if not os.path.exists(output_dir_master):
            os.makedirs(output_dir_master)
            
        output_file_master = os.path.join(output_dir_master, "Labs_and_Quizzes.csv")
        final_df.to_csv(output_file_master, index=False)
        
        print(f"\nSUCCESS: Consolidated Labs file saved to: {output_file_master}")
        print(f"Total Records (Long Format): {len(final_df)}")
    else:
        print("\nWARNING: No Labs data found to consolidate.")

if __name__ == "__main__":
    consolidate_labs()
