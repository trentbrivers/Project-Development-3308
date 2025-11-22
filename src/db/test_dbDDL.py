import src.db.dbDDL as dbDDL
from pathlib import Path
import sqlite3
import unittest

class dbDDLTestCase(unittest.TestCase):
    
    # Implement a setUp method that creates a new sqlite3 database file (use test.db) and runs both functions.
    def setUp(self):
        db = 'test_db'
        self.dbPath = Path(__file__).parent.resolve().joinpath(db)
        self.parentPath = self.dbPath.parent.resolve()

        dbDDL.preClean(self.dbPath)
        dbDDL.dbDDL(self.dbPath)

        # Check that file exists, raise exception if not
        if self.dbPath not in list(self.parentPath.iterdir()):
            raise Exception('Database creation failure; db {} not present in dir {}.'.format(self.dbPath.name, self.parentPath))

    # Implement a tearDown method that deletes the database that was created. Handle exceptions for a failed remove.
    def tearDown(self):
        # Delete DB test
        self.dbPath.unlink()

        # Check that file is gone, raise exception if not
        if self.dbPath in list(self.parentPath.iterdir()):
            raise Exception('Database deletion failure; db {} still present in dir {}.'.format(self.dbPath.name, self.parentPath))
        
    def test_preClean(self):
        """Verifies that dbDDL.preClean() successfully removes
        all tables from the sqlite_schema catalog."""

        dbDDL.preClean(self.dbPath)
        
        # - Scan catalog and verify it is empty
        con = sqlite3.connect(self.dbPath)
        cur = con.cursor()
        allTbls = cur.execute("SELECT * FROM sqlite_schema WHERE Type = 'table'").fetchall()
        self.assertEqual(allTbls, [], msg='Error - expect empty list.')
        con.close()
    
    def test_dbDDL(self):
        """Validates that the table names added to the sqlite_schema
        catalog match the ERD."""
        
        correctNames = {'Player', 'PlayerAnswer', 'Question', 'Contestant',
                    'Game', 'GameQuestion'}
        
        con = sqlite3.connect(self.dbPath)
        cur = con.cursor()
        allTblNames = set([item[0] for item in 
                       cur.execute("SELECT tbl_name FROM sqlite_schema WHERE type = 'table'").fetchall()])
        self.assertEqual(allTblNames, correctNames, msg='Error - expect tables {}.'.format(correctNames))
        con.close()
    
# Run Test Cases
if __name__ == '__main__':
    unittest.main()