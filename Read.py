import pymupdf as fitz

pdffile = r"src\Bill_Of_Materials.pdf"
doc = fitz.open(pdffile)
zoom = 4
mat = fitz.Matrix(zoom, zoom)
count = 0
# Count variable is to get the number of pages in the pdf
for p in doc:
    count += 1
for i in range(count):
    val = f"image_{i+1}.png"
    page = doc.load_page(i)
    pix = page.get_pixmap(matrix=mat)
    pix.save(val)
doc.close()

import easyocr

reader = easyocr.Reader(['en'])
result = reader.readtext("image_1.png", detail=0)

#print("easyocr" + result)

import pandas as pd

# Convert the list to a pandas DataFrame with minimum 4 columns
num_columns = 4
df = pd.DataFrame([result[i:i + num_columns] for i in range(0, len(result), num_columns)])

# Predefined expected columns
EXPECTED_COLUMNS = ["id", "name", "quantity","else"]

# Rename columns based on EXPECTED_COLUMNS
df.columns = EXPECTED_COLUMNS

print(df.head())  # Check the renamed DataFrame


# Display the DataFrame
# print(df)

import sqlite3

conn = sqlite3.connect('BOM.db')
df.to_sql('bill_of_materials', conn, if_exists='replace', index=False)

# Function to query the database for rows containing a given string

def query_database(search_string):
    query = f"SELECT * FROM bill_of_materials WHERE 1=1"
    df = pd.read_sql_query(query, conn)
       
    # Filter rows containing the search string in any column
    filtered_rows = df[df.apply(lambda row: row.astype(str).str.contains(search_string).any(), axis=1)]
    
    return filtered_rows.values.tolist()

#-------------------------------------------------------------------------------------------------------------------

def display_table(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bill_of_materials')
    rows = cursor.fetchall()
    for row in rows:
        print({'id': row[0], 'name': row[1], 'quantity': row[2]})

# Example usage
search_string = 'Names'  # Replace with any string to search for
result_lists = query_database(search_string)
table = display_table(conn)

# Display the result
#print(result_lists

conn.close()