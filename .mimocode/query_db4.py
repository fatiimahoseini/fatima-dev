import sqlite3
import json

db = r'C:\Users\fatii\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Check production session
sid_prod = 'ses_0bcc70f06ffeBM7TkJcCr5gEhB'
print("=== PRODUCTION SESSION - USER MESSAGES ===")
c.execute("SELECT id, data, datetime(time_created, 'unixepoch') as t FROM message WHERE session_id = ? AND json_extract(data, '$.role') = 'user' ORDER BY time_created", (sid_prod,))
for row in c.fetchall():
    d = json.loads(row['data'])
    content = d.get('content', '')
    if isinstance(content, list):
        content = ' '.join([p.get('text','') for p in content if isinstance(p, dict)])
    print(f"[USER @ {row['t']}] {content[:500]}")

print("\n=== PRODUCTION SESSION - EDIT OPERATIONS ===")
c.execute("""SELECT json_extract(p.data, '$.state') as state
             FROM message m
             JOIN part p ON p.message_id = m.id
             WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'assistant'
               AND json_extract(p.data, '$.tool') = 'edit'
             ORDER BY m.time_created""", (sid_prod,))
for row in c.fetchall():
    try:
        state = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        inp = state.get('input', {})
        fp = inp.get('file_path', 'unknown')
        old = inp.get('old_string', '')[:100]
        new = inp.get('new_string', '')[:200]
        print(f"FILE: {fp}")
        print(f"  OLD: {old}...")
        print(f"  NEW: {new}...")
        print()
    except Exception as e:
        print(f"Error: {e}")

print("\n=== PRODUCTION SESSION - WRITE OPERATIONS ===")
c.execute("""SELECT json_extract(p.data, '$.state') as state
             FROM message m
             JOIN part p ON p.message_id = m.id
             WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'assistant'
               AND json_extract(p.data, '$.tool') = 'write'
             ORDER BY m.time_created""", (sid_prod,))
for row in c.fetchall():
    try:
        state = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        inp = state.get('input', {})
        fp = inp.get('file_path', 'unknown')
        content_len = len(inp.get('content', ''))
        print(f"FILE: {fp} ({content_len} chars)")
    except Exception as e:
        print(f"Error: {e}")

# Check background effects session edits
sid_bg = 'ses_0c7fed7eaffeBNzogfjhZOKJSZ'
print("\n=== BACKGROUND EFFECTS SESSION - EDIT OPERATIONS ===")
c.execute("""SELECT json_extract(p.data, '$.state') as state
             FROM message m
             JOIN part p ON p.message_id = m.id
             WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'assistant'
               AND json_extract(p.data, '$.tool') in ('edit', 'write')
             ORDER BY m.time_created""", (sid_bg,))
for row in c.fetchall():
    try:
        state = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        inp = state.get('input', {})
        fp = inp.get('file_path', 'unknown')
        tool_type = 'write' if 'content' in inp else 'edit'
        print(f"[{tool_type}] FILE: {fp}")
    except Exception as e:
        print(f"Error: {e}")

conn.close()
