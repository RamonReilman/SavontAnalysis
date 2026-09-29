import sqlite3
from pathlib import Path

class TaxonomyDB:
    def __init__(self, db_path):
        """
        Initializing database
        :param db_path: Path where the db is stored
        """
        self.db_path = Path(db_path).expanduser()

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._initialize()

    def _initialize(self):
        """
        Creates table if it does not exist yet
        :return: -
        """
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
        """
        Adds a new taxon entry into the database
        :param parent_taxid: the db ID of the parent rank
        :param name: Name of the taxon
        :param rank: Rank of the taxon
        :return: The taxID of the new entry
        """
        with sqlite3.connect(self.db_path) as conn:
            id = self.get_taxID(name, rank)
            if id:
                return id
            sql = """ INSERT INTO taxa (taxid,parent_taxid,name,rank)
                      VALUES(NULL,?,?,?) """
            cur = conn.cursor()
            cur.execute(sql, (parent_taxid, name, rank))
            conn.commit()
        return self.get_taxID(name, rank)

    def get_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT taxid, parent_taxid, name, rank FROM taxa")
            row = cur.fetchall()
            return row

    def get_taxID(self, name, rank):
        """
        Gets the taxID of an entry
        :param name: Name of taxon
        :param rank: Rank of taxon
        :return: The taxID of the new entry
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT taxid FROM taxa WHERE name =? AND rank =?", (name, rank))
            row = cur.fetchone()
            if row:
                return row[0]
            return None

    def get_parentID(self, name, rank):
        """
        Gets the parents ID of an entry
        :param name: Name of taxon
        :param rank: Rank of taxon
        :return: The taxID of the parents entry
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT parent_taxid FROM taxa WHERE name =? and rank =?", (name, rank))
            row = cur.fetchone()
            if row:
                return row[0]
            return None

    def update_parentID(self, parent_id, name, rank):
        """
        Sets the parentID of an entry
        :param parent_id: ID of the entry's parent
        :param name: Name of taxon
        :param rank: Rank of taxon
        :return: -
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE taxa SET parent_taxid =? WHERE name =? and rank =?",
                        (parent_id, name, rank))
            return None

    def fetch_with_id(self, id):
        """
        Gets taxon information through taxID
        :param id: taxID of entry
        :return: Entry information if it exists else None
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM taxa WHERE taxid =?", (id,))
            row = cur.fetchone()
            if row:
                return row
            return None
