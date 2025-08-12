import sqlite3
import pandas as pd
import sys
from pathlib import Path

def csv_to_sqlite(csv_file_path, db_file_path=None, table_name="patient_records"):
    """
    Convert CSV file to SQLite database
    
    Args:
        csv_file_path (str): Path to the CSV file
        db_file_path (str): Path for the SQLite database file (optional)
        table_name (str): Name for the database table
    """
    
    if db_file_path is None:
        csv_path = Path(csv_file_path)
        db_file_path = csv_path.parent / f"{csv_path.stem}.db"
    
    try:
        print(f"Reading CSV file: {csv_file_path}")
        df = pd.read_csv(csv_file_path)
        
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        print(f"Creating SQLite database: {db_file_path}")
        conn = sqlite3.connect(db_file_path)
        
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        cursor = conn.cursor()
        
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_patient_id ON {table_name}(patient_id)')
        
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_datetime ON {table_name}(datetime)')
        
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_condition ON {table_name}(condition)')
        
        conn.commit()
        
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        record_count = cursor.fetchone()[0]
        
        cursor.execute(f'SELECT COUNT(DISTINCT patient_id) FROM {table_name}')
        patient_count = cursor.fetchone()[0]
        
        print(f"\nDatabase created successfully!")
        print(f"Total records: {record_count}")
        print(f"Unique patients: {patient_count}")
        print(f"Table name: {table_name}")
        
        print(f"\nSample records from the database:")
        cursor.execute(f'SELECT * FROM {table_name} LIMIT 3')
        sample_records = cursor.fetchall()
        
        column_names = [description[0] for description in cursor.description]
        print(f"Columns: {column_names}")
        
        for i, record in enumerate(sample_records, 1):
            print(f"Record {i}: {record}")
        
        conn.close()
        print(f"\nDatabase file saved as: {db_file_path}")
        
        return db_file_path
        
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        return None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

def query_database(db_file_path, table_name="patient_records"):

    try:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        
        print(f"\n--- Sample Queries ---")
        
        print("\n1. All records for patient ER101:")
        cursor.execute(f'SELECT datetime, condition, vitals_BP, vitals_HR, medications FROM {table_name} WHERE patient_id = "ER101" ORDER BY datetime')
        results = cursor.fetchall()
        for record in results[:5]:
            print(f"   {record}")
        
        print(f"\n2. Records with high heart rate (>120):")
        cursor.execute(f'SELECT datetime, patient_id, vitals_HR, vitals_BP FROM {table_name} WHERE vitals_HR > 120 ORDER BY vitals_HR DESC')
        results = cursor.fetchall()
        for record in results[:3]:  
            print(f"   {record}")
        
        print(f"\n3. Unique medications used:")
        cursor.execute(f'SELECT DISTINCT medications FROM {table_name} WHERE medications IS NOT NULL')
        results = cursor.fetchall()
        for record in results[:5]:  
            print(f"   {record[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error querying database: {str(e)}")

if __name__ == "__main__":
    csv_file = "sbar_notes_emergency_room_patients_week.csv"  
    
    db_path = csv_to_sqlite(csv_file, table_name="medical_records")
    
    if db_path:
        query_database(db_path, table_name="medical_records")