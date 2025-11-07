$response = Invoke-WebRequest -Uri "http://localhost:5000/initialize_game" -Method POST -Body '{"players": ["rachelm", "trentr", "darvinc"]}' -ContentType 'application/json' -UseBasicParsing
$response
$response.content