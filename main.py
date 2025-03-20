##imports##
import pandas as pd
import sqlite3 as sql
import cv2 as cv2
import numpy as np
import matplotlib as plt
import os
##--##

##functions##


##opencv##  ##move to graphics folder
filename= r'..\src\chessboard.jpg'
img = cv2.imread(filename)




##---##
def read_excel_file(filepath): 
    """Reads an Excel file into a pandas DataFrame with error handling."""
    try:
        df = pd.read_excel(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None
#---------------------------------------------------------------------------------------------------#
def create_connection(db_file):
    conn = sql.connect(db_file)
    return conn

#---------------------------------------------------------------------------------------------------#
def display_table(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bill_of_materials')
    rows = cursor.fetchall()
    for row in rows:
        print({'id': row[0], 'name': row[1], 'quantity': row[2]})
#-----------------------------------------------------------------------------------------------------#
def insert_material(id, name, quantity):
    cursor = conn.cursor()
 # Insert values
    cursor.execute('''
        INSERT INTO bill_of_materials (id, name, quantity)
        VALUES (?, ?, ?)
    ''', (id, name, quantity))
    
    # Commit and close
    conn.commit()
    conn.close()

   
#------------------------------------------------------------------------------------------------------#
def delete_item(conn, item_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bill_of_materials WHERE id = ?', (item_id,))
    conn.commit()
#------------------------------------------------------------------------------------------------------#
def get_item(conn, item_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bill_of_materials WHERE id = ?', (item_id,))
    row = cursor.fetchone()
    if row:
        return {'id': row[0], 'name': row[1], 'quantity': row[2]}
    return None
#--------------------------------------------------------------------------------------------------------#
def push_to_excel(conn, excel_file):
    if os.path.exists(excel_file):
        df = pd.read_sql_query("SELECT * FROM bill_of_materials", conn)
        with pd.ExcelWriter(excel_file, mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name='Items', index=False, header=False)
    else:
        print(f"{excel_file} does not exist.")

#*--*#


# Example usage
if __name__ == "__main__":
    db_file = 'BOM.db'
    conn = create_connection(db_file)

    # Example usage
    insert_material('Bill Of Materials', '19.06.21, 21:05', 'Bill Of Materials')
    
    # Display entire table
    display_table(conn)

    # Push to Excel
    push_to_excel(conn, 'Sample_Bom_Asme.xlsx')

    # Delete example
    delete_item(conn, 1)

    
    conn.close()
