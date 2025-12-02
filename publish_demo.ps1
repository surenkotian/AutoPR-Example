param(
    [Parameter(Mandatory=$true)]
    [string]$RemoteUrl,
    [string]$Branch = 'main'
)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $Root
try {
    if (-not (Test-Path .git)) { git init }
    git add .
    git commit -m 'Initial AutoPR demo repo' -q -a -m 'initial' 2>$null || Write-Host 'Commit already exists'.
    git branch -M $Branch
    if (-not (git remote)) { git remote add origin $RemoteUrl } else { git remote set-url origin $RemoteUrl }
    git push -u origin $Branch
    Write-Host "Demo published to $RemoteUrl (branch $Branch)"
}
finally { Pop-Location }
