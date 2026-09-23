import sqlite3
from pathlib import Path

class TaxonomyDB:
    def __init__(self, db_path):
        self.db_path = Path(db_path).expanduser()

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._initialize()

    def _initialize(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS taxa (
                    taxid INTEGER PRIMARY KEY,
                    parent_taxid INTEGER,
                    name TEXT NOT NULL,
                    rank TEXT
                )
            """)


    def add_taxon(self, parent_taxid, name, rank):
        with sqlite3.connect(self.db_path) as conn:
            sql = """ INSERT INTO taxa (taxid,parent_taxid,name,rank)
                      VALUES(NULL,?,?,?) """
            cur = conn.cursor()
            cur.execute(sql, (parent_taxid, name, rank))
            conn.commit()
        return self.get_taxID(name, rank)

    def get_taxID(self, name, rank):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT taxid FROM taxa WHERE name =? AND rank =?", (name, rank))
            row = cur.fetchone()
            if row:
                return row[0]
            return None

    def get_parentID(self, name, rank):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT parent_taxid FROM taxa WHERE name =? and rank =?", (name, rank))
            row = cur.fetchone()
            if row:
                return row[0]
            return None

    def update_parentID(self, parent_id, name, rank):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE taxa SET parent_taxid =? WHERE name =? and rank =?",
                        (parent_id, name, rank))
            return None

    def fetch_with_id(self, id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM taxa WHERE taxid =?", (id,))
            row = cur.fetchone()
            if row:
                return row
            return None
