# Stop project Native Qdrant
$PidFile = Join-Path (Split-Path -Parent (Split-Path -Parent $PSCommandPath)) "runtime\qdrant\qdrant-native.pid"
if (Test-Path $PidFile) {
  $pidId = [int](Get-Content $PidFile | Select-Object -First 1)
  try { Stop-Process -Id $pidId -Force -ErrorAction SilentlyContinue; Write-Output "Stopped PID $pidId" } catch { }
  Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
}
# Fallback: kill qdrant.exe under this runtime path
Get-Process qdrant -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*opencode-prjs*Tiger-adv-Agentic-RAG-opencode*" } | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Output "done"
