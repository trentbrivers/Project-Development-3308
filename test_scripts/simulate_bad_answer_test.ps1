Invoke-WebRequest -Uri "http://localhost:5000/submit_answer" -Method 'POST' -Body 'bad submission' -ContentType 'application/json' -UseBasicParsing
