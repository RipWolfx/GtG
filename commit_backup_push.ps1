param(
    [string]$Message = "Auto-commit $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    [switch]$NoPush
)

$ErrorActionPreference = 'Stop'

# Repo root
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Backup base folder next to repo
$parentDir = Split-Path -Parent $repoRoot
$backupBase = Join-Path $parentDir 'senati_backend_backups'
if (-not (Test-Path $backupBase)) { New-Item -ItemType Directory -Force -Path $backupBase | Out-Null }

# Timestamped backup
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupDir = Join-Path $backupBase $timestamp
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

# Exclusions
$excludeDirs = @('.git','venv','.venv','__pycache__','.vscode','.idea')
$excludeFiles = @('*.pyc','*.pyo','Thumbs.db','.DS_Store')

# Build robocopy args
$xdArgs = @()
foreach($d in $excludeDirs){ $xdArgs += @('/XD', (Join-Path $repoRoot $d)) }
$xfArgs = @()
foreach($f in $excludeFiles){ $xfArgs += @('/XF', $f) }

# Perform backup copy
Write-Host "Creating backup at $backupDir..."
$robocopyArgs = @($repoRoot, $backupDir, '/E') + $xdArgs + $xfArgs
$proc = Start-Process -FilePath 'robocopy' -ArgumentList $robocopyArgs -Wait -NoNewWindow -PassThru
$rc = $proc.ExitCode
if ($rc -gt 7) { throw "Backup failed with Robocopy exit code $rc" }

# Commit and push
Set-Location $repoRoot
git add -A
try {
    git commit -m $Message
} catch {
    Write-Host "No changes to commit." -ForegroundColor Yellow
}

if (-not $NoPush) {
    git push
}

Write-Host "Backup saved at $backupDir and changes processed." -ForegroundColor Green
