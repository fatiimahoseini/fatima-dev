import sqlite3
import json

db = r'C:\Users\fatii\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Get all user text parts with session info
print("=== ALL USER TEXT PARTS (with session titles) ===")
c.execute("""SELECT p.session_id, s.title, json_extract(p.data, '$.text') as text, datetime(m.time_created, 'unixepoch') as t
             FROM part p
             JOIN message m ON p.message_id = m.id
             JOIN session s ON p.session_id = s.id
             WHERE json_extract(m.data, '$.role') = 'user'
               AND json_extract(p.data, '$.type') = 'text'
             ORDER BY m.time_created""")
for row in c.fetchall():
    text = row[2] or ''
    # Skip system reminders
    if '<system-reminder>' in text:
        continue
    if text.strip():
        print(f"[{row[0]}] [{row[1]}] {text[:400]}")
        print("---")

# Check for deployment-related user messages
print("\n=== PRODUCTION SESSION USER MESSAGES ===")
sid = 'ses_0bcc70f06ffeBM7TkJcCr5gEhB'
c.execute("""SELECT json_extract(p.data, '$.text') as text
             FROM part p
             JOIN message m ON p.message_id = m.id
             WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'user'
               AND json_extract(p.data, '$.type') = 'text'
             ORDER BY m.time_created""", (sid,))
for row in c.fetchall():
    text = row[0] or ''
    if '<system-reminder>' in text:
        continue
    if text.strip():
        print(f"  {text[:500]}")
        print("---")

# Check for mobile session user messages
print("\n=== MOBILE SESSION USER MESSAGES ===")
sid = 'ses_08f1dee7effehqG5CAeY07OdTd'
c.execute("""SELECT json_extract(p.data, '$.text') as text
             FROM part p
             JOIN message m ON p.message_id = m.id
             WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'user'
               AND json_extract(p.data, '$.type') = 'text'
             ORDER BY m.time_created""", (sid,))
for row in c.fetchall():
    text = row[0] or ''
    if '<system-reminder>' in text:
        continue
    if text.strip():
        print(f"  {text[:500]}")
        print("---")

conn.close()
