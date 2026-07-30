import sqlite3
import json

db = r'C:\Users\fatii\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Check message table structure
print("=== MESSAGE TABLE SCHEMA ===")
c.execute("PRAGMA table_info(message)")
for row in c.fetchall():
    print(f"  {row['name']} ({row['type']})")

# Sample messages to understand data format
print("\n=== SAMPLE USER MESSAGES (first 5) ===")
c.execute("SELECT id, session_id, data FROM message WHERE json_extract(data, '$.role') = 'user' LIMIT 5")
for row in c.fetchall():
    try:
        d = json.loads(row['data'])
        print(f"Session: {row['session_id']}")
        print(f"Keys: {list(d.keys())}")
        content = d.get('content', d.get('text', 'NO_CONTENT'))
        if isinstance(content, list):
            print(f"Content type: list, first item: {content[0] if content else 'empty'}")
        else:
            print(f"Content: {str(content)[:200]}")
        print("---")
    except Exception as e:
        print(f"Error: {e}")

# Check if content is in a different field
print("\n=== RAW USER MESSAGE DATA SAMPLE ===")
c.execute("SELECT data FROM message WHERE json_extract(data, '$.role') = 'user' LIMIT 3")
for row in c.fetchall():
    try:
        d = json.loads(row['data'])
        print(json.dumps(d, indent=2)[:500])
        print("---")
    except Exception as e:
        print(f"Error: {e}")

conn.close()
