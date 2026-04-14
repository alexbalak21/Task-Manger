# Path to your API folder
$apiPath = "app"
$env:FLASK_APP = "app/App.py"

# Find all __pycache__ directories inside /app and delete them
Get-ChildItem -Path $apiPath -Recurse -Directory -Filter "__pycache__" |
    ForEach-Object {
        Write-Host "Deleting:" $_.FullName
        Remove-Item -Recurse -Force $_.FullName
    }

Write-Host "All __pycache__ folders removed."
