import sqlite3
import json

db = r'C:\Users\fatii\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Session: Fix mobile responsiveness
sid = 'ses_08f1dee7effehqG5CAeY07OdTd'

print("=== SESSION: Fix mobile responsiveness ===")

# User messages
c.execute("SELECT id, data, datetime(time_created, 'unixepoch') as t FROM message WHERE session_id = ? AND json_extract(data, '$.role') = 'user' ORDER BY time_created", (sid,))
for row in c.fetchall():
    d = json.loads(row['data'])
    content = d.get('content', '')
    if isinstance(content, list):
        content = ' '.join([p.get('text','') for p in content if isinstance(p, dict)])
    print(f"[USER @ {row['t']}] {content[:500]}")

# Assistant messages with tool calls
print("\n=== ASSISTANT TOOL CALLS ===")
c.execute("""SELECT m.id, m.agent_id, json_extract(p.data, '$.type') as part_type,
             json_extract(p.data, '$.tool') as tool,
             substr(p.data, 1, 1000) as preview
             FROM message m
             JOIN part p ON p.message_id = m.id
             WHERE m.session_id = ? AND json_extract(m.data, '$.role') = 'assistant'
             ORDER BY m.time_created, p.time_created""", (sid,))
for row in c.fetchall():
    agent = row['agent_id'] or 'main'
    print(f"[{agent}] type={row['part_type']} tool={row['tool']}")
    if row['part_type'] == 'text':
        try:
            d = json.loads(row['preview'])
            text = d.get('text', '')[:400]
            if text.strip():
                print(f"  TEXT: {text}")
        except:
            pass
    elif row['part_type'] == 'tool':
        try:
            d = json.loads(row['preview'])
            state = d.get('state', {})
            inp = str(state.get('input', ''))[:200]
            out = str(state.get('output', ''))[:300]
            print(f"  INPUT: {inp}")
            if out.strip():
                print(f"  OUTPUT: {out}")
        except:
            pass

conn.close()
