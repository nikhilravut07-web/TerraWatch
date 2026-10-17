import json, sqlite3
from app.config import DB_PATH, DATA_DIR

def connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con=sqlite3.connect(DB_PATH); con.row_factory=sqlite3.Row
    return con

def init_db():
    with connect() as c:
        c.executescript('''CREATE TABLE IF NOT EXISTS assets(id TEXT PRIMARY KEY, data TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS observations(id TEXT PRIMARY KEY, asset_id TEXT NOT NULL, date TEXT NOT NULL, data TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS investigations(id TEXT PRIMARY KEY, asset_id TEXT NOT NULL, created_at TEXT NOT NULL, data TEXT NOT NULL);''')
        if c.execute('SELECT COUNT(*) FROM assets').fetchone()[0] == 0:
            seed=DATA_DIR/'demo'/'demo_data.json'
            if seed.exists():
                d=json.loads(seed.read_text())
                for a in d['assets']: c.execute('INSERT INTO assets VALUES(?,?)',(a['id'],json.dumps(a)))
                for o in d['observations']: c.execute('INSERT INTO observations VALUES(?,?,?,?)',(o['id'],o['asset_id'],o['date'],json.dumps(o)))

def rows(sql, args=()):
    with connect() as c: return [dict(r) for r in c.execute(sql,args).fetchall()]
def get_asset(asset_id):
    r=rows('SELECT data FROM assets WHERE id=?',(asset_id,)); return json.loads(r[0]['data']) if r else None
def assets(): return [json.loads(r['data']) for r in rows('SELECT data FROM assets')]
def observations(asset_id=None):
    sql='SELECT data FROM observations'; args=()
    if asset_id: sql+=' WHERE asset_id=?'; args=(asset_id,)
    sql+=' ORDER BY date'
    return [json.loads(r['data']) for r in rows(sql,args)]
def save_investigation(d):
    with connect() as c: c.execute('INSERT INTO investigations VALUES(?,?,?,?)',(d['id'],d['asset_id'],d['created_at'],json.dumps(d)))
def get_investigation(i):
    r=rows('SELECT data FROM investigations WHERE id=?',(i,)); return json.loads(r[0]['data']) if r else None
def all_investigations(): return [json.loads(r['data']) for r in rows('SELECT data FROM investigations ORDER BY created_at DESC')]
