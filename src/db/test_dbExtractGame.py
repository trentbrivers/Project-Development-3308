import src.db.dbDDL as dbDDL
import src.db.dbExtractGame as dbExtractGame
from pathlib import Path
import sqlite3
import unittest

class dbExtractGameTestCase(unittest.TestCase):
    def setUp(self):
        db = 'test_db'
        dataDir = 'test_data'

        self.dbPath = Path(__file__).parent.resolve().joinpath(db)
        self.parentPath = self.dbPath.parent.resolve()
        self.dataPath = self.parentPath.joinpath(dataDir) # Do I need this?

        dbDDL.preClean(self.dbPath)
        dbDDL.dbDDL(self.dbPath)
        dbExtractGame.extract_game(self.dbPath, self.dataPath)

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
    
    def test_extract_game(self):
        # Gold label data taken manually from game_6692 
        trueGameCode = {'game_6692'}
        
        trueRounds = {'J', 'DJ', 'FJ'}

        trueCategories = {'STATE CAPITALS', 'MONSTERS', 'PROVERBS', '1949', 'THE CIRCLE', 'COMMON BONDS', 'FAMOUS NAMES', 'TRAVEL & TOURISM', 
                          'COMPOSERS', 'SUPREME COURT DECISIONS', "CHILDREN'S LITERATURE", 'POTPOURRI', 'THE BIBLE'}

        trueQs = {"This city on Ohio's Scioto River was laid out in 1812", "It's affectionately known as Nessie",
                  """"You can't judge a book by its binding", nor by this""", 
                  'On August 23 a manslaughter charge was filed against the cabbie who killed this "Gone with the Wind" author',
                  "It's the device with one pointed leg & a pencil on the other, used to draw circles",
                  'The Royal Standard, the Jolly Roger, the Stars and Stripes', 'Until 1900 Newport & this city were co-capitals of Rhode Island',
                  "It's the name native Tibetans have given to the Abominaible Snowman", 
                  """It's long been said, "If you want peace, you must prepare" for this""", 
                  'Mohammed Reza Pahlavi, shah of this country, was wounded when a reporter fired 5 shots at him',
                  'Name for the chord or line that goes through the center', 'Art, wax, natural history', 
                  'The art center in this Iowa capital was designed in the 1940s by Eliel Saarinen', 'The simurgh, like the roc, was a giant one of these', 
                  'An African proverb says, "Leave a log in the water as long as you like, it will never be" this reptile', 
                  "In this country's first election, David Ben-Gurion's Mapai Party won a large plurality", 
                  'An arc that covers 25% of the circumference measures this many degrees', 'Sudd, Dismal, Okefenokee', 
                  'Battle Abbey in this city is the headquarters of the Virginia Historical Society', 
                  'A manticore has a human head, the body of a lion & the tail of this zodiac arachnid', 
                  'Completes the proverb "The spirit is willing, but..."', 
                  'April 14 the war crimes tribunal in this German city passed sentence on 19 criminals', 
                  'This part of a circle shares its name with a bone in the arm', 'Sheep, blessings, calories', 
                  "It's the northernmost state capital in the Rocky Mountains", 
                  'This monster that lived under a fig tree across from Scylla swallowed & threw up the sea waters 3 times a day', 
                  '"No rose without a thorn" & "no garden without" these', 'In his January 5 state of the union message, he called for a "Fair Deal"', 
                  'Fraction used as a common estimate for pi', 'Scottish, Skye, sealyham', 
                  'At 25 he captured a $25,000 prize for being the first person to fly the Atlantic solo', 
                  'The Lambeth, Westminster & Waterloo Bridges all span this river', 
                  'The Stadtpark in Vienna features a statue of this "Waltz King" with violin in hand', 
                  """1963's Gray v. Sanders established the concept of "one man, one" this in reapportionment""", 
                  'The first use of this name for the heroine of "The Three Bears" occurred around 1904', 
                  "While it's been on coins since the Civil War, it wasn't made the national motto until 1956", 
                  'In one year, 1882, he received 75 patents on his inventions', 
                  "Collier's Weekly helped raise money to buy this president's Kentucky birthplace in 1905-06", 
                  """Having sold the rights, he wasn't recognized as the composer of "Swanee River" until after his death""", 
                  'Ware v. Hylton in 1796, held that these international agreements supersede state laws', 
                  'In this 1726 satire, high heels & low heels in Lilliput represent the Tories & the Whigs', 
                  """This outer space "breeze" interacts with the Earth's atmosphere to create the auroras""", 
                  'Survey says from 1929-1931 this famous pollster was head of the journalism dept. at Drake University', 
                  'A Vietnam War exhibit is one of the highlights at his presidential library in Austin, Texas', 
                  'Beethoven called this oratorio composer "the greatest composer that ever lived"', 
                  'In Dartmouth College v. Woodward, the court kept this state from taking over the college', 
                  '"Anne of Avonlea" was the first sequel to this 1908 book about a red-haired orphan girl', 
                  'The 3 gifts associated with Epiphany', 'To generations of dancers, this late Russian-born choreographer was known as "Mr. B."', 
                  'Fort Frederica on St. Simons Island in this state was built by James Oglethorpe in the 1730s', 
                  "The inspiration for many of this Norwegian's songs was his cousin Nina Hagerup, whom he married in 1867", 
                  "As a result of this man's suit against Arizona, police must read arrestees their right", 
                  'In 1942 this "Dr. Dolittle" author wrote an anti-war poem for adults titled "Victory for the Slain"', 
                  "His watercolor paintings were put on 1994 British stamps to celebrate his investiture's 25th anniversary", 
                  'He was teaching at the University of Chicago when he was awarded the 1976 Nobel Prize in Economics', 
                  "The 1,815-foot CN Tower in this Canadian city is the world's tallest self-supporting structure", 
                  'After composing "Peter and the Wolf", he wrote "Cantata for the 20th Anniversary of the October Revolution"', 
                  'Dennis v. U.S. upheld the convictions of 11 leaders of this party under the Smith Act', 
                  'In this Mary Rodgers story, a 13-year-old girl wakes up to find that she has become her own mother', 
                  "We bet you knew U Nu was this country's first premier", 'Although blind, he killed 3,000 at a religious festival'}
        
        trueAs = {'Columbus', 'the Loch Ness Monster', 'its cover', '(Margaret) Mitchell', 'a compass', 'flags', 'Providence', 'the Yeti', 'war', 
                  'Iran', 'the diameter', 'types of museums', 'Des Moines', 'a giant bird', 'a crocodile', 'Israel', '90', 'swamps', 'Richmond', 
                  'a scorpion', 'the flesh is weak', 'Nuremberg', 'the radius', 'things you count', 'Helena (Montana)', 'Charybdis', 'weeds', 
                  'Truman', '22/7', 'different kinds of dogs (terriers)', 'Lindbergh', 'the Thames', '(Johann) Strauss', 'vote', 'Goldilocks', 
                  'In God We Trust', 'Edison', 'Lincoln', '(Stephen) Foster', 'treaties', "Gulliver's Travels", 'the solar wind', '(George) Gallup', 
                  'Lyndon Baines Johnson', 'Handel', 'New Hampshire', 'Anne of Green Gables', 'gold, frankincense and myrrh', 'George Ballanchine', 
                  'Georgia', '(Edvard) Grieg', '(Ernesto) Miranda', '(Hugh) Lofting', 'the Prince of Wales (Prince Charles)', '(Milton) Friedman', 
                  'Toronto', 'Prokofiev', 'the Communist Party', 'Freaky Friday', 'Burma', 'Samson'}
        
        con = sqlite3.connect(self.dbPath)
        cur = con.cursor()
        
        # Validate GameID
        allGameCodes = set([item[0] for item in cur.execute("SELECT DISTINCT GameCode FROM Question;").fetchall()])
        self.assertEqual(trueGameCode, allGameCodes, msg='Error: GameID does not match.')
        
        # Validate Rounds
        allRounds = set([item[0] for item in cur.execute("SELECT DISTINCT Round FROM Question;").fetchall()])
        self.assertEqual(trueRounds, allRounds, msg='Error: Round attributes do not match.')

        # Validate Categories
        allCategories = set([item[0] for item in cur.execute("SELECT Category FROM Question;").fetchall()])
        self.assertEqual(trueCategories, allCategories, msg='Error: Category attributes do not match.')

        # Validate Questions
        allQs = set([item[0] for item in cur.execute("SELECT QuestionText FROM Question;").fetchall()])
        self.assertEqual(trueQs, allQs, msg='Error: Category attributes do not match.')

        # Validate Answers
        allAs = set([item[0] for item in cur.execute("SELECT QuestionAns FROM Question;").fetchall()])
        self.assertEqual(trueAs, allAs, msg='Error: Category attributes do not match.')

        con.close()

# Run Test Cases
if __name__ == '__main__':
    unittest.main()