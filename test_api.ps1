# Test API endpoints
$uri = 'http://localhost:6969'
$headers = @{'Content-Type' = 'application/json'}

Write-Host "Testing Frontend (GET /):" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$uri/" -Method GET -ErrorAction Stop
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "OK - Frontend loads"
} catch {
    Write-Host "Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    Write-Host "ERROR - Frontend not loading"
}

Write-Host "`nTesting Static Files (GET /static/index.html):" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$uri/static/index.html" -Method GET -ErrorAction Stop
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "OK - Static files loading"
} catch {
    Write-Host "Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    Write-Host "ERROR - Static files not loading"
}

Write-Host "`nTesting Docs (GET /docs):" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$uri/docs" -Method GET -ErrorAction Stop
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
}

Write-Host "`nTesting Registration (POST /api/auth/register):" -ForegroundColor Yellow
$body = ConvertTo-Json @{email='test@example.com'; password='password123'}
try {
    $response = Invoke-WebRequest -Uri "$uri/api/auth/register" -Method POST -Body $body -Headers $headers -ErrorAction Stop
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response: $($response.Content)" -ForegroundColor Cyan
} catch {
    Write-Host "Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    Write-Host "Response: $($reader.ReadToEnd())" -ForegroundColor Cyan
}
