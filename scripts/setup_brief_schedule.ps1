<#
.SYNOPSIS
  Register (or remove) a Windows Task Scheduler job that runs the Naiad Daily
  Brief once a day. Optional -- NOT run by default (contract section 5).

.DESCRIPTION
  Creates a schtasks job that invokes scripts/daily_brief.py with the project
  venv and appends output to research_outputs/brief/brief_run.log.

  The brief is an OPS artifact. Scheduling it changes nothing about the
  firewall: it still never reads journals, never computes outcome statistics,
  and never becomes study evidence.

.PARAMETER Time
  Local 24h time to run, HH:mm. Default 07:30.

.PARAMETER TaskName
  Scheduled-task name. Default NaiadDailyBrief.

.PARAMETER Remove
  Delete the task instead of creating it.

.PARAMETER Force
  Overwrite an existing task of the same name.

.EXAMPLE
  .\scripts\setup_brief_schedule.ps1 -Time 07:30
.EXAMPLE
  .\scripts\setup_brief_schedule.ps1 -Remove
#>
[CmdletBinding()]
param(
    [string]$Time = "07:30",
    [string]$TaskName = "NaiadDailyBrief",
    [switch]$Remove,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repo ".venv\Scripts\python.exe"
$script = Join-Path $repo "scripts\daily_brief.py"
$logDir = Join-Path $repo "research_outputs\brief"
$log = Join-Path $logDir "brief_run.log"

if ($Remove) {
    Write-Host "Removing scheduled task '$TaskName'..."
    schtasks /Delete /TN $TaskName /F
    if ($LASTEXITCODE -eq 0) { Write-Host "Removed." } else { Write-Host "Not removed (see above)." }
    exit $LASTEXITCODE
}

if (-not (Test-Path $python)) { throw "venv python not found at $python" }
if (-not (Test-Path $script)) { throw "daily_brief.py not found at $script" }
if ($Time -notmatch '^([01]\d|2[0-3]):[0-5]\d$') { throw "Time must be HH:mm (24h), got '$Time'" }
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

# cmd wrapper so stdout/stderr can be appended to the run log
$inner = '"' + $python + '" "' + $script + '" >> "' + $log + '" 2>&1'
$action = 'cmd /c ' + '"' + $inner + '"'

$taskArgs = @('/Create', '/TN', $TaskName, '/TR', $action, '/SC', 'DAILY', '/ST', $Time, '/RL', 'LIMITED')
if ($Force) { $taskArgs += '/F' }

Write-Host "Registering '$TaskName' to run daily at $Time (local time)."
Write-Host "  python : $python"
Write-Host "  script : $script"
Write-Host "  log    : $log"
schtasks @taskArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "Registration failed. If the task already exists, re-run with -Force."
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Registered. Useful commands:"
Write-Host "  inspect : schtasks /Query /TN $TaskName /V /FO LIST"
Write-Host "  run now : schtasks /Run /TN $TaskName"
Write-Host "  REMOVE  : .\scripts\setup_brief_schedule.ps1 -Remove"
Write-Host "            (or: schtasks /Delete /TN $TaskName /F)"
Write-Host ""
Write-Host "Note: the machine must be awake at $Time; a missed run is simply"
Write-Host "absent from the archive -- the index has one line per date, and a"
Write-Host "later manual run for that date replaces it."
