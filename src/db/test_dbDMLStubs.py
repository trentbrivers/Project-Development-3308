# Execute `PRAGMA foreign_keys = ON` for all connections; https://sqlite.org/foreignkeys.html

import dbDDL
import dbDMLStubs
from pathlib import Path
import sqlite3
import unittest

class dbDMLStubsTestCase(unittest.TestCase):
    # Implement a setUp method that creates a new sqlite3 database file (use test.db) and runs both functions.
    def setUp(self):
        # Data that gets referenced in multiple tests below
        self.playerScript = """BEGIN;
                               UPDATE Player
                               SET TotalGamesPlayed = 1,
                                   TotalGamesWon = 1,
                                   HighScore = 7700
                               WHERE UserName = 'TrentKnowsAll';

                               UPDATE Player
                               SET TotalGamesPlayed = 1,
                                   TotalGamesRunnerUp = 1,
                                   HighScore = 7500
                               WHERE UserName = 'CornRach';

                               UPDATE Player
                               SET TotalGamesPlayed = 1,
                                   HighScore = 7400
                               WHERE UserName = 'AtomicAbe';

                               UPDATE Player
                               SET TotalGamesPlayed = 1,
                                   HighScore = 7100
                               WHERE UserName = 'RetroJammin';
                         
                               COMMIT;"""
        
        self.UserNames = ['TrentKnowsAll', 'CornRach', 'AtomicAbe', 'RetroJammin']
        
        # DB config
        db = 'test_db'
        self.dbPath = Path(__file__).parent.resolve().joinpath(db)
        self.parentPath = self.dbPath.parent.resolve()

        dbDDL.preClean(self.dbPath)
        dbDDL.dbDDL(self.dbPath)

        # Check that file exists, raise exception if not
        if self.dbPath not in list(self.parentPath.iterdir()):
            raise Exception('Database creation failure; db {} not present in dir {}.'.format(self.dbPath.name, self.parentPath))
        
        # Open a connection to query the db
        self.con = sqlite3.connect(self.dbPath)
        self.cur = self.con.cursor()
        self.cur.execute('PRAGMA foreign_keys = ON;')

    # Implement a tearDown method that deletes the database that was created. Handle exceptions for a failed remove.
    def tearDown(self):
        # Close the connection
        self.con.close()
        
        # Delete DB test
        self.dbPath.unlink()

        # Check that file is gone, raise exception if not
        if self.dbPath in list(self.parentPath.iterdir()):
            raise Exception('Database deletion failure; db {} still present in dir {}.'.format(self.dbPath.name, self.parentPath))
    
    def test_Player_newPlayerSignup(self):
        # Positive Control: These should all work (unique)
        for username in self.UserNames:
            with self.subTest(i=self.UserNames.index(username)):
                dbDMLStubs.Player_newUserSignup(self.dbPath, username)
                expect = [(username, 0, 0, 0, 0)]
                queryRes = self.cur.execute("""SELECT UserName, TotalGamesPlayed, TotalGamesWon, TotalGamesRunnerUp, HighScore 
                                           FROM Player 
                                           WHERE UserName = '{}';""".format(username)).fetchall()
                self.assertEqual(expect, queryRes)
        
        # Set some nonzero data to test the next two items
        self.cur.executescript(self.playerScript)
        self.con.commit()
        
        # Negative Control: This should fail (non-unique)
        NegCtrl = 'TrentKnowsAll'
        with self.assertRaises(sqlite3.IntegrityError):
            dbDMLStubs.Player_newUserSignup(self.dbPath, NegCtrl)

        # The attempt to insert a duplicate name should not overwrite data.
        expect = [(NegCtrl, 1, 1, 0, 7700)]
        queryRes = self.cur.execute("""SELECT UserName, TotalGamesPlayed, TotalGamesWon, TotalGamesRunnerUp, HighScore 
                                       FROM Player 
                                       WHERE UserName = '{}';""".format(NegCtrl)).fetchall()
        self.assertEqual(expect, queryRes)
        

    def test_Question_InsertRow(self):
        # Positive Control: This should work & show rowid aliasing in action
        PosCtrl1 = [('J', 'Testing', 100, 'Why are we doing this?', 'To test basic RI actions.'),
               ('J', 'Birds', 500, 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")]
        dbDMLStubs.Question_InsertRow(self.dbPath, PosCtrl1)
        queryRes = self.cur.execute("SELECT Round, Category, PointValue, QuestionText, QuestionAns FROM Question;").fetchall()
        self.assertEqual(PosCtrl1, queryRes, msg='Error: Expect the INSERT and SELECT to match.')
        
        # This should also work - different questions can have the same answer
        PosCtrl2 = [('DJ', 'Testing', 200, 'Why do we validate table constraints?', 'To test basic RI actions.')]
        # Query this and wrap in an assertEquals
        dbDMLStubs.Question_InsertRow(self.dbPath, PosCtrl2)
        queryRes = self.cur.execute("SELECT Round, Category, PointValue, QuestionText, QuestionAns FROM Question WHERE Round = 'DJ';").fetchall()
        self.assertEqual(PosCtrl2, queryRes, msg='Error: Expect the INSERT and SELECT to match.')

        # This should fail - violates uniqueness constraint
        NegCtrl1 = [('FJ', 'Testing', 0, 'Why do we validate table constraints?', 'Broken DB logic is no fun.')]
        with self.assertRaises(sqlite3.IntegrityError):
            dbDMLStubs.Question_InsertRow(self.dbPath, NegCtrl1)

        # Note: this passes, but it takes 26s b/c of internal disk I/O in sqlite3 - proceed with caution!
        # # Every single one of these should violate a NOT NULL constraint
        # NegCtrl2 = [[('NULL', 'Birds', 500, 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")],
        #             [('J', 'NULL', 500, 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")],
        #             [('J', 'Birds', 'NULL', 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")],
        #             [('J', 'Birds', 500, 'NULL', "Wilson's Pharalope")],
        #             [('J', 'Birds', 500, 'This unusual shorebird has showy females and drab males.', 'NULL')]]
        
        # for test in NegCtrl2:
        #     with self.subTest(i=NegCtrl2.index(test)):
        #         with self.assertRaises(sqlite3.OperationalError):
        #             dbDMLStubs.Question_InsertRow(self.dbPath, test)

    def test_Game_CreateNewGame(self):
        user = 'testName'
        
        # Positive Control: This should work & show INSERT... DEFAULT VALUES in action
        rowCtBefore = len(self.cur.execute("SELECT * FROM Game;").fetchall())
        dbDMLStubs.Game_CreateNewGame(self.dbPath)
        rowCtAfter = len(self.cur.execute("SELECT * FROM Game;").fetchall())
        self.assertEqual(rowCtBefore + 1, rowCtAfter, msg='A single row was not added to TABLE Game.')


    def test_Contestant_CreateNewContestant(self):
        user = 'testName'
        
        # Positive Control: This should work & show foreign keys in action
        # Tables Player, Game must have valid PKs to reference
        dbDMLStubs.Player_newUserSignup(self.dbPath, user)
        dbDMLStubs.Game_CreateNewGame(self.dbPath)
        dbDMLStubs.Contestant_CreateNewContestant(self.dbPath, user)
        
        expect = [(1, 1, 0)]
        result = self.cur.execute("SELECT * FROM Contestant;").fetchall()
        self.assertEqual(expect, result, msg='Error; expect foreign keys & default value to match {}.'.format(expect))

        # Confirm that invalid FK references throw IntegrityError
        invalidFKs = [(1, 2), 
                      (2, 1)]
        for test in invalidFKs:
            with self.subTest(i=invalidFKs.index(test)):
                with self.assertRaises(sqlite3.IntegrityError):
                    self.cur.execute("""INSERT INTO Contestant (GameID, PlayerID) 
                                            VALUES (?, ?)""", (test[0], test[1]))
                    self.con.commit()
                    print(self.cur.execute("SELECT * FROM Contestant").fetchall())

    def test_Contestant_DropPlayersOrGames(self):
        """Confirm that RI actions (ON DELETE CASCADE ON UPDATE CASCADE) work"""
        # Set up Player & Game with data
        for name in self.UserNames:
            dbDMLStubs.Player_newUserSignup(self.dbPath, name)
        self.cur.executescript(self.playerScript)
        dbDMLStubs.Game_CreateNewGame(self.dbPath)
 
        # Set up Contestants
        for name in self.UserNames:
            dbDMLStubs.Contestant_CreateNewContestant(self.dbPath, name)
        
        # Delete a player and confirm their contestant is gone
        # Positive control: Contestant should obviously exist before deletion!
        expect = (1, 1, 0)
        posCtrl = self.cur.execute("""SELECT * FROM Contestant WHERE PlayerID = 
                                          (SELECT PlayerID FROM Player WHERE UserName = 'TrentKnowsAll');""").fetchone()
        self.assertEqual(expect, posCtrl, msg='Error: Expect this row to exist before UserName is deleted from Player.')

        self.cur.execute("DELETE FROM Player WHERE UserName = 'TrentKnowsAll';")
        self.con.commit()

        # Confirm Trent is gone from contestant and no one else is.
        rowsLeft = len(self.cur.execute("SELECT * FROM Contestant;").fetchall())
        self.assertEqual(rowsLeft, 3, msg='Error: No other Contestant rows should have ON DELETE CASCADE')
        wheresTrent = self.cur.execute("SELECT * FROM Contestant WHERE PlayerID = 1;").fetchall()
        self.assertEqual(wheresTrent, [], msg='Error: Row 1 should have been deleted by CASCADE')

        # Update a player and confirm it propagates
        self.cur.execute("UPDATE Player SET PlayerID = 13 WHERE UserName = 'CornRach';")
        self.con.commit()
        expect = (1, 13, 0)
        ckUpdate = self.cur.execute("""SELECT * FROM Contestant WHERE PlayerID = 
                                          (SELECT PlayerID FROM Player WHERE UserName = 'CornRach');""").fetchone()
        self.assertEqual(expect, ckUpdate, msg='Error: Expect the PlayerID UPDATE to CASCADE.')
              