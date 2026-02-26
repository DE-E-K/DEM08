import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def consolidate_labs():
    """
    Consolidates 'Labs & Quizes/labs_and_quizzes.xlsx' from 'Cloud Training' and 'PowerBI Training'.
    Extracts data from 'Labs' and 'Quizzes' sheets, adding a 'marks_type' column.
    """
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Module 8 Data")
    output_dir_master = os.path.join(base_dir, "Consolidated Data")
    
    target_dirs = ["Cloud Training", "PowerBI Training"]
    all_dfs = []
    
    logging.info(f"Starting Labs and Quizzes consolidation from base directory: {base_dir}")
    logging.info("-" * 50)
    
    for training_type in target_dirs:
        # Path to specific excel file
        file_name = "labs_and_quizzes.xlsx"
        # Note: Folder is "Labs & Quizes"
        file_path = os.path.join(base_dir, training_type, "Labs & Quizes", file_name)
        
        if os.path.exists(file_path):
            try:
                logging.info(f"Processing: {training_type} -> {file_path}")
                
                # Reading all sheets
                xls = pd.read_excel(file_path, sheet_name=None)
                
                for sheet_name, df in xls.items():
                    marks_type = ""
                    if "lab" in sheet_name.lower():
                        marks_type = "Lab"
                    elif "quiz" in sheet_name.lower():
                        marks_type = "Quiz"
                    else:
                        logging.warning(f"Skipping sheet '{sheet_name}' as it is not a Lab or Quiz.")
                        continue
                    
                    logging.info(f"Processing sheet: '{sheet_name}' as '{marks_type}'")

                    # Add Metadata
                    # Changing column name to lowercase to match requirements exactly
                    df['training type'] = training_type

                    # Transform to Long Format
                    # Identify columns that start with "Week"
                    week_columns = [col for col in df.columns if col.startswith("Week")]
                    
                    if not week_columns:
                        logging.warning(f"No 'Week' columns found in sheet '{sheet_name}'.")
                        continue
                    
                    # Melt the dataframe
                    df_long = df.melt(
                        id_vars=['email', 'training type'], 
                        value_vars=week_columns,
                        var_name='Week', 
                        value_name='Score'
                    )
                    
                    df_long['marks_type'] = marks_type
                    
                    # Reorder columns to ensure exact matching:
                    # email, training type, Week, marks_type (Quiz or Lab) and Score
                    df_long = df_long[['email', 'training type', 'Week', 'marks_type', 'Score']]
                    
                    all_dfs.append(df_long)
                    logging.info(f"Loaded {len(df_long)} rows (Long Format, {marks_type}).")
            except Exception as e:
                logging.error(f"Error reading {file_path}: {e}")
        else:
            logging.warning(f"File not found - {file_path}")

    # Process Master File
    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        
        # Remove empty scores
        # final_df = final_df.dropna(subset=['Score']) # Not requested explicitly, preserving all rows

        if not os.path.exists(output_dir_master):
            os.makedirs(output_dir_master)
            
        output_file_master = os.path.join(output_dir_master, "Labs_and_Quizzes.csv")
        final_df.to_csv(output_file_master, index=False)
        
        logging.info(f"SUCCESS: Consolidated Labs and Quizzes file saved to: {output_file_master}")
        logging.info(f"Total Records (Long Format): {len(final_df)}")
    else:
        logging.warning("No Labs or Quizzes data found to consolidate.")

if __name__ == "__main__":
    consolidate_labs()
