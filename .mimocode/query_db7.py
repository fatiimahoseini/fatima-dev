import sqlite3
import json

db = r'C:\Users\fatii\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Check part table for user text
print("=== PART TABLE SCHEMA ===")
c.execute("PRAGMA table_info(part)")
for row in c.fetchall():
    print(f"  {row['name']} ({row['type']})")

# Get user parts (text content)
print("\n=== USER TEXT PARTS ===")
c.execute("""SELECT p.session_id, p.data
             FROM part p
             JOIN message m ON p.message_id = m.id
             WHERE json_extract(m.data, '$.role') = 'user'
               AND json_extract(p.data, '$.type') = 'text'
             ORDER BY m.time_created
             LIMIT 20""")
for row in c.fetchall():
    try:
        d = json.loads(row[1])
        text = d.get('text', '')[:500]
        if text.strip():
            print(f"[{row['session_id']}] {text}")
            print("---")
    except Exception as e:
        print(f"Error: {e}")

# Check for assistant text with user directives
print("\n=== ASSISTANT TEXT WITH USER DIRECTIVES ===")
c.execute("""SELECT p.session_id, json_extract(p.data, '$.text') as text
             FROM part p
             JOIN message m ON p.message_id = m.id
             WHERE json_extract(m.data, '$.role') = 'assistant'
               AND json_extract(p.data, '$.type') = 'text'
             ORDER BY m.time_created""")
for row in c.fetchall():
    text = row[1] or ''
    lower = text.lower()
    if any(kw in lower for kw in ['user said', 'user wants', 'user asked', 'user requested']):
        print(f"[{row['session_id']}] {text[:400]}")
        print("---")

conn.close()
