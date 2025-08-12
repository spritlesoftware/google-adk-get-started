import sqlite3
import pandas as pd
import sys
from pathlib import Path

def csv_to_sqlite(csv_file_path, db_file_path=None, table_name="clinical_rules"):
    
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
        
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_rule_id ON {table_name}(rule_id)')
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_category ON {table_name}(category)')
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_priority ON {table_name}(priority)')
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_signal ON {table_name}(signal)')
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_dedupe_key ON {table_name}(dedupe_key)')
        
        conn.commit()
        
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        record_count = cursor.fetchone()[0]
        
        cursor.execute(f'SELECT COUNT(DISTINCT category) FROM {table_name}')
        category_count = cursor.fetchone()[0]
        
        print(f"\nDatabase created successfully!")
        print(f"Total rules: {record_count}")
        print(f"Rule categories: {category_count}")
        print(f"Table name: {table_name}")
        
        print(f"\nSample rules from the database:")
        cursor.execute(f'SELECT * FROM {table_name} LIMIT 3')
        sample_records = cursor.fetchall()
        
        column_names = [description[0] for description in cursor.description]
        print(f"Columns: {column_names}")
        
        for i, record in enumerate(sample_records, 1):
            print(f"Rule {i}: {record}")
        
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

def query_database(db_file_path, table_name="clinical_rules"):
    try:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        
        print(f"\n--- Sample Queries ---")
        
        print("\n1. High priority rules:")
        cursor.execute(f'SELECT rule_id, signal, operator, value, message FROM {table_name} WHERE priority = "High" ORDER BY rule_id')
        results = cursor.fetchall()
        for record in results[:5]:
            print(f"   {record}")
        
        print(f"\n2. Rules by category:")
        cursor.execute(f'SELECT category, COUNT(*) as rule_count FROM {table_name} GROUP BY category ORDER BY rule_count DESC')
        results = cursor.fetchall()
        for record in results:
            print(f"   {record}")
        
        print(f"\n3. Vitals monitoring rules:")
        cursor.execute(f'SELECT rule_id, signal, operator, value, unit, action FROM {table_name} WHERE category = "vitals" ORDER BY rule_id')
        results = cursor.fetchall()
        for record in results:
            print(f"   {record}")
        
        print(f"\n4. Time-sensitive rules:")
        cursor.execute(f'SELECT rule_id, signal, time_window_h, action FROM {table_name} WHERE time_window_h > 0 ORDER BY time_window_h')
        results = cursor.fetchall()
        for record in results:
            print(f"   {record}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error querying database: {str(e)}")

if __name__ == "__main__":
    csv_file = "policy_rules.csv"
    
    db_path = csv_to_sqlite(csv_file, table_name="clinical_rules")
    
    if db_path:
        query_database(db_path, table_name="clinical_rules")
        
        print(f"\n--- Usage Instructions ---")
        print(f"To use this database in your applications:")
        print(f"1. Connect: conn = sqlite3.connect('{db_path}')")
        print(f"2. Query: cursor.execute('SELECT * FROM clinical_rules WHERE priority = \"High\"')")
        print(f"3. Fetch: results = cursor.fetchall()")
        print(f"4. Close: conn.close()")