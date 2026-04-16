# Path to your .flaskenv file
$envFile = ".flaskenv"
$envFile = ".localenv"

if (-Not (Test-Path $envFile)) {
    Write-Host ".flaskenv file not found!"
    exit 1  
}

# Read each non-empty, non-comment line
Get-Content $envFile | ForEach-Object {
    if ($_ -match "^\s*$" -or $_ -match "^\s*#") {
        return
    }

    $parts = $_ -split "=", 2
    $key = $parts[0].Trim()
    $value = $parts[1].Trim()

    # Set environment variable for current session
    [System.Environment]::SetEnvironmentVariable($key, $value, "Process")

    Write-Host "Loaded $key"
}

Write-Host  "Environment variables loaded into this PowerShell session."
