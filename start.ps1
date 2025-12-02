$root=(Get-Location).path

Start-Process -FilePath "powershell.exe" -ArgumentList  "-Command", ".venv/Scripts/activate; python -m src.backend.core"
