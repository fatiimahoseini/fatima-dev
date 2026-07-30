import sqlite3
import json

db = r'C:\Users\fatii\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Check for cloudinary details in production session
sid = 'ses_0bcc70f06ffeBM7TkJcCr5gEhB'
print("=== PRODUCTION SESSION - CLOUDINARY SETTINGS WRITE ===")
c.execute("""SELECT json_extract(p.data, '$.state') as state
             FROM message m
             JOIN part p ON p.message_id = m.id
             WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'assistant'
               AND json_extract(p.data, '$.tool') = 'write'
               AND json_extract(p.data, '$.state.input.file_path') LIKE '%settings%'
             ORDER BY m.time_created""", (sid,))
for row in c.fetchall():
    try:
        state = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        inp = state.get('input', {})
        content = inp.get('content', '')
        # Find cloudinary section
        if 'cloudinary' in content.lower():
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'cloudinary' in line.lower() or 'CLOUDINARY' in line:
                    start = max(0, i-1)
                    end = min(len(lines), i+10)
                    print('\n'.join(lines[start:end]))
                    print('---')
    except Exception as e:
        print(f"Error: {e}")

# Check for all user messages with actual content (not empty)
print("\n=== ALL USER MESSAGES WITH CONTENT ===")
c.execute("SELECT session_id, data FROM message WHERE json_extract(data, '$.role') = 'user' ORDER BY time_created")
for row in c.fetchall():
    try:
        d = json.loads(row['data'])
        content = d.get('content', '')
        if isinstance(content, list):
            content = ' '.join([p.get('text','') for p in content if isinstance(p, dict)])
        if content.strip():
            print(f"[{row['session_id']}] {content[:300]}")
    except:
        pass

conn.close()
