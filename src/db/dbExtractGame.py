from pathlib import Path
import re
import sqlite3

# All required paths
dbPath = Path(__file__).parent.resolve().joinpath('notJeopardyDB.db')
dataPath = Path(__file__).parent.resolve().joinpath('data')

# Regex patterns for each attribute (except points - not compatible w/ regex strat)
catMatch = re.compile(r'class="category_name">(.+)</td>')
qMatch = re.compile(r'"clue_(.?J)_[0-9]_[0-9]" class="clue_text">(.+)</td>')
qMatchFJ = re.compile(r'"clue_(FJ)" class="clue_text">(.+)</td>')
aMatch = re.compile(r'class="correct_response">(.+)</em>')

# Some html cleanup needed for text extracts
cleanupList = [(r'&amp;', '&'), (r'<br />', ' '), (r"\\'s", "'s"), (r'<i>', ''), (r'</i>', '')]

# Lists to capture each attribute
UniqueCategory = []
Category = []
Round = []
PointValue = []
QuestionText = []
QuestionAns = []

# For others, iterate through files in data
for f in dataPath.iterdir():
    if Path(f).resolve().is_file():
        with open(f, mode='r', encoding='utf-8') as data:
            for line in data.readlines():
                
                # Get categories
                match = re.search(catMatch, line)
                if match is not None:
                    cat = match.group(1)
                    for item in cleanupList:
                        cat = re.sub(item[0], item[1], cat)
                    UniqueCategory.append(cat)

                    continue

                # Get round and question text for J, DJ
                match = re.search(qMatch, line)
                if match is not None:
                    rd = match.group(1)
                    Round.append(rd)

                    q = match.group(2)
                    for item in cleanupList:
                        q = re.sub(item[0], item[1], q)
                    QuestionText.append(q)

                    continue

                # Get round and question text for FJ
                match = re.search(qMatchFJ, line)
                if match is not None:
                    rd = match.group(1)
                    Round.append(rd)

                    q = match.group(2)
                    for item in cleanupList:
                        q = re.sub(item[0], item[1], q)
                    QuestionText.append(q)

                    continue

                # Get answer text
                match = re.search(aMatch, line)
                if match is not None:
                    ans = match.group(1)
                    for item in cleanupList:
                        ans = re.sub(item[0], item[1], ans)
                    QuestionAns.append(ans)

                    continue

            data.close()
            
# Generate points de novo:
values = [100, 200, 300, 400, 500, 200, 400, 600, 800, 1000]
for value in values:
    for i in range(6):
        PointValue.append(value)
PointValue.append(0) # Placeholder for FJ

# Expand categories to be 1:1 with questions
# Round J
for j in range(5):
    for name in UniqueCategory[0:6]:
        Category.append(name)
# Round DJ
for j in range(5):
    for name in UniqueCategory[6:12]:
        Category.append(name)
# Round FJ
Category.append(UniqueCategory[-1])

# Temp Extraction QC - make more rigorous for finished product
print(f'Captured {len(UniqueCategory)} unique category names.')
# print(UniqueCategory)
print(f'Captured {len(Category)} total category names.')
# print(Category)
print(f'Captured {len(PointValue)} point values.')
# print(PointValue)
print(f'Captured {len(Round)} round markers.')
# print(Round)
print(f'Captured {len(QuestionText)} questions.')
# print(QuestionText)
print(f'Captured {len(QuestionAns)} answers.')
# print(QuestionAns)

# zip together the four lists
allRows = list(zip(Category, Round, PointValue, QuestionText, QuestionAns))

# Temp row creation QC - make more rigorous for the finished product
print(f'Created {len(allRows)} 5-tuples for the database.')
#print(allRows)

# Connect to the db
con = sqlite3.connect(dbPath)
cur = con.cursor()

# Iterate through the tuples and executemany to get them into the db
cur.executemany("INSERT INTO Question (Category, Round, PointValue, QuestionText, QuestionAns) VALUES(?, ?, ?, ?, ?)", allRows)
con.commit()

# Quick QC Check that this worked
cur.execute("SELECT * FROM Question")
print(cur.fetchall())

con.close()