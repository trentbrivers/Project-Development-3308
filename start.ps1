$root=(Get-Location).path

Start-Process -FilePath "powershell.exe" -ArgumentList  "-Command", "cd $root/front-end/not-jeopardy; npm start"
Start-Process -FilePath "powershell.exe" -ArgumentList  "-Command", ".venv/Scripts/activate; python -m src.backend.core"
