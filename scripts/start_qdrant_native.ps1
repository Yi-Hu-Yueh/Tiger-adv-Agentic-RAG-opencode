# Start Windows Native Qdrant for this project (from scratch, no sibling deps)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
$QdrantExe = Join-Path $Root "runtime\qdrant\qdrant.exe"
$Config = Join-Path $Root "config\qdrant-native.yaml"
$LogDir = Join-Path $Root "runtime\qdrant"
$LogFile = Join-Path $LogDir "qdrant-native.log"
$PidFile = Join-Path $LogDir "qdrant-native.pid"

if (-not (Test-Path $QdrantExe)) { throw "Missing $QdrantExe" }
if (-not (Test-Path $Config)) { throw "Missing $Config" }

# Already running?
try {
  $h = Invoke-RestMethod "http://127.0.0.1:6333/healthz" -TimeoutSec 3
  if ($h -match "healthz check passed") { Write-Output "Qdrant already running on 6333"; exit 0 }
} catch { }

$proc = Start-Process -FilePath $QdrantExe -ArgumentList @("--config-path", "`"$Config`"") -WorkingDirectory $Root -RedirectStandardOutput $LogFile -RedirectStandardError "$LogDir\qdrant-native.err.log" -PassThru
Set-Content -Path $PidFile -Value $proc.Id
Write-Output "Starting Qdrant PID $($proc.Id)..."

for ($i = 0; $i -lt 30; $i++) {
  Start-Sleep -Seconds 1
  try {
    $r = Invoke-RestMethod "http://127.0.0.1:6333/healthz" -TimeoutSec 2
    if ("$r" -match "healthz check passed") {
      Write-Output "Native Qdrant ready on http://127.0.0.1:6333 (PID $($proc.Id))."
      exit 0
    }
  } catch { }
}
throw "Qdrant did not become ready. See $LogFile"
