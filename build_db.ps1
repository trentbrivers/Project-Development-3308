$root=(Get-Location).path
cd $root/src/db

python dbDDL.py notJeopardyDB.db
python dbExtractGame.py notJeopardyDB.db

