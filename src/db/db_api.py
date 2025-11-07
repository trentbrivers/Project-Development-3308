import sqlite3 as sql


def add_players(db_file, usernames):
    print(db_file)
    with sql.connect(db_file) as conn:
        cursor = conn.cursor()

        for username in usernames:
            cursor.execute(
        '''
                INSERT INTO Player (UserName, TotalGamesPlayed, TotalGamesWon, TotalGamesRunnerUp, HighScore)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, 0, 0, 0, 0))

        cursor.close()
        conn.commit()