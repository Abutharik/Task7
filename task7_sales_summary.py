import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Create and connect to SQLite database
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Clear any existing data
cursor.execute("DELETE FROM sales")

# Insert dummy sales data
sales_data = [
    ('Pen', 10, 5),
    ('Pencil', 20, 2),
    ('Notebook', 5, 30),
    ('Pen', 15, 5),
    ('Pencil', 10, 2)
]
cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sales_data)
conn.commit()

# Run SQL query
query = """
SELECT product,
       SUM(quantity) AS total_qty,
       SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""
df = pd.read_sql_query(query, conn)
print(df)

# Plot bar chart
df.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue', title='Revenue by Product')
plt.ylabel('Revenue')
plt.tight_layout()
plt.savefig('sales_chart.png')
plt.show()

# Close connection
conn.close()
