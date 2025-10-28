$response = Invoke-WebRequest -Uri "http://localhost:5000/initialize_game" -Method GET
$response
$response.content