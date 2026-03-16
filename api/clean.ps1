# Delete all __pycache__ folders inside the current /api directory
Get-ChildItem -Path "." -Recurse -Directory -Filter "__pycache__" |
    ForEach-Object {
        Write-Host "Deleting:" $_.FullName
        Remove-Item -Recurse -Force $_.FullName
    }

Write-Host "All __pycache__ folders removed."
