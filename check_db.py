import sqlite3

conn = sqlite3.connect('smartcar.db')
cursor = conn.cursor()

cols = cursor.execute("PRAGMA table_info(contracts)").fetchall()

with open("contracts_schema.txt", "w") as f:
    for c in cols:
        f.write(f"{c[1]} ({c[2]})\n")

print("Schema saved to contracts_schema.txt")
conn.close()
