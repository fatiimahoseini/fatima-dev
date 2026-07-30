import sqlite3
import json

db = r'C:\Users\fatii\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Session: Fix mobile responsiveness - get full edit details
sid = 'ses_08f1dee7effehqG5CAeY07OdTd'

print("=== EDIT OPERATIONS ===")
c.execute("""SELECT json_extract(p.data, '$.state') as state
             FROM message m
             JOIN part p ON p.message_id = m.id
             WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'assistant'
               AND json_extract(p.data, '$.tool') = 'edit'
             ORDER BY m.time_created""", (sid,))
for row in c.fetchall():
    try:
        state = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        inp = state.get('input', {})
        fp = inp.get('file_path', 'unknown')
        old = inp.get('old_string', '')[:150]
        new = inp.get('new_string', '')[:300]
        print(f"FILE: {fp}")
        print(f"  OLD: {old}...")
        print(f"  NEW: {new}...")
        print()
    except Exception as e:
        print(f"Error: {e}")

# Also check for any write operations
print("=== WRITE OPERATIONS ===")
c.execute("""SELECT json_extract(p.data, '$.state') as state
             FROM message m
             JOIN part p ON p.message_id = m.id
             WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'assistant'
               AND json_extract(p.data, '$.tool') = 'write'
             ORDER BY m.time_created""", (sid,))
for row in c.fetchall():
    try:
        state = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        inp = state.get('input', {})
        fp = inp.get('file_path', 'unknown')
        content_len = len(inp.get('content', ''))
        print(f"FILE: {fp} ({content_len} chars)")
    except Exception as e:
        print(f"Error: {e}")

# Check for text output (summary of what was done)
print("\n=== FINAL TEXT OUTPUT ===")
c.execute("""SELECT json_extract(p.data, '$.text') as text
             FROM message m
             JOIN part p ON p.message_id = m.id
             WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'assistant'
               AND json_extract(p.data, '$.type') = 'text'
             ORDER BY m.time_created""", (sid,))
for row in c.fetchall():
    if row[0] and len(row[0]) > 10:
        print(row[0][:1000])
        print("---")

conn.close()
