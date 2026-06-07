Push-Location (Join-Path $PSScriptRoot "app")
try {
    .\load-flask-env.ps1
    flask run
}
finally {
    Pop-Location
}