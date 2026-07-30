import sqlite3
import json

db = r'C:\Users\fatii\.local\share\mimocode\mimocode.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# 1. List recent sessions
print("=== RECENT SESSIONS ===")
c.execute("SELECT id, directory, title, datetime(time_created, 'unixepoch') as created FROM session ORDER BY time_created DESC LIMIT 20")
for row in c.fetchall():
    print(f"  {row['id']} | {row['directory']} | {row['title']} | {row['created']}")

# 2. Find sessions for this project
print("\n=== PROJECT SESSIONS (fatima-dev) ===")
c.execute("SELECT id, directory, title, datetime(time_created, 'unixepoch') as created FROM session WHERE directory LIKE '%fatima-dev%' ORDER BY time_created DESC")
sessions = c.fetchall()
for row in sessions:
    print(f"  {row['id']} | {row['title']} | {row['created']}")

# 3. For each session, look for user statements with keywords
print("\n=== USER KEYWORDS ===")
for row in sessions:
    sid = row['id']
    c.execute("SELECT id, data FROM message WHERE session_id = ? AND json_extract(data, '$.role') = 'user' ORDER BY time_created", (sid,))
    msgs = c.fetchall()
    for m in msgs:
        try:
            d = json.loads(m['data'])
            content = d.get('content', '')
            if isinstance(content, list):
                content = ' '.join([p.get('text','') for p in content if isinstance(p, dict)])
            lower = content.lower()
            keywords = ['always', 'never', 'remember', 'rule', 'decision', 'decided', 'tradeoff', 'reason', 'repeat', 'again', 'every time', 'workflow', 'prefer', 'dont', "don't"]
            if any(kw in lower for kw in keywords):
                print(f"  [{sid}] {content[:200]}")
        except:
            pass

# 4. Check for user language (Arabic?)
print("\n=== NON-ENGLISH USER MESSAGES ===")
for row in sessions:
    sid = row['id']
    c.execute("SELECT id, data FROM message WHERE session_id = ? AND json_extract(data, '$.role') = 'user' ORDER BY time_created", (sid,))
    msgs = c.fetchall()
    for m in msgs:
        try:
            d = json.loads(m['data'])
            content = d.get('content', '')
            if isinstance(content, list):
                content = ' '.join([p.get('text','') for p in content if isinstance(p, dict)])
            # Check for Arabic characters
            if any('\u0600' <= ch <= '\u06FF' for ch in content):
                print(f"  [{sid}] {content[:300]}")
        except:
            pass

# 5. Check for errors in tool results
print("\n=== ERRORS IN TOOL OUTPUTS (last 5 sessions) ===")
for row in sessions[:5]:
    sid = row['id']
    c.execute("""SELECT p.data FROM part p 
                 JOIN message m ON p.message_id = m.id 
                 WHERE m.session_id = ? AND json_extract(p.data, '$.type') = 'tool'
                 AND json_extract(p.data, '$.state.output') LIKE '%error%'
                 ORDER BY m.time_created DESC LIMIT 5""", (sid,))
    for p in c.fetchall():
        try:
            d = json.loads(p[0])
            out = d.get('state', {}).get('output', '')[:300]
            tool = d.get('tool', 'unknown')
            print(f"  [{sid}] {tool}: {out}")
        except:
            pass

conn.close()
