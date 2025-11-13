# Execute `PRAGMA foreign_keys = ON` for all connections; https://sqlite.org/foreignkeys.html

import dbDDL
import dbDMLStubs
import dbExtractGame
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
        PosCtrl1 = [('game_0000', 'J', 'Testing', 100, 'Why are we doing this?', 'To test basic RI actions.'),
               ('game_0000', 'J', 'Birds', 500, 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")]
        dbDMLStubs.Question_InsertRow(self.dbPath, PosCtrl1)
        queryRes = self.cur.execute("SELECT GameCode, Round, Category, PointValue, QuestionText, QuestionAns FROM Question;").fetchall()
        self.assertEqual(PosCtrl1, queryRes, msg='Error: Expect the INSERT and SELECT to match.')
        
        # This should also work - different questions can have the same answer
        PosCtrl2 = [('game_0000', 'DJ', 'Testing', 200, 'Why do we validate table constraints?', 'To test basic RI actions.')]
        # Query this and wrap in an assertEquals
        dbDMLStubs.Question_InsertRow(self.dbPath, PosCtrl2)
        queryRes = self.cur.execute("SELECT GameCode, Round, Category, PointValue, QuestionText, QuestionAns FROM Question WHERE Round = 'DJ';").fetchall()
        self.assertEqual(PosCtrl2, queryRes, msg='Error: Expect the INSERT and SELECT to match.')

        # This should fail - violates uniqueness constraint
        NegCtrl1 = [('game_0000', 'FJ', 'Testing', 0, 'Why do we validate table constraints?', 'Broken DB logic is no fun.')]
        with self.assertRaises(sqlite3.IntegrityError):
            dbDMLStubs.Question_InsertRow(self.dbPath, NegCtrl1)

        # Note: this passes, but it takes 26s b/c of internal disk I/O in sqlite3 - proceed with caution!
        # # Every single one of these should violate a NOT NULL constraint
        # NegCtrl2 = [[('NULL', 'J', 'Birds', 500, 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")],
        #             [('game_0000', 'NULL', 'Birds', 500, 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")],
        #             [('game_0000', 'J', 'NULL', 500, 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")],
        #             [('game_0000', 'J', 'Birds', 'NULL', 'This unusual shorebird has showy females and drab males.', "Wilson's Pharalope")],
        #             [('game_0000', 'J', 'Birds', 500, 'NULL', "Wilson's Pharalope")],
        #             [('game_0000', 'J', 'Birds', 500, 'This unusual shorebird has showy females and drab males.', 'NULL')]]
        
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

    def test_GameQuestion_SetupGameBoard(self):
        
        # Need to populate tbls Question, Game, and GameQuestion
        dbExtractGame.extract_game(self.dbPath, self.parentPath.joinpath('test_data'))
        dbDMLStubs.Game_CreateNewGame(self.dbPath)
        dbDMLStubs.GameQuestion_SetupGameboard(self.dbPath, 'game_6692')

        # Generate expected rows
        expect = [(1, i+1, 'N') for i in range(61)]
        query = self.cur.execute("SELECT * FROM GameQuestion").fetchall()
        self.assertEqual(expect, query, msg='Error: Expect these results to match.')
    
    def test_GameQuestion_DropQuestionsOrGames(self):
        """Confirm that RI actions (ON DELETE CASCADE ON UPDATE CASCADE) work"""
        
        # Need to populate tbls Question, Game, and GameQuestion
        dbExtractGame.extract_game(self.dbPath, self.parentPath.joinpath('test_data'))
        dbDMLStubs.Game_CreateNewGame(self.dbPath)
        dbDMLStubs.GameQuestion_SetupGameboard(self.dbPath, 'game_6692')

        # Delete a PointValue and confirm its Questions are gone
        # Positive control: Contestant should obviously exist before deletion!
        expect = [(1, i+1, 'N') for i in range(6)]
        posCtrl = self.cur.execute("""SELECT * FROM GameQuestion WHERE QuestionID IN 
                                        (SELECT QuestionID FROM Question WHERE PointValue = 100);""").fetchall()
        self.assertEqual(expect, posCtrl, msg='Error: Expect this row to exist before PointValue = 100 is deleted from Question.')

        self.cur.execute("DELETE FROM Question WHERE PointValue = 100;")
        self.con.commit()

        # Confirm $100 questions are gone from GameQuestion and nothing else is.
        rowsLeft = len(self.cur.execute("SELECT * FROM GameQuestion;").fetchall())
        self.assertEqual(rowsLeft, 55, msg='Error: Only 6 GameQuestion rows should have ON DELETE CASCADE')
        wheres100 = self.cur.execute("SELECT * FROM GameQuestion WHERE QuestionID IN (1, 2, 3, 4, 5, 6);").fetchall()
        self.assertEqual(wheres100, [], msg='Error: Rows 1-6 should have been deleted by CASCADE')

        # Update the GameID and confirm it propagates
        self.cur.execute("UPDATE Game SET GameID = 13 WHERE GameID = 1;")
        self.con.commit()
        expect = (13, 7, 'N')
        ckUpdate = self.cur.execute("""SELECT * FROM GameQuestion WHERE QuestionID = 7;""").fetchone()
        self.assertEqual(expect, ckUpdate, msg='Error: Expect the GameID UPDATE to CASCADE.')
    
    def test_PlayerAnswer_AddSubmittedAnswer(self):
        
        # Test-specific setup: Need Question, Player, Game
        dbExtractGame.extract_game(self.dbPath, self.parentPath.joinpath('test_data'))
        dbDMLStubs.Game_CreateNewGame(self.dbPath)
        for username in self.UserNames:
            with self.subTest(i=self.UserNames.index(username)):
                dbDMLStubs.Player_newUserSignup(self.dbPath, username)

        # Make sure the QC check on isCorrect works
        with self.assertRaises(ValueError):
            dbDMLStubs.PlayerAnswer_AddSubmittedAnswer(self.dbPath, 1, 1, 1, 'An answer', 'p' )

        # Make sure a regular insert works
        dbDMLStubs.PlayerAnswer_AddSubmittedAnswer(self.dbPath, 1, 1, 1, 'An answer', 'y' )
        expect = (1, 1, 1, 'An answer', 'Y')
        query = self.cur.execute("SELECT * FROM PlayerAnswer").fetchone()
        self.assertEqual(expect, query, msg='Error: Expect these two rows to match.')

    def test_PlayerAnswer_ChangeOrDeleteFKs(self):
        """Confirm that RI actions (ON DELETE CASCADE ON UPDATE CASCADE) work"""
        
        # Test-specific setup: Need Question, Player, Game
        dbExtractGame.extract_game(self.dbPath, self.parentPath.joinpath('test_data'))
        dbDMLStubs.Game_CreateNewGame(self.dbPath)
        for username in self.UserNames:
            with self.subTest(i=self.UserNames.index(username)):
                dbDMLStubs.Player_newUserSignup(self.dbPath, username)

        # Answer some questions
        testAns = [(2, 1, 3, 'Its cover', 'Y'),
                   (3, 1, 8, 'Yeti', 'Y'),
                   (2, 1, 18, 'rivers', 'N'),
                   (1, 1, 25, 'Helena', 'Y')]
        for ans in testAns:
            dbDMLStubs.PlayerAnswer_AddSubmittedAnswer(self.dbPath, ans[0], ans[1], ans[2], ans[3], ans[4])

        # Delete a PointValue and confirm its Questions are gone
        # Positive control: PlayerAnswer should obviously exist before deletion!
        expect = (2, 1, 3, 'Its cover', 'Y')
        posCtrl = self.cur.execute("""SELECT * FROM PlayerAnswer WHERE QuestionID IN 
                                        (SELECT QuestionID FROM Question WHERE PointValue = 100);""").fetchone()
        self.assertEqual(expect, posCtrl, msg='Error: Expect this row to exist before PointValue = 100 is deleted from Question.')

        self.cur.execute("DELETE FROM Question WHERE PointValue = 100;")
        self.con.commit()

        # Confirm question 3 is gone from PlayerAnswer and nothing else is.
        rowsLeft = len(self.cur.execute("SELECT * FROM PlayerAnswer;").fetchall())
        self.assertEqual(rowsLeft, len(testAns)-1, msg='Error: Only 1 PlayerAnswer row should have ON DELETE CASCADE')
        wheres3 = self.cur.execute("SELECT * FROM GameQuestion WHERE QuestionID IN (1, 2, 3, 4, 5, 6);").fetchone()
        self.assertIsNone(wheres3, msg='Error: Question 3 ans should have been deleted by CASCADE')

        # Update the GameID and confirm it propagates
        self.cur.execute("UPDATE Game SET GameID = 13 WHERE GameID = 1;")
        self.con.commit()
        expect = (3, 13, 8, 'Yeti', 'Y')
        ckUpdate = self.cur.execute("""SELECT * FROM PlayerAnswer WHERE QuestionID = 8;""").fetchone()
        self.assertEqual(expect, ckUpdate, msg='Error: Expect the GameID UPDATE to CASCADE.')
        
        # Delete the PlayerID and confirm it cascades
        self.cur.execute("DELETE FROM Player WHERE PlayerID = 3;")
        self.con.commit()
        ckUpdate = self.cur.execute("""SELECT * FROM PlayerAnswer WHERE QuestionID = 8;""").fetchone()
        self.assertIsNone(ckUpdate, msg='Error: Expect the PlayerID DELETE to CASCADE.')

        # Delete the GameID and confirm it cascades
        self.cur.execute("DELETE FROM Game WHERE GameID = 13;")
        self.con.commit()
        ckUpdate = self.cur.execute("""SELECT * FROM PlayerAnswer;""").fetchall()
        self.assertEqual([], ckUpdate, msg='Error: Expect the GameID DELETE to CASCADE.')